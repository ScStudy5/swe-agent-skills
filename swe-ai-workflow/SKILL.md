---
name: swe-ai-workflow
description: >-
  Guía profesional de Context Engineering, flujo de trabajo con agentes IA y control
  de vibe coding: genera archivos base compactos (CONSTITUTION.md, AGENTS.md con
  puentes a CLAUDE.md/GEMINI.md/.cursor/rules/, MEMORY.md y TASK_SPEC.md), aplica
  reglas de ahorro radical de tokens (plan corto, lectura selectiva, scripts antes
  que LLM, higiene de sesión) y corrige vibe coding desordenado (lotes pequeños
  verificados y regla de 2 intentos contra deriva). Usar al configurar un proyecto
  para programar con IA, reducir gasto de tokens o estructurar prompts vagos (para
  construir productos con LLMs/RAG/agentes en producción usar swe-ai-engineering).
---

# Context Engineering, Flujo con Agentes IA y Control de Vibe Coding

Aplica esta skill para preparar un repositorio para trabajar con asistentes/agentes de IA (Antigravity, Claude Code, Codex, Cursor, OpenCode, Gemini CLI) ahorrando tokens, evitando contexto inflado y transformando el *vibe coding* improvisado en entregas verificables.

## Reglas fundamentales
1. **Contexto corto, denso y de fuente única:** los archivos de contexto que el agente lee en cada sesión deben ser breves (<100–120 líneas). Mantén la verdad operativa en `AGENTS.md`, `CONSTITUTION.md` y `.ai/MEMORY.md`; usa `CLAUDE.md`, `GEMINI.md` o `.cursor/rules/` solo como puentes de 5 líneas (nunca dupliques instrucciones).
2. **Script antes que LLM:** ejecuta primero herramientas deterministas (linters, `tsc`/typecheck, tests, `repo_audit_scan.py`, `ai_context_kit.py`) en lugar de gastar tokens pidiendo a la IA que "revise todo el proyecto a ojo".
3. **Cero secretos en archivos de contexto:** nunca pegues API keys, contraseñas, tokens ni PII en `AGENTS.md`, `CONSTITUTION.md`, `MEMORY.md` ni en prompts.
4. **Nivel de rigor proporcional:** si el usuario no indicó el nivel (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto:
   * **Nivel 1 — MVP / Solo dev:** `CONSTITUTION.md`, `AGENTS.md`, `.ai/MEMORY.md` y mini-specs `TASK_SPEC.md` para cambios de más de 1 archivo.
   * **Nivel 2 — Profesional (Equipo / Producción):** lo anterior + puentes para las herramientas del equipo (`CLAUDE.md`/`GEMINI.md`/`.cursor/rules/`), verificación obligatoria (`lint` + `typecheck` + `test`) por lote pequeño y auditoría periódica de presupuesto de contexto.
   * **Nivel 3 — Empresarial / Regulado:** zonas protegidas estrictas (auth, precios, migraciones, permisos requieren aprobación humana explícita), auditoría `ai_context_kit.py audit` en CI y revisión obligatoria de `git diff` contra *slopsquatting* y regresiones de seguridad.

## Flujo de trabajo

### Pilar A — Generar o auditar los archivos base de contexto IA
1. **Generación automática (previsualiza primero con `--dry-run`):** ejecuta [ai_context_kit.py](./scripts/ai_context_kit.py) desde la ruta resuelta de esta skill; el script inspecciona el repo y pre-llena los comandos reales de build/test/lint en `AGENTS.md`:
   ```bash
   # Previsualizar archivos a crear (sin escribir en disco)
   python3 <ruta-de-la-skill>/scripts/ai_context_kit.py init <ruta-del-repo> --bridges claude,gemini,cursor --dry-run

   # Crear CONSTITUTION.md, AGENTS.md, .ai/MEMORY.md, .ai/TASK_SPEC.md y puentes (sin sobrescribir existentes)
   python3 <ruta-de-la-skill>/scripts/ai_context_kit.py init <ruta-del-repo> --bridges claude,gemini,cursor

   # Auditar presupuesto de líneas/tokens, placeholders y cero secretos en archivos de contexto
   python3 <ruta-de-la-skill>/scripts/ai_context_kit.py audit <ruta-del-repo>
   ```
   *(En Windows usa `python` en lugar de `python3`. Códigos de salida de `audit`: `0` sin bloqueadores de seguridad, `1` error de argumentos, `2` secreto o `.env` detectado en archivos de contexto).*
2. **Completar con las plantillas compactas de `./examples/`:**
   * Reglas innegociables y zonas protegidas -> [CONSTITUTION.md](./examples/CONSTITUTION.md)
   * Mapa compacto del repo y comandos reales -> [AGENTS.md](./examples/AGENTS.md)
   * Memoria viva (estado, errores resueltos e intentos fallidos) -> [MEMORY.md](./examples/MEMORY.md)
   * Mini-contrato para transformar prompts vagos -> [TASK_SPEC.md](./examples/TASK_SPEC.md)
   * Puentes finos para múltiples herramientas IA -> [TOOL_BRIDGES.md](./examples/TOOL_BRIDGES.md)

### Pilar B — Reglas de ahorro radical de tokens (para agente y usuario)
Consulta el detalle y presupuestos en [context-engineering-and-tokens.md](./references/context-engineering-and-tokens.md):
1. **Plan corto antes de editar:** ante cualquier prompt ambiguo o que afecte múltiples archivos, presenta primero un **plan de 3–5 líneas** (archivos a tocar, cambio y comando de verificación) y confirma alcance antes de escribir código.
2. **Lectura selectiva obligatoria:** busca primero con `rg`/`grep` y lee solo rangos puntuales de líneas; nunca vuelques archivos enteros ni logs de 500 líneas cuando basta el bloque del error.
3. **Higiene de sesión (1 tarea = 1 sesión):** cuando termines una funcionalidad o la conversación empiece a degradarse/crecer, actualiza `.ai/MEMORY.md` (máx. 5 líneas nuevas, podando lo obsoleto) y cierra o compacta el chat antes de iniciar la siguiente tarea.

### Pilar C — Corrección automática del *Vibe Coding* desordenado
Consulta el protocolo completo en [anti-vibe-coding-guardrails.md](./references/anti-vibe-coding-guardrails.md):
1. **De prompt vago a `TASK_SPEC.md`:** si el usuario pide algo abierto (p. ej. *"haz el login"* o *"arregla el dashboard"*), tradúcelo en segundos a un mini-contrato de 4 líneas (**Objetivo + Archivos involucrados + Restricciones + Comando de verificación**) antes de codificar.
2. **Lote pequeño + verificación obligatoria:** cada cambio debe pasar `lint` + `typecheck` + `test` (y revisión del `git diff`) **antes** de pedir o encadenar la siguiente funcionalidad.
3. **Detección de deriva (Regla de 2 intentos):** si en **2 intentos consecutivos** un bug no queda resuelto, **detén el parcheo ciego**. Relee el error real, formula hipótesis verificable de causa raíz, consulta documentación real (p. ej. `Context7` si existe) y documenta qué se probó y falló en `.ai/MEMORY.md` para que ninguna sesión futura repita el bucle.

## Criterios de verificación
* `CONSTITUTION.md`, `AGENTS.md` y `.ai/MEMORY.md` reflejan comandos y rutas reales del proyecto y se mantienen dentro de su presupuesto de líneas (<120 líneas cada uno).
* Los archivos puente (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`) solo apuntan a la fuente única sin duplicar instrucciones contradictorias.
* `ai_context_kit.py audit` confirma **0 secretos** en archivos de contexto y ningún lote de código se da por terminado sin pasar su comando de verificación real.
