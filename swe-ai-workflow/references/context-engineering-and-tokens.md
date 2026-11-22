# Context Engineering y Reglas de Ahorro Radical de Tokens

El mayor desperdicio de tokens (y la principal causa de alucinaciones en agentes de código) ocurre cuando el modelo entra a un chat nuevo "a ciegas", lee 20 archivos completos para adivinar cómo compila el proyecto o arrastra una conversación de 60 turnos con errores antiguos.

---

## 1. Presupuesto recomendado para archivos de contexto

Mantén los archivos que se inyectan al inicio de cada sesión **cortos y accionables**. Si crecen demasiado, muévelos a `docs/` o `PROJECT-HANDOVER/` y deja solo enlaces.

| Archivo | Propósito | Límite recomendado | Qué NO poner aquí |
| :--- | :--- | :---: | :--- |
| `CONSTITUTION.md` | Reglas innegociables, stack exacto y zonas protegidas | ≤ 80 líneas (~700 tokens) | Tutoriales generales de programación que la IA ya sabe |
| `AGENTS.md` | Mapa compacto del repo, comandos reales y convenciones | ≤ 100 líneas (~900 tokens) | Árbol completo archivo por archivo o changelogs largos |
| `.ai/MEMORY.md` | Estado actual, decisiones recientes e intentos fallidos | ≤ 100 líneas (~900 tokens) | Historial de hace 6 meses (podar al cerrar cada hito) |
| `CLAUDE.md` / `GEMINI.md` / `.cursor/rules/` | Puentes finos hacia `AGENTS.md` y `CONSTITUTION.md` | ≤ 20 líneas (~150 tokens) | Copias duplicadas de `AGENTS.md` que luego divergen |
| `.ai/TASK_SPEC.md` | Mini-contrato de la tarea activa | ≤ 40 líneas (~350 tokens) | Múltiples épicas mezcladas en un solo prompt |

---

## 2. Cuatro reglas de ahorro radical de tokens

### Regla 1 — Plan corto de 3–5 líneas antes de editar
Si una petición es ambigua o toca **más de 2 archivos**, prohíbe editar a ciegas. Presenta primero:
1. **Alcance exacto** (qué sí cambia y qué no).
2. **Archivos concretos** a modificar/crear.
3. **Riesgos o zonas protegidas** involucradas (auth, precios, migraciones).
4. **Comando de verificación** que probará el resultado.

Ahorra iteraciones enteras rehaciendo código que el usuario no quería.

### Regla 2 — Lectura selectiva obligatoria (nunca volcar el repo ni logs crudos)
* **Localiza primero, lee después:** usa `rg` / `grep` / búsqueda por símbolo antes de abrir archivos.
* **Rangos acotados:** lee solo las 40–100 líneas relevantes alrededor de la función o clase objetivo, no archivos de 1,500 líneas completos.
* **Logs filtrados:** nunca pegues salidas de 500 líneas de `npm test` o stack traces repetidos; filtra solo los fallos (`--bail`, `pytest -q --tb=short`, primeras 30 líneas del primer error real).

### Regla 3 — Script antes que LLM (determinismo gratis)
Antes de pedirle a la IA *"revisa todo el proyecto para ver qué está mal"*, ejecuta las herramientas deterministas locales (0 tokens de inferencia) y pásale **solo la lista concreta de fallos**:
* Estructura, docs, `.env` y secretos -> `repo_audit_scan.py` (`swe-methodology`)
* Presupuesto de contexto IA -> `ai_context_kit.py audit` (`swe-ai-workflow`)
* Sintaxis, tipos y estilo -> `eslint`, `ruff`, `tsc --noEmit`, `mypy`, `dotnet build`
* Comportamiento -> suite de tests unitarios/integración y `playwright_security_audit.mjs`

### Regla 4 — Higiene de sesión (1 tarea = 1 sesión)
El costo por turno crece linealmente con el historial y la precisión cae cuando se acumulan fallos antiguos:
1. **Una tarea verificable por chat:** no mezcles "diseña la BD", "arregla CSS" y "configura Docker" en la misma conversación eterna.
2. **Cierre limpio obligatorio:** antes de abrir un chat nuevo o compactar (`/compact`), actualiza `.ai/MEMORY.md` con:
   * Qué quedó terminado y verificado.
   * Qué quedó pendiente (siguiente paso exacto).
   * Qué se intentó y **falló** (para evitar repetirlo en el siguiente chat).
3. **Poda de memoria:** cuando `.ai/MEMORY.md` supere las 100 líneas, archiva decisiones permanentes en `docs/adr/` o `PROJECT-HANDOVER/` y borra notas temporales ya resueltas.
