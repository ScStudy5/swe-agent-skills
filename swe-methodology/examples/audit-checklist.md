# Checklist Maestro de Auditoría Previa al Lanzamiento (`Pre-Production Release Checklist 0/57`)

> **Regla de verificación:** marca `[x]` **únicamente después de comprobarlo con evidencia** (prueba ejecutada, configuración inspeccionada o documento publicado), no solo por haberlo implementado. Aplica los controles proporcionalmente al nivel del proyecto (`Nivel 1: MVP` / `Nivel 2: Profesional` / `Nivel 3: Empresarial`) y su perfil en [product-profiles.md](../references/product-profiles.md), respetando siempre las **3 reglas innegociables**.

## 3 Reglas Innegociables de Salida a Producción
1. Ningún secreto, llave privilegiada ni dato privado puede quedar expuesto.
2. Ningún servicio de pago (cloud, serverless, IA o API) puede operar sin límites de consumo y controles de costos adecuados.
3. Ninguna aplicación puede publicarse sin revisar sus obligaciones mínimas de seguridad y cumplimiento legal.

---

## 1. Seguridad informática (`7` puntos — Bloqueante)
- [ ] Secretos, contraseñas, tokens y API Keys privadas protegidos (cero exposición en frontend, repositorio o logs) y variables de entorno separadas entre desarrollo y producción.
- [ ] Autenticación, gestión de sesiones (cookies `HttpOnly`/`Secure`/`SameSite`, expiración, invalidación al cerrar sesión, revocación, anti-enumeración de correos) y autorización verificadas (prueba cruzada **IDOR/BOLA** entre usuarios).
- [ ] **RLS (Row Level Security)** y permisos de base de datos, vistas, funciones y Storage revisados y probados.
- [ ] Protección verificada contra inyecciones (SQL/NoSQL), XSS, CSRF, validación y cálculo de precios/permisos siempre en backend, y límites de tipo/tamaño en subida de archivos.
- [ ] Rate limiting (por IP/usuario/endpoint), protección contra fuerza bruta y defensa anti-bots/scraping activas.
- [ ] Lockfiles presentes y dependencias escaneadas sin vulnerabilidades críticas/altas (SCA / Trivy / Dependabot / CodeQL).
- [ ] Panel administrativo protegido (RBAC estricto, **MFA** para administradores y Audit Logs de acciones administrativas).

## 2. Infraestructura y costos inesperados (`6` puntos — Bloqueante)
- [ ] Presupuesto máximo operativo y **topes duros de gasto (*hard spending caps*)** configurados donde el proveedor lo soporte (recordando que una alerta de presupuesto NO detiene el servicio automáticamente).
- [ ] Alertas escalonadas de consumo configuradas (50 %, 80 %, 100 %).
- [ ] Límites de ancho de banda (*egress*), ejecuciones serverless, tamaño de solicitudes/respuestas y techos de auto-scaling (`maxReplicas`) configurados.
- [ ] Protección contra **DDoS / HTTP Flood / abuso** y protección de endpoints costosos verificadas.
- [ ] Caché de contenido estático y CDN configurados correctamente (evitando reprocesamiento innecesario).
- [ ] Procedimiento probado para desactivar temporalmente servicios (**kill switch** / modo mantenimiento) ante ataque o pico de factura.

## 3. Base de datos y almacenamiento (`6` puntos — Bloqueante)
- [ ] **RLS activado** en todas las tablas expuestas por API con políticas `SELECT`, `INSERT`, `UPDATE` y `DELETE` probadas entre usuarios distintos.
- [ ] Permisos de tablas, vistas, funciones/RPCs y buckets de Storage revisados (sin archivos privados públicos).
- [ ] Credenciales privilegiadas (p. ej. `service_role key`) protegidas exclusivamente en backend/bóveda (nunca en frontend) y conexiones cifradas con límites/pool de conexiones.
- [ ] Backups automáticos configurados (BD, archivos/documentos y configuraciones críticas), cifrados, verificando que realmente se generan (y copia *off-site* si el riesgo lo exige).
- [ ] **Restauración de backups probada** con evidencia reciente (RPO y RTO definidos).
- [ ] Políticas de retención/eliminación definidas, índices revisados y ausencia de consultas N+1 o almacenamiento de datos innecesarios.

