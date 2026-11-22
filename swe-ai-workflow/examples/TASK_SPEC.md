# TASK_SPEC — Mini-Contrato de Tarea Activa

> Usa esta plantilla para convertir un prompt vago (*"haz el login"*) en un contrato verificable antes de editar código. **1 tarea = 1 sesión.**

## 1. Objetivo concreto (1–2 líneas)
`[Qué problema resuelve o qué comportamiento exacto debe quedar funcionando.]`

## 2. Archivos y alcance
- **Archivos a crear / modificar:**
  - `[ruta/archivo-1]`
  - `[ruta/archivo-2]`
- **Fuera de alcance (NO tocar):**
  - `[Ej. esquema de BD, estilos globales, módulos no relacionados]`

## 3. Restricciones y seguridad
- Respetar [CONSTITUTION.md](../CONSTITUTION.md) (sin nuevas dependencias sin permiso, validación en servidor, cero secretos/PII).
- `[Restricción específica de esta tarea: contrato API, compatibilidad, rendimiento, WCAG.]`

## 4. Criterio de terminado y comando de verificación
- [ ] El cambio cumple el objetivo en un lote pequeño y limpio (`git diff` revisado).
- [ ] Comando de verificación ejecutado y en verde:
  ```bash
  [Ej. npm run lint && npm run typecheck && npm test -- <archivo-de-prueba>]
  ```
- [ ] `.ai/MEMORY.md` actualizado si hubo hallazgos, decisiones o aprendizajes.
