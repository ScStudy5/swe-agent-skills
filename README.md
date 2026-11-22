# Software Engineering Agent Skills (`swe-*`)

Colección de **14 skills modulares e independientes** de buenas prácticas de ingeniería de software, calibradas para llevar proyectos desde **1. MVP**, pasando por **2. Profesional (miles de usuarios)** hasta **3. Empresarial**, con seguridad fuerte, flujo GitHub completo, cumplimiento legal base, flujo ordenado con agentes IA, dirección visual/oficio UI, pruebas en vivo y entrega formal (*handover*).

Escritas bajo el estándar abierto **Agent Skills (`SKILL.md`)**, compatibles con **Antigravity**, **Claude Code**, **OpenAI Codex**, **Cursor**, **OpenCode** y **Gemini CLI**.

---

## Skills incluidas (14)

| Skill | Área que cubre | Cuándo usarla |
| :--- | :--- | :--- |
| `swe-methodology` | Metodología base, selector de nivel (`1. MVP / 2. Profesional / 3. Empresarial`), **ciclo de lanzamiento en 5 etapas**, **3 reglas innegociables**, perfiles por producto (`product-profiles.md`), integración con `modern-web-guidance`/`Context7`, documentación (`examples/`), **Pre-Production Release Checklist (`0/57`) + matriz Go/No-Go** (`audit-checklist.md`), diagnóstico rápido (`scripts/repo_audit_scan.py`) y normas ISO/OWASP/NIST | Al arrancar un proyecto, definir alcance/estándares, crear documentación o realizar auditorías de pre-lanzamiento |
| `swe-domain-discovery` | Descubrimiento independiente de brechas por industria y país (fintech/banca, salud, gobierno, videojuegos, e-commerce, menores, IoT): qué desarrollar en código vs. qué licencias/normas/auditorías externas faltan | Al plantear un proyecto de un sector específico y descubrir requisitos fuera de las buenas prácticas generales |
| `swe-browser-audit` | Auditoría dinámica y visual en navegador real con Playwright (`scripts/playwright_security_audit.mjs`): consola, red, frontend, Security Headers, cookies, storage, sourcemaps, capturas PNG (`desktop`/`tablet`/`mobile`, `light`/`dark`) para crítica visual, validación de campos, XSS, sondas seguras de SQLi/NoSQLi, IDOR/CSRF, `axe-core` y responsive | Para probar en vivo una app en `localhost` o `staging` autorizado buscando errores, vulnerabilidades y defectos visuales |
| `swe-architecture-design` | Arquitectura, SOLID/DRY/KISS/YAGNI, Clean Architecture, DDD, patrones de resiliencia (Circuit Breaker/Bulkhead), portabilidad (sin Vendor Lock-in), calidad de código, linting y refactoring | Al diseñar arquitectura, crear ADRs o auditar estructura y calidad del código |
| `swe-security-privacy` | DevSecOps, SSDLC, Threat Modeling, OWASP Top 10/ASVS, autenticación/sesiones (anti-enumeración, revocación, MFA), autorización (**IDOR/BOLA**), **Row Level Security (RLS/BaaS)**, cifrado, privacidad (ARCO/LFPDPPP), licencias OSS/PI y cadena de suministro (SBOM/SCA) | Al diseñar flujos sensibles, revisar vulnerabilidades/RLS, gestionar secretos/dependencias/licencias o validar privacidad |
| `swe-qa-testing` | Estrategia de pruebas, pirámide de testing, 25 tipos de pruebas (Unit, Integration, E2E, Contract, Load, Security, Mutation, Fuzz, Chaos, LLM Evals, etc.) e higiene previa a producción (*Release Hygiene*) | Al definir estrategia QA, auditar suite de pruebas, validar higiene de release o escribir planes y casos de prueba |
| `swe-ui-craft` | Dirección visual anti-genérica y *Design Engineering* en 4 micro-guías por tarea: exploración visual (tesis visual + 3 direcciones distintas antes de codificar), tipografía/composición guiada por contenido (`100dvh` sticky footer, *code splitting*), movimiento/microinteracciones (estilo Emil Kowalski) y crítica visual de identidad sobre capturas reales de Playwright | Al definir la identidad visual de una interfaz, diseñar/rediseñar pantallas, ajustar animaciones o auditar calidad estética |
| `swe-ux-accessibility` | Estrategia UX (investigación con usuarios, *User Flows*, 10 heurísticas de Nielsen), diseño responsive (Mobile First, 4 estados de UI, preservación de formularios, `ErrorBoundary` + vistas `400`/`403`/`404`/`500`/`503`), accesibilidad WCAG 2.2 AA / WAI-ARIA, SEO público, RUM/analítica ética, compatibilidad e i18n/l10n | Al investigar flujos UX, construir formularios/estados, auditar accesibilidad, configurar SEO público o localización |
| `swe-data-apis` | Diseño de BD, normalización, **RLS y permisos de Storage**, concurrencia/pagos/webhooks/DLQ, migraciones compatibles hacia atrás, RTO/RPO, backups (*off-site* + restauración probada), REST/OpenAPI, Problem Details (RFC 9457) y rendimiento | Al modelar bases de datos, revisar RLS/backups, diseñar APIs/pagos y resolver cuellos de botella o consultas N+1 |
| `swe-devops-operations` | Git (GitHub Flow / Trunk-Based / Git Flow, Conventional Commits, Rulesets/`gh CLI`), CI/CD endurecido por SHA (CI, CD con Environments/OIDC, Releases SemVer, CodeQL, Dependabot, validación PRs, `CODEOWNERS`, `.gitattributes`, Issue Forms), Docker/IaC/Kubernetes, protección perimetral (**DDoS/bots/WAF**), incidentes/postmortem, observabilidad (Sentry, Uptime Kuma, Grafana), DORA y FinOps (topes duros y *kill switch*) | Al configurar repositorios GitHub, pipelines CI/CD, contenedores, despliegues, monitoreo, protección de tráfico y costos en nube |
| `swe-ai-engineering` | Seguridad y gobernanza de IA/LLMs en producto (NIST AI RMF, ISO 42001), prompt injection, alucinaciones, sesgos, Human-in-the-loop, versionado de prompts/modelos, evals, **protección contra bucles recursivos/iteraciones/concurrencia en agentes** y topes estrictos de costos | Al diseñar, auditar o probar funciones de producto con LLMs, RAG, agentes o tool calling |
| `swe-project-handover` | Paquete integral de Software Project Handover y Documentación Viva (`PROJECT-HANDOVER/00-START-HERE` a `17-APPENDICES` + Regla 18): contexto ejecutivo, guía de código, memoria histórica/deuda, licencias/PI, manuales diferenciados, inventario, transferencia/revocación de accesos, sesiones supervisadas, acta de entrega y `scripts/handover_scaffold.py` | Al preparar la entrega formal de un proyecto, onboarding de sucesores o auditar completitud documental |
| `swe-legal-compliance` | Marco de Cumplimiento Legal y Regulatorio (LCS — 13 pilares + checklist `Legal Launch Readiness 0/36` + matriz adaptable de páginas públicas/confianza y footer por proyecto): borradores base (Aviso de Privacidad integral/simplificado LFPDPPP, Términos y Condiciones, Cookies, PROFECO/LFPC arts. 76 Bis y 76 Bis 1, Accesibilidad, Seguridad/`security.txt`, Subprocesadores y Política de IA condicional), PI (INDAUTOR/IMPI, coautores), contratos B2B (EULA, SaaS, NDA, DPA, SLA), SAT/CFDI, evidencia NOM-151, controles técnico-legales y `scripts/legal_readiness_check.py` | Al generar borradores legales a la medida de cada proyecto, definir qué páginas públicas/footer aplican, implementar controles técnico-legales (ARCO/consentimiento/log versionado) o evaluar preparación legal de lanzamiento |
| `swe-ai-workflow` | Context Engineering, ahorro radical de tokens y control de *vibe coding*: genera y audita `CONSTITUTION.md`, `AGENTS.md` (con puentes a `CLAUDE.md`/`GEMINI.md`/`.cursor/rules/`), `.ai/MEMORY.md`, `.ai/TASK_SPEC.md`, lectura selectiva, script antes que LLM, lotes pequeños verificados, regla de 2 intentos y `scripts/ai_context_kit.py` | Al configurar un repositorio para programar con agentes IA, reducir gasto de tokens o estructurar prompts vagos de *vibe coding* |

