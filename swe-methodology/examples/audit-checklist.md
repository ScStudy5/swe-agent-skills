# Checklist de Auditoría Integral (MVP → Producción Escalable)

Usa este checklist para auditar proyectos existentes o validar una entrega antes de salir a producción (orientado a proyectos desde MVP hasta sistemas de miles de usuarios).

## Bloque 1 — Arquitectura, Código y Requisitos
- [ ] Arquitectura clara y modular (sin lógica de negocio mezclada en rutas HTTP o vistas).
- [ ] Requisitos y flujos críticos definidos con criterios de aceptación claros.
- [ ] Sin dependencia extrema (*Vendor Lock-in*) innecesaria en lógica central.
- [ ] Linter, formatter y tipado estático activos y pasando sin errores.
- [ ] Manejo consistente de errores y logging estructurado sin datos sensibles.

## Bloque 2 — Seguridad, Privacidad y Dependencias (Bloqueante)
- [ ] Cero secretos, API keys o `.env` reales rastreados en Git o en logs.
- [ ] Validación de entradas y **cálculo de precios/totales/permisos en servidor** en **todos** los endpoints/formularios.
- [ ] Autenticación segura, sesiones/tokens con expiración y autorización (RBAC/tenant) verificada en cada recurso.
- [ ] HTTPS/TLS, **sin modo depuración (`DEBUG=false`)**, sin archivos/buckets expuestos (`.git`, `.sql`, `.map`), Security Headers, CORS estricto y Rate Limiting en rutas sensibles.
- [ ] Lockfiles presentes, dependencias revisadas sin CVEs críticos/altos y licencias OSS compatibles.
- [ ] Minimización de PII, aviso de privacidad cuando aplique y logs libres de datos personales sensibles.

## Bloque 3 — Pruebas y Calidad (QA)
- [ ] Pruebas unitarias en lógica de negocio crítica y casos límite.
- [ ] Pruebas de integración en BD/APIs reales (sin usar datos personales reales).
- [ ] Pruebas E2E o Smoke en los flujos críticos de negocio (registro, login, flujo principal, pagos).
- [ ] Suite automatizada ejecutándose en cada Pull Request.

## Bloque 4 — Datos, APIs, Resiliencia y Rendimiento
- [ ] Migraciones de base de datos versionadas y compatibles hacia atrás.
- [ ] Índices en consultas frecuentes y ausencia de consultas N+1 evidentes.
- [ ] Backups automáticos configurados **y restauración probada** al menos una vez.
- [ ] Contratos de API documentados (OpenAPI) y errores consistentes (RFC 9457).
- [ ] Timeouts, retries con backoff/jitter, idempotencia en operaciones críticas y paginación en listados.

## Bloque 5 — UX/UI, Accesibilidad, Operación y Costos
- [ ] Diseño responsive Mobile First sin scroll horizontal; estados Loading, Empty y Error implementados.
- [ ] Accesibilidad básica WCAG 2.2 AA (teclado, foco visible, contraste, etiquetas, `alt`).
- [ ] Entorno local reproducible (`Docker` / `docker-compose.yml`) y CI/CD automatizado por ambientes (`Local -> Dev/Staging -> Producción`) con rollback claro.
- [ ] Monitoreo de errores (ej. Sentry), health checks y alertas básicas de disponibilidad.
- [ ] Topes duros/límites de auto-scaling y alertas de costos en nube (Azure/AWS/GCP) y APIs externas configurados (recordando que las alertas en cloud no apagan recursos automáticamente).
- [ ] Si usa IA/LLMs: protección contra *prompt injection*, límites de tokens, validación de salidas y *evals* base.

## Formato recomendado del reporte de auditoría
1. **Crítico (Bloqueante para producción):** fallos de seguridad, fuga de datos, pérdida de integridad o ausencia total de validación/auth.
2. **Importante (Corto plazo para escalar a miles de usuarios):** falta de índices, timeouts/retries, backups sin probar, tests faltantes en flujos clave, alertas de costos.
3. **Recomendado (Mejora continua):** deuda técnica menor, optimizaciones UX/A11y finas, documentación adicional.
