#!/usr/bin/env node
/**
 * Browser & Security Audit Script (Playwright).
 *
 * Runs passive checks (console, network, HTTP security headers, cookies,
 * storage keys, sourcemaps, horizontal overflow, optional axe-core) and
 * optional non-destructive form probes (--probe-forms) against localhost or
 * explicitly authorized staging URLs.
 *
 * Usage:
 *   node <skill-dir>/scripts/playwright_security_audit.mjs http://localhost:3000 \
 *     --routes /,/login --probe-forms --out audit.json
 *
 * Exit codes:
 *   0 = completed
 *   1 = invalid CLI arguments / runtime error
 *   2 = refused target (non-http(s) protocol or remote host without --allow-remote)
 *   3 = playwright not found in current project or Node resolution path
 */

import fs from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";

const SQL_ERROR_SIGNATURES = [
  /SQLSTATE\[/i,
  /syntax error at or near/i,
  /unterminated quoted string/i,
  /pg_query\(\)|PostgreSQL.{0,20}ERROR:|PG::\w+Error/i,
  /You have an error in your SQL syntax/i,
  /Warning:\s*mysqli?_/i,
  /SQLite3::|SQLITE_ERROR/i,
  /System\.Data\.SqlClient|Microsoft OLE DB Provider/i,
  /ORA-\d{5}/i,
  /MongoServerError|CastError to ObjectId/i,
];

const STACK_TRACE_SIGNATURES = [
  /Traceback \(most recent call last\):/,
  /\bat\s+[\w.$]+\s+\([^)]+:\d+:\d+\)/,
  /Fatal error:.*on line \d+/i,
];

const RECOMMENDED_HEADERS = [
  "content-security-policy",
  "x-content-type-options",
  "referrer-policy",
  "permissions-policy",
];

// Formularios cuyo envío podría ser destructivo o tener efectos reales: se omiten salvo --include-risky-forms.
const RISKY_FORM_PATTERN =
  /delete|remove|destroy|eliminar|borrar|pay|checkout|purchase|buy|pagar|comprar|transfer|logout|signout|cancel|revoke|deactivate/i;

const SENSITIVE_QUERY_PARAM =
  /token|key|secret|pass|pwd|auth|jwt|code|session|sig|credential|bearer/i;

const SAFE_FORM_PROBES = [
  { name: "xss_dom_probe", value: `AUDIT_XSS_TEXT_<b>probe</b>` },
  { name: "xss_img_probe", value: `"><img src=x onerror="window.__auditXssTriggered='img'">` },
  { name: "xss_svg_probe", value: `<svg onload="window.__auditXssTriggered='svg'">` },
  { name: "sqli_quote_probe", value: `' OR '1'='1` },
  { name: "sqli_single_quote_probe", value: `'` },
  { name: "nosqli_probe", value: `{"$ne":null}` },
  { name: "path_traversal_probe", value: `../../../../etc/passwd` },
  { name: "unicode_control_probe", value: `\u0000\u202E\u{1F4A5}` },
  { name: "boundary_long_probe", value: "A".repeat(1200) },
];

const USAGE =
  "Usage: node playwright_security_audit.mjs <url> [--routes /,/login] [--probe-forms] [--include-risky-forms] [--max-forms 10] [--screenshots-dir dir] [--color-scheme light|dark|both] [--allow-remote] [--out report.json]\n" +
  "  --routes <list>          rutas separadas por coma (default: /)\n" +
  "  --probe-forms            ejecuta sondas seguras no destructivas sobre formularios\n" +
  "  --include-risky-forms    tambien prueba formularios de borrado/pago/logout (solo con datos de prueba)\n" +
  "  --max-forms <n>          maximo de formularios a sondear por ruta (default: 10)\n" +
  "  --screenshots-dir <dir>  captura PNGs (wide 1920x1080, desktop 1440x900, tablet 768x1024, mobile 390x844; fold + fullPage) para revision visual\n" +
  "  --color-scheme <mode>    esquema de color al capturar screenshots: light | dark | both (default: light)\n" +
  "  --allow-remote           autoriza auditar un host staging no local (solo entornos autorizados)\n" +
  "  --out <archivo.json>     guarda el reporte JSON detallado en disco\n" +
  "  Nota: IDOR/CSRF requieren dos usuarios y se verifican manualmente (ver SKILL.md).";