---

## Instalación

Puedes instalar **todas las 14 skills** o copiar únicamente las carpetas `swe-*` que necesites.

### Opción 1 — Instalación rápida con `skills` CLI (recomendado)

```bash
# Instalar todas las skills del repositorio
npx skills add ScStudy5/swe-agent-skills

# O instalar solo una skill específica
npx skills add ScStudy5/swe-agent-skills --skill swe-ai-workflow
```

### Opción 2 — Instalación por proyecto (`.agents/skills/`, estándar compartido)

Ideal para compartir las mismas skills con todo el equipo dentro del repositorio (compatible con Antigravity, Codex, OpenCode y herramientas compatibles con `.agents/skills/`):

**Linux / macOS (Bash):**
```bash
git clone --depth 1 https://github.com/ScStudy5/swe-agent-skills.git /tmp/swe-agent-skills
mkdir -p .agents/skills
cp -r /tmp/swe-agent-skills/swe-* .agents/skills/
rm -rf /tmp/swe-agent-skills
```

**Windows (PowerShell):**
```powershell
git clone --depth 1 https://github.com/ScStudy5/swe-agent-skills.git "$env:TEMP\swe-agent-skills"
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force "$env:TEMP\swe-agent-skills\swe-*" ".agents\skills\"
Remove-Item -Recurse -Force "$env:TEMP\swe-agent-skills"
```

