# Checklist de Definition of Ready (DoR) y Definition of Done (DoD)

Adapta los puntos marcados según el nivel del proyecto (`Nivel 1`, `Nivel 2` o `Nivel 3`).

## Definition of Ready (DoR) — Antes de iniciar una tarea
- [ ] Problema y objetivo de usuario claramente definidos.
- [ ] Criterios de aceptación verificables (casos exitosos y de error).
- [ ] Dependencias técnicas o externas identificadas y desbloqueadas.
- [ ] Contrato de API / modelo de datos / diseño UX definido si la tarea lo requiere.
- [ ] Riesgos de seguridad o privacidad identificados (especialmente si maneja PII o permisos).
- [ ] Tamaño acotado para completarse dentro de una iteración.

## Definition of Done (DoD) — Antes de dar por terminada la tarea
- [ ] Código implementado respetando arquitectura, tipado y convenciones del proyecto.
- [ ] Sin secretos, tokens ni datos personales reales en código, fixtures o logs.
- [ ] Validación de entradas en servidor y manejo consistente de errores (RFC 9457 en APIs).
- [ ] Linters, formateo y análisis estático sin errores ni advertencias bloqueantes.
- [ ] Pruebas unitarias e integración pasando (y E2E en flujos críticos).
- [ ] Revisión por pares (Pull Request aprobado).
- [ ] Migraciones de BD probadas y sin consultas N+1 obvias en rutas nuevas.
- [ ] Si hay UI: responsive comprobado, estados de carga/vacío/error y accesibilidad básica (teclado, contraste, etiquetas).
- [ ] Documentación viva actualizada (`README.md`, OpenAPI, `CHANGELOG.md`, ADR y secciones afectadas de `PROJECT-HANDOVER/` si existe).
