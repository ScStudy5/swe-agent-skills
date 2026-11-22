#!/usr/bin/env python3
"""Project Handover scaffolding and security/completeness audit tool.

Zero external dependencies (Python standard library only).
- `audit` (read-only): validates completeness by project level (1/2/3), counts
  unfilled placeholders, and blocks accidental `.env` files or secrets inside
  PROJECT-HANDOVER/ (never prints secret values).
- `init` (opt-in write): creates the standardized 18-point PROJECT-HANDOVER/
  tree calibrated by level without overwriting existing files unless `--force`.

Exit codes:
  0 = success (and 0 critical security blockers in `audit`)
  1 = CLI argument error / path error
  2 = critical security blocker found in `audit` (.env or secret inside handover)
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
    r"\[(?:TODO|PENDIENTE|COMPLETAR|YYYY-MM-DD|<git-sha>|Nombre[^\]]*|Ej\.[^\]]*|Rol[^\]]*|Descripción[^\]]*)\]",
    re.IGNORECASE,
)

# Each entry: (section_dir, filename, min_level, title, optional_example_template)
BLUEPRINT: list[tuple[str, str, int, str, str | None]] = [
    ("00-START-HERE", "INDEX.md", 1, "Índice Maestro de Handover", "00-INDEX.md"),
    ("00-START-HERE", "QUICKSTART.md", 1, "Guía de Arranque Rápido (Primeros 30 Minutos)", None),
    ("00-START-HERE", "PROJECT_STATUS.md", 1, "Estado Actual del Proyecto", None),
    ("01-EXECUTIVE-CONTEXT", "PROJECT_CHARTER.md", 2, "Acta de Constitución del Proyecto (Project Charter)", None),
    ("01-EXECUTIVE-CONTEXT", "BUSINESS_CASE.md", 3, "Caso de Negocio (Business Case)", None),
    ("01-EXECUTIVE-CONTEXT", "STAKEHOLDERS.md", 2, "Mapa de Stakeholders y Contactos", None),
    ("01-EXECUTIVE-CONTEXT", "PRODUCT_VISION.md", 2, "Visión de Producto y Roadmap", None),
    ("01-EXECUTIVE-CONTEXT", "GLOSSARY.md", 2, "Glosario de Dominio y Negocio", None),
    ("02-REQUIREMENTS-AND-DOMAIN", "FUNCTIONAL_REQUIREMENTS.md", 2, "Requisitos Funcionales", None),
    ("02-REQUIREMENTS-AND-DOMAIN", "NON_FUNCTIONAL_REQUIREMENTS.md", 2, "Requisitos No Funcionales (ISO/IEC 25010)", None),
    ("02-REQUIREMENTS-AND-DOMAIN", "DOMAIN_REQUIREMENTS.md", 2, "Requisitos de Dominio y Regulación", None),
    ("02-REQUIREMENTS-AND-DOMAIN", "SCOPE_AND_EXCLUSIONS.md", 3, "Alcance y Exclusiones Explícitas", None),
    ("03-ARCHITECTURE-AND-DESIGN", "ARCHITECTURE.md", 1, "Arquitectura del Sistema (C4)", None),
    ("03-ARCHITECTURE-AND-DESIGN", "DIAGRAMS.md", 2, "Diagramas Técnicos (C4, Secuencia, Despliegue)", None),
    ("03-ARCHITECTURE-AND-DESIGN", "ADRS_INDEX.md", 2, "Índice de Decisiones Arquitectónicas (ADRs)", None),
    ("04-CODEBASE-GUIDE", "CODEBASE_GUIDE.md", 1, "Guía del Código Fuente para Sucesores", "CODEBASE_GUIDE.md"),
    ("04-CODEBASE-GUIDE", "MODULES.md", 2, "Mapa de Módulos y Responsabilidades", None),
    ("04-CODEBASE-GUIDE", "ERROR_CATALOG.md", 2, "Catálogo de Errores de Dominio y API", None),
    ("04-CODEBASE-GUIDE", "CONFIGURATION_REFERENCE.md", 1, "Referencia de Configuración y Variables de Entorno", None),
    ("05-DATA-AND-DATABASES", "DATABASE_GUIDE.md", 2, "Modelo de Datos y Esquema (ERD)", None),
    ("05-DATA-AND-DATABASES", "DATA_DICTIONARY.md", 2, "Diccionario de Datos", None),
    ("05-DATA-AND-DATABASES", "MIGRATIONS_AND_SEEDS.md", 2, "Migraciones, Semillas y Datos de Prueba", None),
    ("05-DATA-AND-DATABASES", "BACKUP_AND_RECOVERY.md", 2, "Respaldos, RTO/RPO y Evidencia de Restore Testing", None),
    ("06-APIS-AND-INTEGRATIONS", "API_GUIDE.md", 2, "Guía de APIs, OpenAPI y Errores RFC 9457", None),
    ("06-APIS-AND-INTEGRATIONS", "EXTERNAL_INTEGRATIONS.md", 2, "Integraciones Externas, Webhooks y SLAs", None),
    ("07-UX-UI-AND-ACCESSIBILITY", "DESIGN_SYSTEM_AND_FLOWS.md", 3, "Design System y Flujos Clave de UI", None),
    ("07-UX-UI-AND-ACCESSIBILITY", "ACCESSIBILITY_REPORT.md", 3, "Estado de Accesibilidad (WCAG 2.2 AA)", None),
    ("07-UX-UI-AND-ACCESSIBILITY", "I18N_AND_COMPATIBILITY.md", 3, "Internacionalización y Matriz de Compatibilidad", None),
    ("08-SECURITY-AND-PRIVACY", "SECURITY_HANDOVER.md", 1, "Seguridad, Autenticación y Bóveda de Secretos", None),
    ("08-SECURITY-AND-PRIVACY", "PRIVACY_COMPLIANCE.md", 2, "Privacidad, PII y Cumplimiento (ARCO/LFPDPPP/GDPR)", None),
    ("08-SECURITY-AND-PRIVACY", "SBOM_AND_SCA_STATUS.md", 3, "Estado de Dependencias, SCA y SBOM", None),
    ("09-QA-AND-TESTING", "TESTING_GUIDE.md", 2, "Estrategia y Guía de Pruebas (QA)", None),
    ("09-QA-AND-TESTING", "TEST_DATA_AND_ENVIRONMENTS.md", 2, "Ambientes de Prueba y Datos Sintéticos", None),
    ("09-QA-AND-TESTING", "LAST_AUDIT_RESULTS.md", 2, "Resultados de Última Auditoría (Código / Navegador)", None),
    ("10-DEVOPS-AND-OPERATIONS", "INFRASTRUCTURE_AND_DEPLOY.md", 1, "Infraestructura, Despliegue y Ambientes", None),
    ("10-DEVOPS-AND-OPERATIONS", "CICD_PIPELINES.md", 2, "Pipelines de CI/CD y Versionado", None),
    ("10-DEVOPS-AND-OPERATIONS", "ROLLBACK_PROCEDURES.md", 2, "Procedimientos de Rollback y Recuperación", None),
    ("10-DEVOPS-AND-OPERATIONS", "OBSERVABILITY_AND_FINOPS.md", 2, "Observabilidad, Alertas y Límites de Costos (FinOps)", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "KNOWN_ISSUES.md", 1, "Problemas Conocidos Activos y Workarounds", "KNOWN_ISSUES_AND_DEBT.md"),
    ("11-HISTORY-AND-KNOWN-ISSUES", "BUG_BACKLOG.md", 2, "Backlog de Bugs Abiertos", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "TECHNICAL_DEBT.md", 1, "Registro de Deuda Técnica", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "LESSONS_LEARNED.md", 2, "Lecciones Aprendidas", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "RISKS_REGISTER.md", 2, "Registro de Riesgos Técnicos y Operativos", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "OPEN_QUESTIONS.md", 2, "Preguntas y Decisiones Abiertas", None),
    ("11-HISTORY-AND-KNOWN-ISSUES", "DECISIONS_HISTORY.md", 2, "Historial de Decisiones Clave", None),
    ("12-LEGAL-LICENSES-AND-IP", "THIRD_PARTY_LICENSES.md", 2, "Licencias de Terceros y Open Source", None),
    ("12-LEGAL-LICENSES-AND-IP", "COPYRIGHT.md", 2, "Copyright y Licencia del Código Propio", None),
    ("12-LEGAL-LICENSES-AND-IP", "ASSET_LICENSES.md", 2, "Licencias de Activos (Fuentes, Medios, Datasets, Modelos)", None),
    ("12-LEGAL-LICENSES-AND-IP", "IP_OWNERSHIP_AND_TRANSFER.md", 3, "Titularidad y Cesión de Propiedad Intelectual", None),
    ("13-MANUALS", "USER_MANUAL.md", 2, "Manual de Usuario Final", None),
    ("13-MANUALS", "ADMINISTRATOR_MANUAL.md", 2, "Manual de Administración", None),
    ("13-MANUALS", "SUPPORT_MANUAL.md", 2, "Manual de Soporte (L1/L2/L3 y Escalamiento)", None),
    ("13-MANUALS", "OPERATIONS_MANUAL.md", 2, "Manual de Operaciones y Runbooks de Incidentes", None),
    ("14-DELIVERABLES-INVENTORY", "DELIVERABLES_INVENTORY.md", 1, "Inventario de Activos Entregables", None),
    ("14-DELIVERABLES-INVENTORY", "ACCOUNTS_AND_ACCESS_MATRIX.md", 1, "Matriz de Cuentas, Roles y Propiedad", None),
    ("15-TRANSFER-AND-SESSIONS", "ACCESS_TRANSFER_AND_REVOCATION.md", 2, "Transferencia de Propiedad, Rotación y Revocación", "ACCESS_TRANSFER_AND_REVOCATION.md"),
    ("15-TRANSFER-AND-SESSIONS", "HANDOVER_SESSIONS_LOG.md", 2, "Registro de Sesiones Supervisadas de Transferencia", None),
    ("16-HANDOVER-ACCEPTANCE", "HANDOVER_ACCEPTANCE_CHECKLIST.md", 1, "Checklist de Aceptación del Handover", None),
    ("16-HANDOVER-ACCEPTANCE", "HANDOVER_SIGN_OFF_ACTA.md", 1, "Acta Formal de Entrega y Aceptación", "HANDOVER_ACCEPTANCE_ACTA.md"),
    ("17-APPENDICES", "APPENDICES_INDEX.md", 2, "Índice de Anexos y Evidencias", None),
    ("17-APPENDICES", "LIVING_DOCUMENTATION_POLICY.md", 1, "Política de Documentación Viva (Regla 18)", None),
]

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def is_sensitive_env_name(filename: str) -> bool:
    lower = filename.lower()
    if not (lower == ".env" or lower.startswith(".env.")):
        return False
    return not lower.endswith(ENV_SAFE_SUFFIXES)


def render_stub(title: str, project_name: str, level: int, section: str, filename: str) -> str:
    today = dt.date.today().isoformat()
    if filename == "LIVING_DOCUMENTATION_POLICY.md":
        return (
            f"# {title} — {project_name}\n\n"
            f"- **Última actualización:** {today}\n"
            f"- **Nivel del proyecto:** Nivel {level}\n"
            "- **Responsable:** `[Rol / Tech Lead]`\n\n"
            "## Regla obligatoria (Punto 18 — Docs-as-Code)\n"
            "Todo Pull Request o release que cambie arquitectura, variables de entorno, contratos de API, "
            "esquema de BD, seguridad/accesos, infraestructura, incidentes conocidos o flujos de usuario "
            "**debe actualizar el documento correspondiente en `PROJECT-HANDOVER/` en el mismo cambio**.\n\n"
            "## Verificación recomendada\n"
            "- Ejecutar `handover_scaffold.py audit PROJECT-HANDOVER --level "
            f"{level}` antes de cada release mayor.\n"
            "- Revisión periódica de vigencia de `PROJECT_STATUS.md`, `KNOWN_ISSUES.md` y `ACCOUNTS_AND_ACCESS_MATRIX.md`.\n"
        )
    return (
        f"# {title} — {project_name}\n\n"
        f"- **Última actualización:** {today}\n"
        "- **Commit de referencia:** `[<git-sha>]`\n"
        "- **Responsable:** `[Rol / Nombre]`\n"
        f"- **Sección:** `{section}/{filename}` (Nivel {level})\n\n"
        "> **Seguridad:** No incluyas secretos, contraseñas ni datos personales reales (PII) en este documento.\n\n"
        "## Contenido\n"
        "- `[PENDIENTE]` Completa esta sección con hechos verificados del repositorio real (o enlaza el documento fuente vigente sin duplicar).\n"
    )


def get_initial_content(
    title: str,
    project_name: str,
    level: int,
    section: str,
    filename: str,
    template_name: str | None,
) -> str:
    if template_name:
        tpl_path = EXAMPLES_DIR / template_name
        if tpl_path.is_file() and not tpl_path.is_symlink():
            raw = tpl_path.read_text(encoding="utf-8")
            return raw.replace("[Nombre del Proyecto]", project_name)
    return render_stub(title, project_name, level, section, filename)


def run_init(target: Path, level: int, project_name: str, dry_run: bool, force: bool) -> int:
    selected = [entry for entry in BLUEPRINT if entry[2] <= level]
    created = 0
    skipped = 0
    overwritten = 0

    for section, filename, _min_lvl, title, tpl in selected:
        dest = target / section / filename
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

        rel = f"{section}/{filename}"
        if dry_run:
            print(f"[DRY-RUN] {action}: {rel}")
            continue

        if action == "SKIP_EXISTS":
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        content = get_initial_content(title, project_name, level, section, filename, tpl)
        with dest.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)

    mode = "DRY-RUN" if dry_run else "COMPLETADO"
    print(
        f"\n[{mode}] PROJECT-HANDOVER (Nivel {level}) en `{target}`: "
        f"creados={created}, sobrescritos={overwritten}, omitidos_existentes={skipped}"
    )
    return 0


def run_audit(target: Path, level: int, output_format: str, max_findings: int) -> int:
    if not target.is_dir():
        print(f"Error: directory not found: {target}", file=sys.stderr)
        return 1

    required = [entry for entry in BLUEPRINT if entry[2] <= level]
    required_sections = sorted({entry[0] for entry in required})
    missing_sections = [sec for sec in required_sections if not (target / sec).is_dir()]
    present_files: list[str] = []
    missing_files: list[str] = []

    for section, filename, _min_lvl, _title, _tpl in required:
        rel = f"{section}/{filename}"
        fpath = target / section / filename
        if fpath.is_file() and not fpath.is_symlink():
            present_files.append(rel)
        else:
            missing_files.append(rel)

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
            placeholder_hits = 0
            for idx, line in enumerate(content.splitlines(), start=1):
                placeholder_hits += len(PLACEHOLDER_PATTERN.findall(line))
                for rule_name, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        if len(secret_findings) < max_findings:
                            secret_findings.append({"file": rel, "line": idx, "rule": rule_name})
                        else:
                            secret_findings_truncated = True
                        break
            if placeholder_hits > 0:
                placeholder_files.append({"file": rel, "placeholders": placeholder_hits})

    total_required = len(required)
    completion_pct = round((len(present_files) / total_required) * 100, 1) if total_required else 100.0
    has_security_blocker = bool(env_files_found or secret_findings)

    report = {
        "target": str(target),
        "level": level,
        "required_docs_total": total_required,
        "present_docs_count": len(present_files),
        "completion_percent": completion_pct,
        "missing_sections": missing_sections,
        "missing_docs": missing_files,
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
            f"# Auditoría Project Handover (Nivel {level}): `{report['target']}`",
            "",
            f"- **Cobertura documental:** {report['present_docs_count']}/{report['required_docs_total']} ({report['completion_percent']}%)",
            f"- **Archivos escaneados:** {report['scanned_files']}",
            f"- **Archivos con placeholders sin completar:** {len(placeholder_files)}",
            "",
            "## Seguridad del paquete (Bloqueante)",
        ]
        if env_files_found:
            lines.append(f"- **CRÍTICO:** Archivos `.env` detectados dentro del handover: {', '.join(env_files_found)}")
        if secret_findings:
            lines.append("- **CRÍTICO:** Posibles secretos detectados (solo ubicación, nunca valores):")
            for item in secret_findings:
                lines.append(f"  - `{item['file']}:{item['line']}` ({item['rule']})")
            if secret_findings_truncated:
                lines.append("  - *(Truncado por `--max-findings`; corrige y vuelve a ejecutar.)*")
        if not has_security_blocker:
            lines.append("- [OK] Sin archivos `.env` ni patrones de secretos detectados dentro del handover.")

        lines.append("")
        lines.append("## Documentos faltantes para este nivel")
        if missing_files:
            for mf in missing_files:
                lines.append(f"- [FALTA] `{mf}`")
        else:
            lines.append("- [OK] Todos los documentos requeridos para este nivel existen.")

        if placeholder_files:
            lines.append("")
            lines.append("## Documentos con placeholders pendientes")
            for pf in placeholder_files[:20]:
                lines.append(f"- `{pf['file']}` ({pf['placeholders']} placeholders)")
            if len(placeholder_files) > 20:
                lines.append(f"- *(... y {len(placeholder_files) - 20} archivos más)*")

        print("\n".join(lines))

    return 2 if has_security_blocker else 0


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Project Handover scaffold (init) & completeness/security check (audit)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create PROJECT-HANDOVER/ structure calibrated by level")
    p_init.add_argument("path", nargs="?", default="PROJECT-HANDOVER", help="Target handover directory")
    p_init.add_argument("--level", type=int, choices=[1, 2, 3], default=2, help="Project rigor level (1/2/3)")
    p_init.add_argument("--project-name", default="[Nombre del Proyecto]", help="Project name for headers")
    p_init.add_argument("--dry-run", action="store_true", help="Preview files without writing to disk")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing files")

    p_audit = sub.add_parser("audit", help="Read-only completeness, placeholder, and secret-leak audit")
    p_audit.add_argument("path", nargs="?", default="PROJECT-HANDOVER", help="Target handover directory")
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
