#!/usr/bin/env python3
"""AI Workflow & Context Engineering kit (`init` & `audit`).

Zero external dependencies (Python standard library only).
- `init`: inspects repository manifests to auto-detect real build/test/lint commands
  and scaffolds compact, token-efficient context files (`CONSTITUTION.md`, `AGENTS.md`,
  `.ai/MEMORY.md`, `.ai/TASK_SPEC.md`) plus optional thin bridges (`CLAUDE.md`,
  `GEMINI.md`, `.cursor/rules/00-project-context.mdc`). Never overwrites without `--force`.
- `audit` (read-only): checks presence, enforces line/token budgets to prevent context
  bloat, counts unfilled placeholders, and blocks accidental secrets or `.env` files
  inside AI context files (never prints secret values).

Exit codes:
  0 = success (and 0 critical security blockers in `audit`)
  1 = CLI argument / path error
  2 = critical security blocker found in `audit` (.env or secret inside AI context files)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "dist", "build", "out",
    "target", "bin", "obj", ".next", ".nuxt", "__pycache__", ".pytest_cache",
    "coverage", ".dart_tool", ".idea", ".vscode",
}

ENV_SAFE_SUFFIXES = (".example", ".sample", ".template")

SECRET_PATTERNS = [
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("aws_access_key_id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github_pat", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("openai_like_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "hardcoded_secret_assignment",
        re.compile(
            r"""(?i)\b(?:api_key|apikey|secret_key|client_secret|db_password|password)\b\s*[:=]\s*["'][^"'\s]{10,}["']"""
        ),
    ),
]

PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:TODO|PENDIENTE|COMPLETAR|YYYY-MM-DD|<git-sha>|Ej\.[^\]]*|Nombre[^\]]*|"
    r"Descripción[^\]]*|Tarea[^\]]*|ruta/[^\]]*|Qué [^\]]*)\]",
    re.IGNORECASE,
)

LINE_BUDGETS = {
    "CONSTITUTION.md": 80,
    "AGENTS.md": 100,
    ".ai/MEMORY.md": 100,
    "MEMORY.md": 100,
    ".ai/TASK_SPEC.md": 50,
    "TASK_SPEC.md": 50,
    "CLAUDE.md": 20,
    "GEMINI.md": 20,
    ".cursor/rules/00-project-context.mdc": 20,
}

VALID_BRIDGES = {"claude", "gemini", "cursor"}
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def is_sensitive_env_name(filename: str) -> bool:
    lower = filename.lower()
    if not (lower == ".env" or lower.startswith(".env.")):
        return False
    return not lower.endswith(ENV_SAFE_SUFFIXES)


def detect_repo_commands(root: Path) -> dict[str, str]:
    """Detect real stack & build/lint/test commands from repository manifests."""
    cmds = {
        "install": "`[Definir comando de instalación]`",
        "dev": "`[Definir comando de desarrollo local]`",
        "lint": "`[Definir comando de lint/formato]`",
        "typecheck_build": "`[Definir comando de typecheck/build]`",
        "test": "`[Definir comando de tests rápidos]`",
    }

    pkg_path = root / "package.json"
    if pkg_path.is_file() and not pkg_path.is_symlink():
        pm = "npm"
        if (root / "pnpm-lock.yaml").is_file():
            pm = "pnpm"
        elif (root / "yarn.lock").is_file():
            pm = "yarn"
        elif (root / "bun.lockb").is_file() or (root / "bun.lock").is_file():
            pm = "bun"

        run_prefix = f"{pm} run " if pm == "npm" else f"{pm} "
        cmds["install"] = f"`{pm} ci`" if pm == "npm" else f"`{pm} install --frozen-lockfile`"
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8", errors="ignore"))
            scripts = pkg.get("scripts", {}) if isinstance(pkg, dict) else {}
            if isinstance(scripts, dict):
                if "dev" in scripts:
                    cmds["dev"] = f"`{run_prefix}dev`"
                elif "start" in scripts:
                    cmds["dev"] = f"`{run_prefix}start`"
                if "lint" in scripts:
                    cmds["lint"] = f"`{run_prefix}lint`"
                tc_parts = []
                if "typecheck" in scripts:
                    tc_parts.append(f"{run_prefix}typecheck")
                if "build" in scripts:
                    tc_parts.append(f"{run_prefix}build")
                if tc_parts:
                    cmds["typecheck_build"] = f"`{' && '.join(tc_parts)}`"
                if "test" in scripts:
                    cmds["test"] = f"`{pm} test`"
        except (OSError, json.JSONDecodeError):
            pass
        return cmds

    if (root / "pyproject.toml").is_file() or (root / "requirements.txt").is_file():
        cmds["install"] = "`uv sync --frozen`" if (root / "uv.lock").is_file() else "`pip install -r requirements.txt`"
        cmds["lint"] = "`ruff check .`"
        cmds["typecheck_build"] = "`mypy .`"
        cmds["test"] = "`pytest -q`"
        return cmds

    if (root / "go.mod").is_file():
        cmds["install"] = "`go mod download`"
        cmds["lint"] = "`golangci-lint run`"
        cmds["typecheck_build"] = "`go build ./...`"
        cmds["test"] = "`go test ./...`"
        return cmds

    if (root / "Cargo.toml").is_file():
        cmds["install"] = "`cargo fetch`"
        cmds["lint"] = "`cargo clippy --all-targets`"
        cmds["typecheck_build"] = "`cargo build`"
        cmds["test"] = "`cargo test`"
        return cmds

    if list(root.glob("*.sln")) or list(root.glob("*.csproj")):
        cmds["install"] = "`dotnet restore`"
        cmds["lint"] = "`dotnet format --verify-no-changes`"
        cmds["typecheck_build"] = "`dotnet build --no-restore`"
        cmds["test"] = "`dotnet test --no-build`"
        return cmds

    return cmds


def list_top_dirs(root: Path) -> list[str]:
    dirs: list[str] = []
    try:
        for child in sorted(root.iterdir()):
            if child.is_dir() and not child.is_symlink() and child.name not in IGNORED_DIRS:
                dirs.append(child.name)
    except OSError:
        pass
    return dirs[:10]


def render_agents_md(root: Path, project_name: str) -> str:
    cmds = detect_repo_commands(root)
    top_dirs = list_top_dirs(root)
    tree_lines = ["."]
    for idx, d in enumerate(top_dirs):
        branch = "└──" if idx == len(top_dirs) - 1 else "├──"
        tree_lines.append(f"{branch} {d}/")
    if not top_dirs:
        tree_lines.append("└── src/          # [Código principal]")

    tree_block = "\n".join(tree_lines)
    return (
        f"# AGENTS — Mapa Operativo de {project_name}\n\n"
        "> Fuente única de contexto operativo para agentes de IA. **Mantener ≤ 100 líneas.**\n"
        "> Lee también [CONSTITUTION.md](./CONSTITUTION.md) (reglas innegociables) y "
        "[.ai/MEMORY.md](./.ai/MEMORY.md) (estado y aprendizajes recientes).\n\n"
        "## 1. Propósito del proyecto\n"
        "`[Descripción de 2–3 líneas del sistema y usuarios principales.]`\n\n"
        "## 2. Mapa compacto de carpetas\n"
        f"```text\n{tree_block}\n```\n\n"
        "## 3. Comandos reales (ejecutar en lugar de adivinar)\n"
        f"- **Instalar:** {cmds['install']}\n"
        f"- **Desarrollo local:** {cmds['dev']}\n"
        f"- **Lint / Formato:** {cmds['lint']}\n"
        f"- **Typecheck / Build:** {cmds['typecheck_build']}\n"
        f"- **Tests rápidos (tras cada lote):** {cmds['test']}\n\n"
        "## 4. Convenciones y flujo obligatorio\n"
        "- **Plan corto:** ante cambios ambiguos o >2 archivos, presenta plan de 3–5 líneas antes de editar.\n"
        "- **Lectura selectiva:** busca primero con `rg`/grep y lee rangos acotados; evita volcar logs masivos.\n"
        "- **Script antes que LLM:** corre lint/typecheck/tests antes de pedir revisión general a la IA.\n"
        "- **Regla de 2 intentos:** si un bug falla 2 veces, frena el parcheo ciego, diagnostica causa raíz y anota lo fallido en `.ai/MEMORY.md`.\n"
        "- **Cierre de sesión:** actualiza `.ai/MEMORY.md` y trabaja bajo el esquema `1 tarea = 1 sesión` usando `.ai/TASK_SPEC.md`.\n"
    )


def render_bridge(kind: str) -> tuple[str, str]:
    if kind == "claude":
        return (
            "CLAUDE.md",
            "# Project Instructions (Claude Code Bridge)\n\n"
            "Source of truth for this repository:\n"
            "- Read `AGENTS.md` for architecture map, real build/test/lint commands, and workflow.\n"
            "- Follow all non-negotiable rules in `CONSTITUTION.md`.\n"
            "- Check `.ai/MEMORY.md` before starting and update it before ending the session.\n",
        )
    if kind == "gemini":
        return (
            "GEMINI.md",
            "# Project Instructions (Gemini / Antigravity Bridge)\n\n"
            "Source of truth for this repository:\n"
            "- Read `AGENTS.md` for architecture map, real build/test/lint commands, and workflow.\n"
            "- Follow all non-negotiable rules in `CONSTITUTION.md`.\n"
            "- Check `.ai/MEMORY.md` before starting and update it before ending the session.\n",
        )
    return (
        ".cursor/rules/00-project-context.mdc",
        "---\n"
        "description: Core repository rules, commands, and living AI memory\n"
        "alwaysApply: true\n"
        "---\n\n"
        "Read and follow:\n"
        "1. `CONSTITUTION.md` — non-negotiable rules, protected zones, and quality gates.\n"
        "2. `AGENTS.md` — repository map and exact build/lint/typecheck/test commands.\n"
        "3. `.ai/MEMORY.md` — current status, resolved bugs, and failed approaches to avoid repeating.\n",
    )


def load_example(name: str, project_name: str) -> str:
    raw = (EXAMPLES_DIR / name).read_text(encoding="utf-8")
    today = dt.date.today().isoformat()
    return raw.replace("[Nombre del Proyecto]", project_name).replace("[YYYY-MM-DD]", today, 1)


def run_init(root: Path, project_name: str, bridges: list[str], dry_run: bool, force: bool) -> int:
    if not root.is_dir():
        print(f"Error: directory not found: {root}", file=sys.stderr)
        return 1

    plan: list[tuple[str, str]] = [
        ("CONSTITUTION.md", load_example("CONSTITUTION.md", project_name)),
        ("AGENTS.md", render_agents_md(root, project_name)),
        (".ai/MEMORY.md", load_example("MEMORY.md", project_name)),
        (".ai/TASK_SPEC.md", load_example("TASK_SPEC.md", project_name)),
    ]
    for b in bridges:
        plan.append(render_bridge(b))

    created = 0
    skipped = 0
    overwritten = 0

    for rel, content in plan:
        dest = root / rel
        exists = dest.exists()
        if exists and not force:
            skipped += 1
            action = "SKIP_EXISTS"
        elif exists and force:
            overwritten += 1
            action = "OVERWRITE"
        else:
            created += 1
            action = "CREATE"

        if dry_run:
            print(f"[DRY-RUN] {action}: {rel}")
            continue
        if action == "SKIP_EXISTS":
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)

    mode = "DRY-RUN" if dry_run else "COMPLETADO"
    print(
        f"\n[{mode}] AI Context Kit en `{root}`: "
        f"creados={created}, sobrescritos={overwritten}, omitidos_existentes={skipped}"
    )
    return 0


def run_audit(root: Path, output_format: str, max_findings: int) -> int:
    if not root.is_dir():
        print(f"Error: directory not found: {root}", file=sys.stderr)
        return 1

    memory_rel = ".ai/MEMORY.md" if (root / ".ai/MEMORY.md").is_file() else "MEMORY.md"
    spec_rel = ".ai/TASK_SPEC.md" if (root / ".ai/TASK_SPEC.md").is_file() else "TASK_SPEC.md"
    core_files = ["CONSTITUTION.md", "AGENTS.md", memory_rel, spec_rel]
    bridge_files = ["CLAUDE.md", "GEMINI.md", ".cursor/rules/00-project-context.mdc"]

    present_core: list[str] = []
    missing_core: list[str] = []
    present_bridges: list[str] = []
    file_metrics: list[dict[str, object]] = []
    budget_warnings: list[str] = []
    placeholder_files: list[dict[str, object]] = []
    env_files_found: list[str] = []
    secret_findings: list[dict[str, object]] = []
    secret_findings_truncated = False

    files_to_inspect: list[str] = []
    for rel in core_files:
        p = root / rel
        if p.is_file() and not p.is_symlink():
            present_core.append(rel)
            files_to_inspect.append(rel)
        else:
            missing_core.append(rel)

    for rel in bridge_files:
        p = root / rel
        if p.is_file() and not p.is_symlink():
            present_bridges.append(rel)
            files_to_inspect.append(rel)

    # Also check .ai/ directory for any accidental .env or extra files with secrets
    ai_dir = root / ".ai"
    if ai_dir.is_dir() and not ai_dir.is_symlink():
        for dirpath, dirnames, filenames in os.walk(ai_dir, followlinks=False):
            dirnames[:] = sorted(dirnames)
            for fname in sorted(filenames):
                fp = Path(dirpath) / fname
                if fp.is_symlink() or not fp.is_file():
                    continue
                rel = str(fp.relative_to(root)).replace("\\", "/")
                if is_sensitive_env_name(fname):
                    env_files_found.append(rel)
                elif rel not in files_to_inspect:
                    files_to_inspect.append(rel)

    total_est_tokens = 0
    for rel in files_to_inspect:
        fp = root / rel
        try:
            if fp.stat().st_size > 512 * 1024:
                continue
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        lines_list = content.splitlines()
        line_count = len(lines_list)
        est_tokens = max(1, round(len(content) / 4)) if content else 0
        total_est_tokens += est_tokens
        budget = LINE_BUDGETS.get(rel)
        over_budget = budget is not None and line_count > budget
        if over_budget:
            budget_warnings.append(
                f"`{rel}` tiene {line_count} líneas (~{est_tokens} tokens); límite recomendado: ≤ {budget} líneas."
            )
        file_metrics.append(
            {
                "file": rel,
                "lines": line_count,
                "estimated_tokens": est_tokens,
                "recommended_max_lines": budget,
                "over_budget": over_budget,
            }
        )

        ph_count = 0
        for idx, line in enumerate(lines_list, start=1):
            ph_count += len(PLACEHOLDER_PATTERN.findall(line))
            for rule_name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    if len(secret_findings) < max_findings:
                        secret_findings.append({"file": rel, "line": idx, "rule": rule_name})
                    else:
                        secret_findings_truncated = True
                    break
        if ph_count > 0:
            placeholder_files.append({"file": rel, "placeholders": ph_count})

    has_security_blocker = bool(env_files_found or secret_findings)

    report = {
        "root": str(root),
        "present_core_files": present_core,
        "missing_core_files": missing_core,
        "present_bridges": present_bridges,
        "total_estimated_tokens": total_est_tokens,
        "file_metrics": file_metrics,
        "budget_warnings": budget_warnings,
        "files_with_placeholders": placeholder_files,
        "security_blockers": {
            "env_files_found": env_files_found,
            "potential_secret_findings": secret_findings,
            "secret_findings_truncated": secret_findings_truncated,
        },
        "has_security_blocker": has_security_blocker,
    }

    if output_format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        lines = [
            f"# Auditoría AI Context Kit: `{report['root']}`",
            "",
            f"- **Archivos base presentes:** {len(present_core)}/4 ({', '.join(present_core) or 'Ninguno'})",
            f"- **Puentes detectados:** {', '.join(present_bridges) or 'Ninguno'}",
            f"- **Tokens estimados totales de contexto:** ~{total_est_tokens}",
            "",
            "## Seguridad en archivos de contexto (Bloqueante)",
        ]
        if env_files_found:
            lines.append(f"- **CRÍTICO:** Archivos `.env` detectados en `.ai/`: {', '.join(env_files_found)}")
        if secret_findings:
            lines.append("- **CRÍTICO:** Posibles secretos detectados (solo ubicación, nunca valores):")
            for item in secret_findings:
                lines.append(f"  - `{item['file']}:{item['line']}` ({item['rule']})")
            if secret_findings_truncated:
                lines.append("  - *(Truncado por `--max-findings`.)*")
        if not has_security_blocker:
            lines.append("- [OK] Sin secretos ni archivos `.env` en archivos de contexto IA.")

        lines.append("")
        lines.append("## Presupuesto de contexto y completitud")
        if missing_core:
            for mf in missing_core:
                lines.append(f"- [FALTA] `{mf}`")
        else:
            lines.append("- [OK] Los 4 archivos base (`CONSTITUTION.md`, `AGENTS.md`, `MEMORY.md`, `TASK_SPEC.md`) existen.")
        if budget_warnings:
            for w in budget_warnings:
                lines.append(f"- **AVISO DE TOKENS:** {w}")
        else:
            lines.append("- [OK] Todos los archivos presentes respetan su presupuesto recomendado de líneas.")
        if placeholder_files:
            lines.append("")
            lines.append("## Archivos con placeholders pendientes de completar")
            for pf in placeholder_files:
                lines.append(f"- `{pf['file']}` ({pf['placeholders']} placeholders)")

        print("\n".join(lines))

    return 2 if has_security_blocker else 0


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="AI Workflow & Context Engineering scaffold (init) & token-budget audit"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create compact CONSTITUTION.md, AGENTS.md, .ai/MEMORY.md, .ai/TASK_SPEC.md")
    p_init.add_argument("path", nargs="?", default=".", help="Path to repository root")
    p_init.add_argument("--project-name", default="[Nombre del Proyecto]", help="Project name for headers")
    p_init.add_argument(
        "--bridges",
        default="",
        help="Comma-separated tool bridges to create: claude,gemini,cursor",
    )
    p_init.add_argument("--dry-run", action="store_true", help="Preview files without writing to disk")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing files")

    p_audit = sub.add_parser("audit", help="Read-only context budget, placeholder, and secret audit")
    p_audit.add_argument("path", nargs="?", default=".", help="Path to repository root")
    p_audit.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    p_audit.add_argument("--max-findings", type=int, default=25, help="Max secret findings to report")

    args = parser.parse_args()

    if args.command == "init":
        bridges = [b.strip().lower() for b in args.bridges.split(",") if b.strip()]
        invalid = [b for b in bridges if b not in VALID_BRIDGES]
        if invalid:
            raise SystemExit(
                f"Error: unknown bridge(s): {', '.join(invalid)}. Allowed: {', '.join(sorted(VALID_BRIDGES))}"
            )
        rc = run_init(
            root=Path(args.path).resolve(),
            project_name=args.project_name,
            bridges=bridges,
            dry_run=args.dry_run,
            force=args.force,
        )
        raise SystemExit(rc)

    if args.max_findings < 1:
        raise SystemExit("Error: --max-findings must be >= 1")

    rc = run_audit(
        root=Path(args.path).resolve(),
        output_format=args.format,
        max_findings=args.max_findings,
    )
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
