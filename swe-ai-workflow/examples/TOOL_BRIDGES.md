# Puentes Finos para Herramientas IA (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`)

Para evitar duplicar instrucciones (y quemar el doble de tokens o generar contradicciones entre herramientas), mantén la fuente única de verdad en `AGENTS.md`, `CONSTITUTION.md` y `.ai/MEMORY.md`, y usa archivos puente de **≤ 15 líneas**.

---

## 1. `CLAUDE.md` (Claude Code)
```markdown
# Project Instructions (Claude Code Bridge)

Source of truth for this repository:
- Read `AGENTS.md` for architecture map, real build/test/lint commands, and workflow.
- Follow all non-negotiable rules in `CONSTITUTION.md`.
- Check `.ai/MEMORY.md` before starting and update it before ending the session.
```

## 2. `GEMINI.md` (Antigravity / Gemini CLI)
```markdown
# Project Instructions (Gemini / Antigravity Bridge)

Source of truth for this repository:
- Read `AGENTS.md` for architecture map, real build/test/lint commands, and workflow.
- Follow all non-negotiable rules in `CONSTITUTION.md`.
- Check `.ai/MEMORY.md` before starting and update it before ending the session.
```

## 3. `.cursor/rules/00-project-context.mdc` (Cursor)
```markdown
---
description: Core repository rules, commands, and living AI memory
alwaysApply: true
---

Read and follow:
1. `CONSTITUTION.md` — non-negotiable rules, protected zones, and quality gates.
2. `AGENTS.md` — repository map and exact build/lint/typecheck/test commands.
3. `.ai/MEMORY.md` — current status, resolved bugs, and failed approaches to avoid repeating.
```

> **Alternativa en Linux/macOS:** en equipos que solo usan Unix (sin Windows), también se puede usar un enlace simbólico (`ln -s AGENTS.md CLAUDE.md`), pero los puentes de 5 líneas son más portables entre Windows, macOS, Linux y Git sin requerir `core.symlinks=true`.