const SCREENSHOT_VIEWPORTS = [
  { name: "wide", width: 1920, height: 1080 },
  { name: "desktop", width: 1440, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "mobile", width: 390, height: 844 },
];

function parseArgs(argv) {
  const args = argv.slice(2);
  if (!args.length || args.includes("--help") || args.includes("-h")) {
    console.log(USAGE);
    process.exit(args.length ? 0 : 1);
  }

  const url = args[0];
  if (url.startsWith("-")) {
    console.error(`Error: el primer argumento debe ser la URL objetivo, no "${url}".\n\n${USAGE}`);
    process.exit(1);
  }

  let routes = ["/"];
  let probeForms = false;
  let includeRisky = false;
  let allowRemote = false;
  let maxForms = 10;
  let screenshotsDir = null;
  let colorScheme = "light";
  let outFile = null;

  for (let i = 1; i < args.length; i += 1) {
    const a = args[i];
    if (a === "--routes") {
      if (!args[i + 1] || args[i + 1].startsWith("--")) {
        console.error("Error: --routes requiere una lista separada por comas (ej. --routes /,/login).");
        process.exit(1);
      }
      routes = args[++i].split(",").map((r) => r.trim()).filter(Boolean);
      if (!routes.length) {
        console.error("Error: --routes no puede quedar vacio.");
        process.exit(1);
      }
    } else if (a === "--probe-forms") {
      probeForms = true;
    } else if (a === "--include-risky-forms") {
      includeRisky = true;
    } else if (a === "--allow-remote") {
      allowRemote = true;
    } else if (a === "--max-forms") {
      const raw = args[++i];
      const parsedMax = Number.parseInt(raw || "", 10);
      if (!Number.isFinite(parsedMax) || parsedMax < 1) {
        console.error("Error: --max-forms requiere un entero >= 1.");
        process.exit(1);
      }
      maxForms = parsedMax;
    } else if (a === "--screenshots-dir") {
      if (!args[i + 1] || args[i + 1].startsWith("--")) {
        console.error("Error: --screenshots-dir requiere un directorio destino (ej. --screenshots-dir .audit-screenshots).");
        process.exit(1);
      }
      screenshotsDir = args[++i];
    } else if (a === "--color-scheme") {
      const rawScheme = (args[++i] || "").toLowerCase();
      if (!["light", "dark", "both"].includes(rawScheme)) {
        console.error("Error: --color-scheme debe ser light, dark o both.");
        process.exit(1);
      }
      colorScheme = rawScheme;
    } else if (a === "--out") {
      if (!args[i + 1] || args[i + 1].startsWith("--")) {
        console.error("Error: --out requiere una ruta de archivo de salida (ej. --out audit.json).");
        process.exit(1);
      }
      outFile = args[++i];
    } else {
      console.error(`Error: opcion desconocida "${a}".\n\n${USAGE}`);
      process.exit(1);
    }
  }
  return { url, routes, probeForms, includeRisky, allowRemote, maxForms, screenshotsDir, colorScheme, outFile };
}

