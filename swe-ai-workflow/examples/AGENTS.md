# AGENTS — Mapa Operativo de [Nombre del Proyecto]

> Fuente única de contexto operativo para cualquier agente de IA. **Mantener ≤ 100 líneas.**
> Lee también [CONSTITUTION.md](./CONSTITUTION.md) (reglas innegociables) y [.ai/MEMORY.md](./.ai/MEMORY.md) (estado y aprendizajes recientes).

## 1. Qué hace este proyecto
`[Descripción de 2–3 líneas del propósito del sistema y usuarios principales.]`

## 2. Mapa compacto de carpetas
```text
.
├── src/          # [Código principal: describir subcarpetas clave en 1 línea]
├── tests/        # [Pruebas automatizadas]
├── docs/         # [ADRs, OpenAPI y documentación técnica]
└── .ai/          # MEMORY.md (estado/aprendizajes) y TASK_SPEC.md (tarea activa)
```

## 3. Comandos reales (ejecutar en lugar de adivinar)
- **Instalar dependencias:** `[Ej. npm ci | uv sync --frozen]`
- **Desarrollo local:** `[Ej. npm run dev | uvicorn app.main:app --reload]`
- **Lint / Formato:** `[Ej. npm run lint | ruff check .]`
- **Typecheck / Build:** `[Ej. npm run typecheck && npm run build | mypy .]`
- **Tests rápidos (usar tras cada lote):** `[Ej. npm test | pytest -q]`
- **Tests E2E / Auditoría:** `[Ej. npx playwright test]`

## 4. Convenciones rápidas del repositorio
- **Commits:** Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).
- **Variables de entorno:** documentadas en `.env.example` (nunca leer ni imprimir `.env` real).
- **Puntos de entrada clave:** `[Ej. src/main.ts, src/routes/index.ts, prisma/schema.prisma]`.

## 5. Flujo obligatorio por tarea
1. Convertir peticiones abiertas en un mini-contrato en `.ai/TASK_SPEC.md` (Objetivo + Archivos + Restricciones + Comando de verificación).
2. Ejecutar primero linters/tests/scripts deterministas antes de pedir análisis amplio al LLM.
3. Antes de cerrar la sesión, actualizar `.ai/MEMORY.md` con lo completado, pendientes e intentos fallidos.
