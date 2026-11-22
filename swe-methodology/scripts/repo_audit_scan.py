#!/usr/bin/env python3
"""Quick repository hygiene and stack discovery scan for software engineering audits.

Read-only diagnostic tool using Python standard library only.
Never prints secret values—only file paths, line numbers, and pattern names.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "out",
    "target",
    "bin",
    "obj",
    ".next",
    ".nuxt",
    ".output",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "coverage",
    ".dart_tool",
}

STACK_MARKERS = {
    "package.json": "Node.js / JavaScript / TypeScript",
    "tsconfig.json": "TypeScript",
    "pyproject.toml": "Python (pyproject)",
    "requirements.txt": "Python (requirements.txt)",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "pubspec.yaml": "Dart / Flutter",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Java / Kotlin (Gradle KTS)",
    "composer.json": "PHP",
    "Gemfile": "Ruby",
    "Dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
}

MONOREPO_SUBDIRS = {
    "apps",
    "packages",
    "services",
    "backend",
    "frontend",
    "api",
    "web",
    "server",
    "client",
    "mobile",
}

LOCKFILES = [
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "bun.lock",
    "poetry.lock",
    "uv.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "go.sum",
    "pubspec.lock",
    "composer.lock",
    "Gemfile.lock",
]

DOC_FILES = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "ARCHITECTURE.md",
    "CHANGELOG.md",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".env.example",
]

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

TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".yml", ".yaml",
    ".toml", ".ini", ".cfg", ".conf", ".properties", ".env", ".cs", ".java", ".kt",
    ".go", ".rs", ".php", ".rb", ".dart", ".sql", ".sh", ".ps1", ".tf", ".tfvars",
    ".xml", ".html", ".vue", ".svelte", ".astro", ".md",
}


def is_sensitive_env_name(filename: str) -> bool:
    """Return True for .env and .env.* files excluding safe example/template names."""
    lower = filename.lower()
    if not (lower == ".env" or lower.startswith(".env.")):
        return False
    return not lower.endswith(ENV_SAFE_SUFFIXES)


def detect_git_tracked_env(root: Path) -> list[str]:
    """Return tracked .env files (root or nested, excluding templates) if inside a git repo."""
    if not (root / ".git").exists():
        return []
    try:
        res = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), "ls-files"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode != 0:
            return []
        tracked: list[str] = []
        for raw_line in res.stdout.splitlines():
            rel_path = raw_line.strip()
            if not rel_path:
                continue
            fname = Path(rel_path).name
            if is_sensitive_env_name(fname):
                tracked.append(rel_path.replace("\\", "/"))
        return tracked
    except (OSError, subprocess.SubprocessError):
        return []


def collect_stack_candidate_dirs(root: Path) -> list[Path]:
    """Return root plus shallow monorepo package directories for stack detection."""
    dirs = [root]
    for sub_name in MONOREPO_SUBDIRS:
        sub = root / sub_name
        if not sub.is_dir() or sub.is_symlink():
            continue
        dirs.append(sub)
        if sub_name in {"apps", "packages", "services"}:
            try:
                for child in sorted(sub.iterdir()):
                    if child.is_dir() and not child.is_symlink() and child.name not in IGNORED_DIRS:
                        dirs.append(child)
            except OSError:
                continue
    return dirs


def detect_ci_workflows(root: Path) -> list[str]:
    """Detect common CI/CD pipeline configuration files."""
    ci_workflows: list[str] = []
    gh_dir = root / ".github" / "workflows"
    if gh_dir.is_dir() and not gh_dir.is_symlink():
        ci_workflows.extend(
            sorted(
                str(p.relative_to(root)).replace("\\", "/")
                for p in gh_dir.glob("*.y*ml")
                if p.is_file() and not p.is_symlink()
            )
        )
    for extra in (
        "azure-pipelines.yml",
        "azure-pipelines.yaml",
        ".gitlab-ci.yml",
        "Jenkinsfile",
        ".circleci/config.yml",
        "bitbucket-pipelines.yml",
    ):
        candidate = root / extra
        if candidate.is_file() and not candidate.is_symlink():
            ci_workflows.append(extra)
    return ci_workflows


def scan_repository(root: Path, max_findings: int = 25) -> dict:
    """Scan repository root and return structured diagnostic findings."""
    stacks: set[str] = set()
    lockfiles_present: set[str] = set()

    for candidate_dir in collect_stack_candidate_dirs(root):
        for filename, label in STACK_MARKERS.items():
            if (candidate_dir / filename).is_file():
                stacks.add(label)
        if list(candidate_dir.glob("*.sln")) or list(candidate_dir.glob("*.csproj")):
            stacks.add(".NET / C#")
        for lf in LOCKFILES:
            if (candidate_dir / lf).is_file():
                rel_lf = str((candidate_dir / lf).relative_to(root)).replace("\\", "/")
                lockfiles_present.add(rel_lf)

    docs_present = {f: (root / f).is_file() for f in DOC_FILES}
    docs_present["docs/adr"] = (root / "docs" / "adr").is_dir()

    ci_workflows = detect_ci_workflows(root)
    test_dirs = [
        d for d in ("tests", "test", "__tests__", "spec", "e2e") if (root / d).is_dir()
    ]
    env_files_on_disk: list[str] = []
    secret_findings: list[dict[str, object]] = []
    secret_findings_truncated = False
    todo_count = 0
    scanned_files = 0

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if fpath.is_symlink() or not fpath.is_file():
                continue

            rel = str(fpath.relative_to(root)).replace("\\", "/")

            if is_sensitive_env_name(fname):
                env_files_on_disk.append(rel)
                continue

            if fname.lower().endswith(ENV_SAFE_SUFFIXES) or fname in LOCKFILES:
                continue

            if fpath.suffix.lower() not in TEXT_EXTENSIONS and fname not in {"Dockerfile"}:
                continue

            try:
                if fpath.stat().st_size > 512 * 1024:
                    continue
                content = fpath.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            scanned_files += 1
            for idx, line in enumerate(content.splitlines(), start=1):
                if "TODO" in line or "FIXME" in line:
                    todo_count += 1
                for rule_name, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        if len(secret_findings) < max_findings:
                            secret_findings.append(
                                {"file": rel, "line": idx, "rule": rule_name}
                            )
                        else:
                            secret_findings_truncated = True
                        break

    return {
        "root": str(root),
        "stacks_detected": sorted(stacks),
        "docs_present": docs_present,
        "lockfiles_present": sorted(lockfiles_present),
        "ci_workflows": ci_workflows,
        "test_dirs_at_root": test_dirs,
        "env_files_on_disk": env_files_on_disk,
        "git_tracked_env_files": detect_git_tracked_env(root),
        "potential_secret_findings": secret_findings,
        "secret_findings_truncated": secret_findings_truncated,
        "todo_fixme_lines": todo_count,
        "scanned_text_files": scanned_files,
    }


def format_markdown(report: dict) -> str:
    """Format diagnostic report as concise Markdown."""
    lines = [
        f"# Diagnóstico rápido: `{report['root']}`",
        "",
        f"- **Stacks detectados:** {', '.join(report['stacks_detected']) or 'No detectado en raíz/subproyectos estándar'}",
        f"- **Lockfiles:** {', '.join(report['lockfiles_present']) or 'Ninguno detectado'}",
        f"- **Workflows CI:** {', '.join(report['ci_workflows']) or 'Ninguno detectado'}",
        f"- **Carpetas de tests en raíz:** {', '.join(report['test_dirs_at_root']) or 'Ninguna en raíz'}",
        f"- **Archivos de texto escaneados:** {report['scanned_text_files']} (líneas TODO/FIXME: {report['todo_fixme_lines']})",
        "",
        "## Documentación e higiene base",
    ]
    for doc, exists in report["docs_present"].items():
        mark = "OK" if exists else "FALTA"
        lines.append(f"- [{mark}] `{doc}`")

    lines.append("")
    lines.append("## Alertas de seguridad e higiene")
    if report["git_tracked_env_files"]:
        lines.append(
            f"- **CRÍTICO:** Archivos `.env` rastreados en Git: {', '.join(report['git_tracked_env_files'])}"
        )
    if report["env_files_on_disk"]:
        lines.append(
            f"- **AVISO:** Archivos `.env` presentes en disco (verificar `.gitignore`): {', '.join(report['env_files_on_disk'])}"
        )
    if report["potential_secret_findings"]:
        lines.append("- **REVISAR:** Posibles secretos hardcodeados (solo ubicación, verificar falsos positivos):")
        for item in report["potential_secret_findings"]:
            lines.append(f"  - `{item['file']}:{item['line']}` ({item['rule']})")
        if report["secret_findings_truncated"]:
            lines.append("  - *(Resultados truncados por límite `--max-findings`; ejecuta Gitleaks o aumenta `--max-findings` para revisión exhaustiva.)*")
    if (
        not report["git_tracked_env_files"]
        and not report["env_files_on_disk"]
        and not report["potential_secret_findings"]
    ):
        lines.append("- Sin alertas evidentes de archivos `.env` o patrones de secretos.")

    return "\n".join(lines)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Quick repository hygiene scan (read-only)")
    parser.add_argument("path", nargs="?", default=".", help="Path to repository root")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument("--max-findings", type=int, default=25, help="Maximum secret findings to report")
    args = parser.parse_args()

    if args.max_findings < 1:
        raise SystemExit("Error: --max-findings must be >= 1")

    root = Path(args.path).resolve()
    if not root.is_dir():
        raise SystemExit(f"Error: directory not found: {root}")

    report = scan_repository(root, max_findings=args.max_findings)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(report))


if __name__ == "__main__":
    main()
