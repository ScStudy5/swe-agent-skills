#!/usr/bin/env python3
"""Legal & Regulatory Compliance (LCS) scaffold & Launch Readiness (0/36) audit.

Zero external dependencies (Python standard library only).
- `init`: scaffolds LEGAL-DOCS/ with starter legal drafts (requiring legal counsel review)
  and the 36-item Legal Launch Readiness checklist calibrated by level (1/2/3).
- `audit` (read-only): evaluates document presence, computes Legal Launch Readiness score
  (X/36 and level-specific score), counts unfilled legal placeholders, and blocks accidental
  `.env` files or secrets inside LEGAL-DOCS/ (never prints secret values).

Exit codes:
  0 = completed without security blockers
  1 = CLI argument / path error
  2 = critical security blocker found in `audit` (.env or secret inside LEGAL-DOCS/)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

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
    r"\[(?:TODO|PENDIENTE|COMPLETAR|YYYY-MM-DD|RAZÓN SOCIAL[^\]]*|DOMICILIO[^\]]*|CALLE[^\]]*|RFC|"
    r"Nombre[^\]]*|Coautor[^\]]*|Ej\.[^\]]*|https://tu-dominio\.com[^\]]*|"
    r"[a-z]+@tu-dominio\.com|\+52[^\]]*)\]",
    re.IGNORECASE,
)

CHECKLIST_ITEM_RE = re.compile(
    r"^\s*-\s*\[([ xX])\]\s*\*\*L-(\d{2})\s*\(`N([123])`\):\*\*"
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = SKILL_ROOT / "examples"
REFERENCES_DIR = SKILL_ROOT / "references"

# (filename, min_level, source_kind, source_file_or_title)
# source_kind: "example" | "reference" | "stub"
LEGAL_BLUEPRINT: list[tuple[str, int, str, str]] = [
    ("AVISO_DE_PRIVACIDAD_INTEGRAL.md", 1, "example", "AVISO_DE_PRIVACIDAD_INTEGRAL.md"),
    ("TERMINOS_Y_CONDICIONES.md", 1, "example", "TERMINOS_Y_CONDICIONES.md"),
    ("POLITICA_DE_COOKIES.md", 1, "example", "POLITICA_DE_COOKIES.md"),
    ("COAUTHOR_IP_ASSIGNMENT_OUTLINE.md", 1, "example", "COAUTHOR_IP_ASSIGNMENT_OUTLINE.md"),
    ("ACCEPTANCE_AUDIT_LOG_SCHEMA.json", 1, "example", "ACCEPTANCE_AUDIT_LOG_SCHEMA.json"),
    ("LEGAL_LAUNCH_READINESS_36.md", 1, "reference", "legal-launch-readiness-36.md"),
    ("POLITICA_CANCELACIONES_Y_REEMBOLSOS.md", 2, "stub", "Política de Cancelaciones, Renovaciones (LFPC 76 Bis 1) y Reembolsos"),
    ("REGISTRO_PI_INDAUTOR_IMPI.md", 2, "stub", "Expediente de Propiedad Intelectual y Marca (INDAUTOR / IMPI)"),
    ("FISCAL_SAT_CFDI_Y_NOM151.md", 2, "stub", "Obligaciones Fiscales (SAT / RFC / CFDI / IVA) y Evidencia Electrónica (NOM-151)"),
    ("CONTRATOS_B2B_EULA_DPA_SLA.md", 3, "stub", "Paquete de Contratos B2B (EULA, SaaS Agreement, NDA, DPA y SLA)"),
]


def is_sensitive_env_name(filename: str) -> bool:
    lower = filename.lower()
    if not (lower == ".env" or lower.startswith(".env.")):
        return False
    return not lower.endswith(ENV_SAFE_SUFFIXES)


def render_stub(title: str, project_name: str, level: int) -> str:
    today = dt.date.today().isoformat()
    return (
        f"# {title} — {project_name}\n\n"
        "> **BORRADOR BASE — REQUIERE REVISIÓN PROFESIONAL:** Este documento es una guía técnico-operativa "
        "(LCS). **No constituye asesoría legal ni contable oficial.** Valídalo con abogado habilitado "
        "y/o contador público certificado antes de aplicarlo en producción.\n\n"
        f"- **Última actualización:** {today}\n"
        f"- **Nivel objetivo:** Nivel {level}\n"
        "- **Titular / Razón Social:** `[RAZÓN SOCIAL O TITULAR]`\n"
        "- **Jurisdicción principal:** `[México / Jurisdicción aplicable]`\n\n"
        "## Puntos a completar y validar\n"
        "- `[PENDIENTE]` Completar detalles específicos del modelo de negocio y adjuntar revisión legal/contable.\n"
    )


def build_content(source_kind: str, source_ref: str, project_name: str, level: int) -> str:
    if source_kind == "example":
        raw = (EXAMPLES_DIR / source_ref).read_text(encoding="utf-8")
        return raw.replace("[Nombre del Proyecto]", project_name)
    if source_kind == "reference":
        raw = (REFERENCES_DIR / source_ref).read_text(encoding="utf-8")
        return raw.replace("[Nombre del Proyecto]", project_name)
    return render_stub(source_ref, project_name, level)


def run_init(target: Path, level: int, project_name: str, dry_run: bool, force: bool) -> int:
    selected = [entry for entry in LEGAL_BLUEPRINT if entry[1] <= level]
    created = 0
    skipped = 0
    overwritten = 0

    for filename, _min_lvl, kind, ref in selected:
        dest = target / filename
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
            print(f"[DRY-RUN] {action}: {filename}")
            continue

        if action == "SKIP_EXISTS":
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        content = build_content(kind, ref, project_name, level)
        with dest.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)

    mode = "DRY-RUN" if dry_run else "COMPLETADO"
    print(
        f"\n[{mode}] LEGAL-DOCS (Nivel {level}) en `{target}`: "
        f"creados={created}, sobrescritos={overwritten}, omitidos_existentes={skipped}"
    )
    return 0


def parse_readiness_checklist(checklist_path: Path, level: int) -> dict | None:
    if not checklist_path.is_file() or checklist_path.is_symlink():
        return None
    text = checklist_path.read_text(encoding="utf-8", errors="ignore")
    total_found = 0
    total_checked = 0
    level_required = 0
    level_checked = 0
    unchecked_for_level: list[str] = []

    for line in text.splitlines():
        m = CHECKLIST_ITEM_RE.match(line)
        if not m:
            continue
        is_checked = m.group(1).lower() == "x"
        item_id = f"L-{m.group(2)}"
        item_level = int(m.group(3))
        total_found += 1
        if is_checked:
            total_checked += 1
        if item_level <= level:
            level_required += 1
            if is_checked:
                level_checked += 1
            else:
                unchecked_for_level.append(f"{item_id} (N{item_level})")

    return {
        "total_items_detected": total_found,
        "overall_score": f"{total_checked}/{total_found}",
        "overall_checked": total_checked,
        "level_score": f"{level_checked}/{level_required}",
        "level_checked": level_checked,
        "level_required": level_required,
        "unchecked_for_level": unchecked_for_level,
    }


def run_audit(target: Path, level: int, output_format: str, max_findings: int) -> int:
    if not target.is_dir():
        print(f"Error: directory not found: {target}", file=sys.stderr)
        return 1

    required = [entry[0] for entry in LEGAL_BLUEPRINT if entry[1] <= level]
    present_docs = [f for f in required if (target / f).is_file() and not (target / f).is_symlink()]
    missing_docs = [f for f in required if f not in present_docs]

    readiness = parse_readiness_checklist(target / "LEGAL_LAUNCH_READINESS_36.md", level)

    env_files_found: list[str] = []
    secret_findings: list[dict[str, object]] = []
    secret_findings_truncated = False
    placeholder_files: list[dict[str, object]] = []
    scanned_files = 0

    for dirpath, dirnames, filenames in os.walk(target, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if fpath.is_symlink() or not fpath.is_file():
                continue
            rel = str(fpath.relative_to(target)).replace("\\", "/")

            if is_sensitive_env_name(fname):
                env_files_found.append(rel)
                continue

            try:
                if fpath.stat().st_size > 1024 * 1024:
                    continue
                content = fpath.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            scanned_files += 1
            ph_count = 0
            for idx, line in enumerate(content.splitlines(), start=1):
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
        "target": str(target),
        "level": level,
        "required_docs_total": len(required),
        "present_docs_count": len(present_docs),
        "missing_docs": missing_docs,
        "legal_launch_readiness": readiness,
        "files_with_placeholders": placeholder_files,
        "scanned_files": scanned_files,
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
            f"# Auditoría Legal Compliance (Nivel {level}): `{report['target']}`",
            "",
            f"- **Documentos base presentes:** {report['present_docs_count']}/{report['required_docs_total']}",
            f"- **Archivos escaneados:** {report['scanned_files']}",
            f"- **Archivos con placeholders sin completar:** {len(placeholder_files)}",
        ]
        if readiness:
            lines.append(
                f"- **Legal Launch Readiness (Global):** `{readiness['overall_score']}` | "
                f"**Para Nivel {level}:** `{readiness['level_score']}`"
            )
        else:
            lines.append("- **Legal Launch Readiness:** `LEGAL_LAUNCH_READINESS_36.md` no encontrado")

        lines.append("")
        lines.append("## Seguridad del paquete legal (Bloqueante)")
        if env_files_found:
            lines.append(f"- **CRÍTICO:** Archivos `.env` detectados en LEGAL-DOCS: {', '.join(env_files_found)}")
        if secret_findings:
            lines.append("- **CRÍTICO:** Posibles secretos detectados (solo ubicación, nunca valores):")
            for item in secret_findings:
                lines.append(f"  - `{item['file']}:{item['line']}` ({item['rule']})")
            if secret_findings_truncated:
                lines.append("  - *(Truncado por `--max-findings`.)*")
        if not has_security_blocker:
            lines.append("- [OK] Sin archivos `.env` ni secretos hardcodeados en el paquete legal.")

        lines.append("")
        lines.append("## Documentos faltantes para este nivel")
        if missing_docs:
            for mf in missing_docs:
                lines.append(f"- [FALTA] `{mf}`")
        else:
            lines.append("- [OK] Todos los documentos base requeridos para este nivel existen.")

        if placeholder_files:
            lines.append("")
            lines.append("## Borradores con placeholders por completar (no publicar así)")
            for pf in placeholder_files:
                lines.append(f"- `{pf['file']}` ({pf['placeholders']} placeholders)")

        if readiness and readiness["unchecked_for_level"]:
            lines.append("")
            lines.append(f"## Ítems pendientes en Legal Launch Readiness (Nivel {level})")
            lines.append(f"- {', '.join(readiness['unchecked_for_level'])}")

        lines.append("")
        lines.append("> **Recordatorio:** Valida todos los borradores y requisitos fiscales con abogado habilitado y contador público antes del lanzamiento comercial.")
        print("\n".join(lines))

    return 2 if has_security_blocker else 0


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Legal Compliance scaffold (init) & Legal Launch Readiness 0/36 audit"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create LEGAL-DOCS/ base drafts and 0/36 checklist")
    p_init.add_argument("path", nargs="?", default="LEGAL-DOCS", help="Target directory for legal drafts")
    p_init.add_argument("--level", type=int, choices=[1, 2, 3], default=2, help="Project rigor level (1/2/3)")
    p_init.add_argument("--project-name", default="[Nombre del Proyecto]", help="Project name for headers")
    p_init.add_argument("--dry-run", action="store_true", help="Preview files without writing to disk")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing files")

    p_audit = sub.add_parser("audit", help="Read-only Legal Launch Readiness 0/36, placeholder, and secret audit")
    p_audit.add_argument("path", nargs="?", default="LEGAL-DOCS", help="Target LEGAL-DOCS directory")
    p_audit.add_argument("--level", type=int, choices=[1, 2, 3], default=2, help="Project rigor level (1/2/3)")
    p_audit.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    p_audit.add_argument("--max-findings", type=int, default=25, help="Max secret findings to report")

    args = parser.parse_args()

    if args.command == "init":
        rc = run_init(
            target=Path(args.path).resolve(),
            level=args.level,
            project_name=args.project_name,
            dry_run=args.dry_run,
            force=args.force,
        )
        raise SystemExit(rc)

    if args.max_findings < 1:
        raise SystemExit("Error: --max-findings must be >= 1")

    rc = run_audit(
        target=Path(args.path).resolve(),
        level=args.level,
        output_format=args.format,
        max_findings=args.max_findings,
    )
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