function sanitizeRouteSlug(routePath) {
  const pathOnly = String(routePath || "/").split(/[?#]/)[0];
  const cleaned = pathOnly
    .replace(/^\/+|\/+$/g, "")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase();
  return cleaned ? cleaned.slice(0, 60) : "root";
}

function isLocalHostname(hostname) {
  return ["localhost", "127.0.0.1", "::1", "[::1]"].includes(hostname.toLowerCase());
}

function redactUrl(rawUrl) {
  try {
    const u = new URL(rawUrl);
    if (u.password) u.password = "REDACTED";
    for (const [k] of u.searchParams.entries()) {
      if (SENSITIVE_QUERY_PARAM.test(k)) {
        u.searchParams.set(k, "REDACTED");
      }
    }
    return u.toString();
  } catch {
    return rawUrl;
  }
}

async function loadOptionalModule(pkgName) {
  // 1. Resolve from target project's working directory (critical when skill is installed globally)
  try {
    const cwdRequire = createRequire(path.join(process.cwd(), "package.json"));
    const resolved = cwdRequire.resolve(pkgName);
    return await import(pathToFileURL(resolved).href);
  } catch {
    // Fall through to standard ESM resolution from script directory / NODE_PATH
  }
  return await import(pkgName);
}

function checkTextSignatures(text) {
  const hits = [];
  for (const re of SQL_ERROR_SIGNATURES) {
    if (re.test(text)) hits.push(`sql_error:${re.source}`);
  }
  for (const re of STACK_TRACE_SIGNATURES) {
    if (re.test(text)) hits.push(`stack_trace:${re.source}`);
  }
  return hits;
}

function extractSourceMapUrl(jsBody, scriptUrl) {
  const matches = jsBody.match(/\/\/[#@]\s*sourceMappingURL=([^\s'"]+)/g);
  if (!matches || !matches.length) return null;
  const last = matches[matches.length - 1];
  const rawTarget = last.replace(/^\/\/[#@]\s*sourceMappingURL=/, "").trim();
  if (!rawTarget || rawTarget.startsWith("data:")) return null;
  try {
    return new URL(rawTarget, scriptUrl).toString();
  } catch {
    return null;
  }
}

async function auditRoute(
  context,
  baseUrl,
  routePath,
  { probeForms, includeRisky, maxForms, screenshotsDir, colorScheme }
) {
  const targetUrl = new URL(routePath, baseUrl).toString();
  const targetOrigin = new URL(targetUrl).origin;
  const page = await context.newPage();

  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  const httpErrors = [];
  const bodyLeakHits = [];
  const sourcemapsExposed = new Set();
  const candidateSourcemaps = new Set();
  const pendingChecks = [];

  page.on("console", (msg) => {
    if (msg.type() === "error") {
      consoleErrors.push(msg.text().slice(0, 300));
    }
  });
  page.on("pageerror", (err) => {
    pageErrors.push(String(err).slice(0, 300));
  });
  page.on("requestfailed", (req) => {
    failedRequests.push({
      url: redactUrl(req.url()),
      reason: req.failure()?.errorText || "failed",
    });
  });
  page.on("response", (res) => {
    const resUrl = res.url();
    const safeUrl = redactUrl(resUrl);
    const status = res.status();

    let resPath = resUrl;
    try {
      resPath = new URL(resUrl).pathname;
    } catch {
      // keep raw URL
    }
    if (resPath.endsWith(".map") && status === 200) {
      sourcemapsExposed.add(safeUrl);
    }
    if (status >= 400) {
      httpErrors.push({ url: safeUrl, status });
    }

    const ct = (res.headers()["content-type"] || "").toLowerCase();
    if (ct.includes("json") || ct.includes("html") || ct.includes("text/plain")) {
      pendingChecks.push(
        res
          .text()
          .then((body) => {
            const hits = checkTextSignatures(body.slice(0, 50000));
            if (hits.length) {
              bodyLeakHits.push({ url: safeUrl, status, hits });
            }
          })
          .catch(() => {})
      );
    } else if (
      status === 200 &&
      (ct.includes("javascript") || resPath.endsWith(".js") || resPath.endsWith(".mjs"))
    ) {
      pendingChecks.push(
        res
          .text()
          .then((body) => {
            const tail = body.slice(-2048);
            const mapUrl = extractSourceMapUrl(tail, resUrl);
            if (mapUrl && mapUrl.startsWith(targetOrigin)) {
              candidateSourcemaps.add(mapUrl);
            }
          })
          .catch(() => {})
      );
    }
  });

  await page.setViewportSize({ width: 1440, height: 900 });
  let mainResponse = null;
  try {
    mainResponse = await page.goto(targetUrl, { waitUntil: "networkidle", timeout: 30000 });
  } catch {
    mainResponse = await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
  }

  await Promise.allSettled(pendingChecks);

  const mainStatus = mainResponse ? mainResponse.status() : null;
  const finalUrl = page.url();
  const documentHeaders = mainResponse ? mainResponse.headers() : {};

  // Active lightweight check for referenced same-origin .map files (since headless Chromium doesn't fetch them)
  let checkedMaps = 0;
  for (const mapUrl of candidateSourcemaps) {
    if (checkedMaps >= 10) break;
    checkedMaps += 1;
    try {
      let resp = await context.request.head(mapUrl, { timeout: 5000 });
      if (resp.status() === 405) {
        resp = await context.request.get(mapUrl, { timeout: 5000 });
      }
      if (resp.status() === 200) {
        sourcemapsExposed.add(redactUrl(mapUrl));
      }
    } catch {
      // ignore unreachable sourcemap
    }
  }

  await page.setViewportSize({ width: 1920, height: 1080 });
  const wideOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth
  );

  await page.setViewportSize({ width: 1440, height: 900 });
  const desktopOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth
  );

  const layoutChecks = await page.evaluate(() => {
    const footer = document.querySelector("footer");
    let floatingFooter = false;
    let footerGapPx = 0;
    if (footer) {
      const rect = footer.getBoundingClientRect();
      const gap = Math.round(window.innerHeight - rect.bottom);
      if (rect.height > 0 && gap > 40) {
        floatingFooter = true;
        footerGapPx = gap;
      }
    }

    const unsafeFormLinks = [];
    for (const form of document.querySelectorAll("form")) {
      for (const a of form.querySelectorAll("a[href]")) {
        const href = a.getAttribute("href") || "";
        const target = (a.getAttribute("target") || "").toLowerCase();
        if (!href.startsWith("#") && !href.startsWith("mailto:") && target !== "_blank") {
          unsafeFormLinks.push({
            href,
            text: (a.textContent || "").trim().slice(0, 80),
          });
        }
      }
    }

    return { floatingFooter, footerGapPx, unsafeFormLinks };
  });

  await page.setViewportSize({ width: 768, height: 1024 });
  const tabletOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth
  );

  await page.setViewportSize({ width: 390, height: 844 });
  const mobileOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth
  );

  const screenshots = [];
  if (screenshotsDir) {
    const resolvedDir = path.resolve(screenshotsDir);
    fs.mkdirSync(resolvedDir, { recursive: true });
    const slug = sanitizeRouteSlug(routePath);
    const schemes = colorScheme === "both" ? ["light", "dark"] : [colorScheme];

    for (const scheme of schemes) {
      await page.emulateMedia({ colorScheme: scheme });
      for (const vp of SCREENSHOT_VIEWPORTS) {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.waitForTimeout(200);
        const prefix = `${slug}-${vp.name}-${scheme}`;
        const foldPath = path.join(resolvedDir, `${prefix}-fold.png`);
        const fullPath = path.join(resolvedDir, `${prefix}-full.png`);
        await page.screenshot({ path: foldPath, fullPage: false });
        await page.screenshot({ path: fullPath, fullPage: true });
        screenshots.push(
          { viewport: vp.name, colorScheme: scheme, kind: "above-the-fold", path: foldPath },
          { viewport: vp.name, colorScheme: scheme, kind: "full-page", path: fullPath }
        );
      }
    }
    await page.emulateMedia({ colorScheme: null });
  }

  await page.setViewportSize({ width: 1440, height: 900 });

  const missingHeaders = RECOMMENDED_HEADERS.filter((h) => !(h in documentHeaders));
  const hasFrameProtection =
    "x-frame-options" in documentHeaders ||
    (documentHeaders["content-security-policy"] || "").includes("frame-ancestors");
  if (!hasFrameProtection) missingHeaders.push("x-frame-options_or_csp_frame-ancestors");
  if (finalUrl.startsWith("https:") && !("strict-transport-security" in documentHeaders)) {
    missingHeaders.push("strict-transport-security");
  }

  const cookies = (await context.cookies(finalUrl)).map((c) => ({
    name: c.name,
    httpOnly: c.httpOnly,
    secure: c.secure,
    sameSite: c.sameSite,
  }));

  const storageInspection = await page.evaluate(() => {
    const inspect = (store) => {
      const keys = [];
      for (let i = 0; i < store.length; i += 1) {
        const k = store.key(i);
        const suspicious = /token|jwt|auth|secret|key|pass/i.test(k || "");
        keys.push({ key: k, suspiciousName: suspicious });
      }
      return keys;
    };
    return {
      localStorage: inspect(window.localStorage),
      sessionStorage: inspect(window.sessionStorage),
    };
  });

  const formsInventory = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("form")).map((form, idx) => ({
      index: idx,
      id: form.getAttribute("id") || "",
      name: form.getAttribute("name") || "",
      ariaLabel: form.getAttribute("aria-label") || "",
      headingText: Array.from(form.querySelectorAll("legend, h1, h2, h3, h4"))
        .map((h) => (h.textContent || "").trim())
        .join(" | ")
        .slice(0, 120),
      action: form.getAttribute("action") || "(current)",
      method: (form.getAttribute("method") || "GET").toUpperCase(),
      submitText: Array.from(form.querySelectorAll('button, input[type="submit"]'))
        .map((b) => (b.textContent || b.value || "").trim())
        .join(" | ")
        .slice(0, 120),
      fields: Array.from(form.querySelectorAll("input, textarea, select")).map((el) => ({
        name: el.getAttribute("name") || el.getAttribute("id") || "(unnamed)",
        type: el.getAttribute("type") || el.tagName.toLowerCase(),
        required: el.hasAttribute("required"),
      })),
    }));
  });

  let axeSummary = { available: false, violations: [] };
  try {
    const axeMod = await loadOptionalModule("@axe-core/playwright");
    const AxeBuilder = axeMod.AxeBuilder || axeMod.default?.AxeBuilder || axeMod.default;
    if (AxeBuilder) {
      const axeResults = await new AxeBuilder({ page }).analyze();
      axeSummary = {
        available: true,
        violations: axeResults.violations.map((v) => ({
          id: v.id,
          impact: v.impact,
          nodes: v.nodes.length,
          help: v.help,
        })),
      };
    }
  } catch {
    // Optional dependency not installed
  }

  const formProbeResults = [];
  const skippedRiskyForms = [];
  let formsTruncatedByCap = false;

  if (probeForms && formsInventory.length > 0) {
    let probedCount = 0;
    for (const formMeta of formsInventory) {
      const riskyText = [
        formMeta.action,
        formMeta.id,
        formMeta.name,
        formMeta.ariaLabel,
        formMeta.headingText,
        formMeta.submitText,
      ].join(" ");
      if (!includeRisky && RISKY_FORM_PATTERN.test(riskyText)) {
        skippedRiskyForms.push({
          index: formMeta.index,
          action: formMeta.action,
          submitText: formMeta.submitText,
        });
        continue;
      }
      if (probedCount >= maxForms) {
        formsTruncatedByCap = true;
        break;
      }
      probedCount += 1;

      for (const probe of SAFE_FORM_PROBES) {
        const probePage = await context.newPage();
        let dialogTriggered = false;
        let probe500s = 0;
        const probeSqlHits = [];
        const probePending = [];

        probePage.on("dialog", async (dialog) => {
          dialogTriggered = true;
          await dialog.dismiss().catch(() => {});
        });
        probePage.on("response", (res) => {
          if (res.status() >= 500) probe500s += 1;
          const ct = (res.headers()["content-type"] || "").toLowerCase();
          if (ct.includes("json") || ct.includes("html") || ct.includes("text")) {
            probePending.push(
              res
                .text()
                .then((txt) => {
                  probeSqlHits.push(...checkTextSignatures(txt.slice(0, 30000)));
                })
                .catch(() => {})
            );
          }
        });

        await probePage.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 20000 });
        // Línea base: evita falso positivo si la página ya contiene <b>probe</b> legítimo.
        const hadBoldProbeBefore = await probePage.evaluate(() =>
          Array.from(document.querySelectorAll("b")).some((b) => b.textContent === "probe")
        );
        await probePage.evaluate(
          ({ fIndex, val }) => {
            const form = document.querySelectorAll("form")[fIndex];
            if (!form) return;
            form.setAttribute("novalidate", "true");
            const inputSetter = Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,
              "value"
            )?.set;
            const textareaSetter = Object.getOwnPropertyDescriptor(
              window.HTMLTextAreaElement.prototype,
              "value"
            )?.set;

            for (const el of form.querySelectorAll("input, textarea")) {
              const t = (el.getAttribute("type") || "text").toLowerCase();
              if (["hidden", "submit", "button", "checkbox", "radio", "file"].includes(t)) continue;
              el.removeAttribute("maxlength");
              el.removeAttribute("pattern");
              const nextVal = t === "email" ? `${val}@example.com` : val;
              if (el.tagName === "TEXTAREA" && textareaSetter) {
                textareaSetter.call(el, nextVal);
              } else if (inputSetter) {
                inputSetter.call(el, nextVal);
              } else {
                el.value = nextVal;
              }
              el.dispatchEvent(new Event("input", { bubbles: true }));
              el.dispatchEvent(new Event("change", { bubbles: true }));
            }
          },
          { fIndex: formMeta.index, val: probe.value }
        );

        const submitBtn = probePage
          .locator("form")
          .nth(formMeta.index)
          .locator('button[type="submit"], input[type="submit"], button:not([type])')
          .first();

        if (await submitBtn.count()) {
          await submitBtn.click({ timeout: 5000 }).catch(() => {});
          await probePage.waitForTimeout(800);
        }

        await Promise.allSettled(probePending);

        const xssExecuted = await probePage.evaluate(() => Boolean(window.__auditXssTriggered));
        const unescapedTag =
          !hadBoldProbeBefore &&
          (await probePage.evaluate(() => {
            return Array.from(document.querySelectorAll("b")).some((b) => b.textContent === "probe");
          }));

        if (dialogTriggered || xssExecuted || unescapedTag || probe500s > 0 || probeSqlHits.length > 0) {
          formProbeResults.push({
            formIndex: formMeta.index,
            probe: probe.name,
            dialogTriggered,
            xssExecuted,
            unescapedHtmlInDom: unescapedTag,
            http500Count: probe500s,
            leakSignatures: [...new Set(probeSqlHits)],
          });
        }
        await probePage.close();
      }
    }
  }

  await page.close();
  return {
    route: routePath,
    url: redactUrl(targetUrl),
    finalUrl: redactUrl(finalUrl),
    mainStatus,
    consoleErrors,
    pageErrors,
    failedRequests,
    httpErrors,
    bodyLeakHits,
    sourcemapsExposed: [...sourcemapsExposed],
    missingSecurityHeaders: missingHeaders,
    cookies,
    storageInspection,
    responsiveOverflow: { wide: wideOverflow, desktop: desktopOverflow, tablet: tabletOverflow, mobile: mobileOverflow },
    layoutChecks,
    screenshots,
    formsCount: formsInventory.length,
    formsInventory,
    axe: axeSummary,
    formProbeFindings: formProbeResults,
    skippedRiskyForms,
    formsTruncatedByCap,
  };
}