### Opción 3 — Instalación global por herramienta

Copia las carpetas `swe-*` en la carpeta global de tu agente:

| Herramienta | Ruta global de skills | Ruta por proyecto |
| :--- | :--- | :--- |
| **Antigravity** | `~/.gemini/config/skills/` | `<proyecto>/.agents/skills/` |
| **Claude Code** | `~/.claude/skills/` | `<proyecto>/.claude/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `<proyecto>/.agents/skills/` |
| **Cursor** | `~/.cursor/skills/` | `<proyecto>/.cursor/skills/` o `.agents/skills/` |
| **OpenCode / Gemini CLI** | `~/.config/opencode/skills/` | `<proyecto>/.agents/skills/` |

### Verificación rápida tras instalar

1. Reinicia o abre una nueva sesión de tu agente y pregúntale: *"¿Qué skills `swe-*` tienes disponibles?"*.
2. (Opcional) Comprueba los scripts auxiliares (Python 3 estándar; Node.js + Playwright solo para `swe-browser-audit`):
   ```bash
   python3 .agents/skills/swe-methodology/scripts/repo_audit_scan.py .
   python3 .agents/skills/swe-ai-workflow/scripts/ai_context_kit.py audit .
   node .agents/skills/swe-browser-audit/scripts/playwright_security_audit.mjs http://localhost:3000 \
     --routes /,/login --screenshots-dir .audit-screenshots --out audit-report.json
   ```

---

## Principio de aplicación proporcional y compuerta de lanzamiento

No todas las prácticas aplican por igual a todos los proyectos. Todas las skills clasifican el proyecto en tres niveles antes de exigir controles:

1. **Nivel 1 — MVP sólido:** entrega rápida sin deuda tóxica y preparada para escalar (arquitectura clara, validación en servidor, secretos fuera del repo, tests críticos, HTTPS).
2. **Nivel 2 — Producción pequeña/mediana (miles de usuarios / SaaS / App en vivo):** CI/CD endurecido con linters y tests completos, resiliencia (timeouts/retries/idempotencia), RLS y backups con restauración probada, WCAG 2.2 AA + crítica visual con Playwright, SEO público, monitoreo de errores, topes de costos en nube/IA (FinOps) y auditorías periódicas.
3. **Nivel 3 — Empresarial / Regulado:** Threat Modeling formal, gobernanza (RACI/SRS/BPMN/DAMA-DMBOK), cumplimiento ISO/OWASP ASVS/NIST SSDF, SLSA/Sigstore, ITIL 4, Chaos/Load testing y observabilidad distribuida.

### 3 Reglas innegociables antes de publicar (cualquier nivel)
1. **Ningún secreto ni dato privado puede quedar expuesto** (código, frontend, repositorio, logs, BD/RLS o storage).
2. **Ningún servicio de pago puede operar sin límites de consumo y controles de costos adecuados** (topes duros/límites de ejecución/cuotas; no confundir alertas con topes).
3. **Ninguna aplicación puede publicarse sin revisar sus obligaciones de seguridad y cumplimiento legal** aplicables (checklist maestro `0/57` + matriz `Go/No-Go` en `swe-methodology/examples/audit-checklist.md`).

---

## Licencia

Distribuido bajo la licencia **Apache-2.0**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