## 4. IA y servicios externos (`6` puntos — Bloqueante si usa IA de pago)
- [ ] Límites estrictos de llamadas por usuario, tokens de entrada/salida y **máximo de iteraciones por tarea** (`max_iterations`).
- [ ] Presupuesto por usuario/plan de suscripción, presupuesto global y **topes estrictos de gasto** configurados en el proveedor.
- [ ] Timeouts explícitos, reintentos acotados con **backoff exponencial + *jitter*** (cero reintentos infinitos) y fallback/degradación elegante.
- [ ] Protección contra **ciclos recursivos** y bloqueo contra **ejecución concurrente duplicada** de la misma tarea en agentes.
- [ ] Proveedores, versiones de modelo/prompts y APIs externas documentados con API Keys protegidas y registro de tokens/costos/errores sin PII.
- [ ] Validación determinista de respuestas (JSON Schema / sanitización XSS), protección contra *prompt injection* y mínimo privilegio en herramientas (sin acceso administrativo libre; confirmación humana en acciones críticas).

## 5. Legal, privacidad y operación comercial (`7` puntos — Bloqueante)
*(Complementar con el checklist `0/36` de `swe-legal-compliance`.)*
- [ ] Aviso de Privacidad (integral y simplificado según LFPDPPP / jurisdicción aplicable) publicado y consistente con los datos recolectados y terceros receptores.
- [ ] Términos y Condiciones publicados y accesibles sin inicio de sesión (incluyendo uso aceptable y contacto/soporte operativo).
- [ ] Licencias OSS, licencias de assets (imágenes, iconos, fuentes, sonidos) y propiedad intelectual verificadas.
- [ ] Consentimiento granular sin casillas premarcadas, registro inmutable de aceptación y reglas de comunicaciones comerciales / listas de espera (*waitlists*, identificación del remitente y baja/*unsubscribe* operativa).
- [ ] Política de Cookies y bloqueo previo de rastreadores no esenciales antes del consentimiento.
- [ ] Mecanismos operativos para derechos **ARCO**, cancelación de cuenta y eliminación/anonimización de datos.
- [ ] Condiciones transparentes de precios, suscripciones, reembolsos y cancelaciones; si cobra en línea: pasarela PCI-DSS (sin guardar tarjetas), **webhooks verificados**, **idempotencia**, validación en backend y manejo de pagos fallidos.

## 6. Accesibilidad, UX y SEO público (`6` puntos)
- [ ] Navegación completa por teclado (orden lógico `Tab`, menús desplegables y gestión de foco en modales) sin trampas de teclado.
- [ ] Textos alternativos (`alt`) descriptivos en imágenes informativas y `alt=""` en decorativas; atributo `lang` y jerarquía `h1`–`h6` correctos.
- [ ] Etiquetas accesibles (`<label>`) en formularios y nombres accesibles en todos los botones.
- [ ] Contraste suficiente (WCAG 2.2 AA), foco visible, independencia del color y zoom de texto hasta 200 % sin pérdida de contenido.
- [ ] Diseño responsive Mobile First sin scroll horizontal, estados Loading/Empty/Error, confirmaciones de acciones críticas y optimización WebP/AVIF + Core Web Vitals.
- [ ] Mensajes de error comprensibles y, en sitios públicos, SEO/publicación listos (`title`/description/favicon/Open Graph/canónicas, `robots.txt`/`sitemap.xml`, `/admin` con `noindex`, páginas `404`/`500` limpias y cero enlaces rotos).

## 7. Calidad y pruebas (`6` puntos)
- [ ] Pruebas unitarias e integración en lógica crítica y BD/APIs reales (usando datos sintéticos, nunca PII real), ejecutándose en CI en cada PR.
- [ ] Pruebas End-to-End (E2E) o Smoke en los flujos críticos de negocio (registro, login, flujo principal, pagos).
- [ ] Pruebas de seguridad (validación bypass en backend, XSS, SQLi/NoSQLi, IDOR/BOLA, CSRF y Security Headers — p. ej. `swe-browser-audit` / OWASP ZAP).
- [ ] Pruebas de rendimiento, carga y estrés (y comportamiento *offline* / caída de servicios externos cuando corresponda).
- [ ] Compatibilidad verificada en navegadores, dispositivos y redes lentas (3G/4G).
- [ ] Higiene de release verificada: sin errores críticos en consola, sin endpoints de prueba, sin usuarios/contraseñas predeterminados ni datos ficticios en producción.

## 8. Producción y operaciones (`7` puntos)
- [ ] Entornos estrictamente separados (`Local` / `Dev` / `Staging` / `Production`) y modo producción activo (`DEBUG=false`).
- [ ] Dominio, DNS, certificados HTTPS y redirección forzada **HTTP -> HTTPS** configurados y verificados.
- [ ] Cabeceras de seguridad HTTP (`CSP`, `HSTS`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) y `CORS` estricto configurados.
- [ ] Migraciones de base de datos versionadas, probadas en staging y compatibles hacia atrás.
- [ ] Procedimiento de **rollback** probado y despliegue sin interrupción de operaciones críticas.
- [ ] Monitoreo y alertas operativos (uptime, errores 4xx/5xx, CPU/RAM/BD, costos, actividad sospechosa, fallos de auth y fallos de backups — p. ej. Sentry, Uptime Kuma, Grafana).
- [ ] Plan de respuesta ante incidentes, runbooks y (cuando aplique) página de estado / aviso de mantenimiento listos.

## 9. Documentación y entrega (`6` puntos)
*(Para transferencia formal completa, usar el paquete `PROJECT-HANDOVER/` de `swe-project-handover`.)*
- [ ] `README.md`, arquitectura (`ARCHITECTURE.md` / C4), diagramas de infraestructura/BD y ADRs actualizados.
- [ ] Documentación de API (OpenAPI/Swagger) y contratos de error (RFC 9457) al día.
- [ ] Variables de entorno documentadas (`.env.example` / referencia de configuración) sin revelar secretos.
- [ ] Manuales de despliegue, rollback, recuperación (DR), administración y usuario (cuando aplique) disponibles.
- [ ] **SBOM**, inventario de dependencias/servicios externos e inventario de licencias generados y revisados.
- [ ] Responsables, contactos de proveedores, `CHANGELOG.md` y procedimiento de rotación de credenciales documentados.

---

## Matriz de Riesgos (4 niveles)

| Nivel | Significado / Ejemplos | Acción obligatoria |
| :--- | :--- | :--- |
| **Crítico** | Exposición de datos/secretos, acceso administrativo indebido, falta de RLS/IDOR, costos sin límites ni topes. | **Bloquear lanzamiento (No-Go).** |
| **Alto** | Vulnerabilidades importantes, backups sin probar, fallos en operaciones críticas o pagos sin idempotencia/webhooks verificados. | **Corregir antes de publicar.** |
| **Medio** | Problemas de rendimiento, accesibilidad parcial, SEO incompleto o documentación parcial. | **Evaluar y fijar fecha de corrección.** |
| **Bajo** | Detalles visuales y mejoras menores. | **Registrar en backlog.** |

*(Equivalencia ejecutiva en reportes resumidos de `swe-methodology`: `Crítico` -> Crítico; `Alto`/`Medio` -> Importante; `Bajo` -> Recomendado.)*

---

## Matriz de Autorización de Lanzamiento (`Go / No-Go`)

En equipos pequeños una persona puede asumir varios roles, pero **todas las revisiones deben realizarse y quedar registradas** antes de liberar:

| Rol responsable | Ámbito que valida | Decisión (`Go / No-Go`) | Responsable y fecha |
| :--- | :--- | :---: | :--- |
| **Desarrollador / Tech Lead** | Funcionamiento, calidad, pruebas, higiene de release, migraciones y rollback | `[ ] Go  [ ] No-Go` | |
| **Responsable de Seguridad** | Secretos, auth/sesiones, IDOR/BOLA, RLS, dependencias/SCA y cabeceras HTTP | `[ ] Go  [ ] No-Go` | |
| **Responsable de Infraestructura** | Servidores, DNS/HTTPS, DDoS/bots, backups/restore, monitoreo, alertas y límites de costos | `[ ] Go  [ ] No-Go` | |
| **Responsable de Proyecto / Legal** | Privacidad, TyC, cookies, licencias/PI, consentimiento, pagos y aprobación comercial | `[ ] Go  [ ] No-Go` | |