async function main() {
  const opts = parseArgs(process.argv);

  let parsed;
  try {
    parsed = new URL(opts.url);
  } catch {
    console.error(`Error: URL invalida "${opts.url}". Usa un formato completo como http://localhost:3000.\n\n${USAGE}`);
    process.exit(1);
  }

  if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
    console.error(
      `Refusing to audit unsupported protocol "${parsed.protocol}". Only http: and https: URLs are allowed.`
    );
    process.exit(2);
  }

  if (!isLocalHostname(parsed.hostname) && !opts.allowRemote) {
    console.error(
      `Refusing to run browser audit against non-local host "${parsed.hostname}" without --allow-remote.`
    );
    process.exit(2);
  }

  let chromium;
  try {
    const pwMod = await loadOptionalModule("playwright");
    chromium = pwMod.chromium || pwMod.default?.chromium;
    if (!chromium) throw new Error("playwright chromium export not found");
  } catch {
    console.error(
      'Playwright is not installed in the current project or Node path. Install with "npm i -D playwright" or run via your Playwright environment.'
    );
    process.exit(3);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ ignoreHTTPSErrors: isLocalHostname(parsed.hostname) });
  const results = [];

  try {
    for (const r of opts.routes) {
      results.push(
        await auditRoute(context, opts.url, r, {
          probeForms: opts.probeForms,
          includeRisky: opts.includeRisky,
          maxForms: opts.maxForms,
          screenshotsDir: opts.screenshotsDir,
          colorScheme: opts.colorScheme,
        })
      );
    }
  } finally {
    await browser.close();
  }

  const summary = {
    target: redactUrl(opts.url),
    probedForms: opts.probeForms,
    routes: results,
  };
  if (opts.outFile) {
    const resolvedOut = path.resolve(opts.outFile);
    fs.mkdirSync(path.dirname(resolvedOut), { recursive: true });
    fs.writeFileSync(resolvedOut, JSON.stringify(summary, null, 2), "utf8");
  }

  console.log(`# Browser Security & QA Audit: ${redactUrl(opts.url)}`);
  for (const r of results) {
    console.log(`\n## Ruta ${r.route} (HTTP ${r.mainStatus ?? "?"} -> ${r.finalUrl})`);
    console.log(`- Errores consola: ${r.consoleErrors.length} | Excepciones JS: ${r.pageErrors.length}`);
    console.log(`- Peticiones fallidas: ${r.failedRequests.length} | Respuestas >=400: ${r.httpErrors.length}`);
    console.log(`- Fugas SQL/Stack en respuestas: ${r.bodyLeakHits.length} | Sourcemaps expuestos: ${r.sourcemapsExposed.length}`);
    console.log(
      `- Headers de seguridad faltantes: ${
        r.missingSecurityHeaders.join(", ") || "Ninguno basico faltante (revisar directivas CSP/HSTS)"
      }`
    );
    console.log(
      `- Overflow horizontal: wide=${r.responsiveOverflow.wide}, desktop=${r.responsiveOverflow.desktop}, tablet=${r.responsiveOverflow.tablet}, mobile=${r.responsiveOverflow.mobile}`
    );
    if (r.layoutChecks.floatingFooter) {
      console.log(
        `- ALERTA UX/Layout: footer flotando (${r.layoutChecks.footerGapPx}px vacios debajo en 1440x900; usa min-height: 100dvh + flex-column).`
      );
    }
    if (r.layoutChecks.unsafeFormLinks.length) {
      console.log(
        `- ALERTA UX Formularios: ${r.layoutChecks.unsafeFormLinks.length} enlace(s) dentro de <form> sin target="_blank" (pueden borrar progreso del usuario).`
      );
    }
    if (r.screenshots.length) {
      console.log(`- Capturas visuales guardadas (${r.screenshots.length}): ${path.resolve(opts.screenshotsDir)}`);
    }
    console.log(`- Formularios detectados: ${r.formsCount} | Hallazgos en sondas activas: ${r.formProbeFindings.length}`);
    if (r.skippedRiskyForms.length) {
      console.log(
        `- Formularios omitidos por ser de riesgo (borrado/pago/logout): ${r.skippedRiskyForms.length} (usa --include-risky-forms con datos de prueba)`
      );
    }
    if (r.formsTruncatedByCap) {
      console.log(`- Aviso: se alcanzo el limite --max-forms (${opts.maxForms}) en esta ruta.`);
    }
    if (r.axe.available) {
      console.log(`- Violaciones axe-core (A11y): ${r.axe.violations.length}`);
    }
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
