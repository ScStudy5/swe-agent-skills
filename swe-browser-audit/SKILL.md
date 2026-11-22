---
name: swe-browser-audit
description: >-
  Auditoría dinámica profesional en navegador real con Playwright sobre localhost o
  staging autorizado: inspecciona código cliente, consola, peticiones HTTP, Security
  Headers, cookies, storage, accesibilidad (axe-core), responsive y ejecuta pruebas
  controladas de validación de campos, XSS, sondas seguras de SQLi/NoSQLi, CSRF e
  IDOR. Usar para auditar seguridad y calidad funcional en vivo (para revisión
  estática de código, arquitectura o privacidad en repositorio usar swe-security-privacy).
---

# Auditoría Dinámica y Seguridad en Navegador (Playwright)

Aplica esta skill para probar una aplicación web en ejecución (`localhost`, entorno efímero o `staging`) combinando QA funcional avanzado, revisión frontend/red y pruebas activas de seguridad controladas.

## Regla fundamental de seguridad y alcance
* **Solo entornos autorizados:** ejecuta estas pruebas únicamente contra `localhost` o entornos `staging`/QA propios con **base de datos de pruebas**. Nunca apuntes contra producción con datos reales ni contra sitios de terceros.
* **Sondas no destructivas:** usa exclusivamente marcadores de detección y payloads seguros; **prohibido** lanzar sentencias destructivas (`DROP`, `DELETE` masivo, denegación de servicio).
* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto para priorizar los hallazgos sin exigir controles desproporcionados en un MVP.

## Flujo de trabajo

### 1. Pre-flight del entorno objetivo
1. Confirma la URL objetivo (`http://localhost:...` o staging autorizado), rutas principales y si hay credenciales de prueba para dos roles/usuarios (necesario para probar **IDOR / Control de acceso**).
2. Verifica si `playwright` está disponible en el proyecto objetivo o globalmente (o usa el servidor MCP / subagente de navegador si tu entorno lo provee).
3. Consulta el catálogo completo de sondas y criterios en [security-probes-catalog.md](./references/security-probes-catalog.md).

### 2. Auditoría pasiva en vivo (Frontend, Consola, Red y Headers)
Ejecuta el script base [playwright_security_audit.mjs](./scripts/playwright_security_audit.mjs) desde el directorio del proyecto objetivo (resolviendo la ruta real de esta skill):

```bash
# Auditoría pasiva en localhost (default)
node <ruta-de-la-skill>/scripts/playwright_security_audit.mjs http://localhost:3000 \
  --routes /,/login --out audit-report.json

# Con sondas activas seguras en entorno de pruebas (agrega --allow-remote solo para staging autorizado)
node <ruta-de-la-skill>/scripts/playwright_security_audit.mjs http://localhost:3000 \
  --routes /,/login --probe-forms --max-forms 10 --out audit-report.json
```

*Códigos de salida del script:* `0` completado, `1` error de argumentos/ejecución, `2` objetivo rechazado (protocolo no `http/https` o host remoto sin `--allow-remote`), `3` `playwright` no encontrado (en ese caso, replica estos pasos con el MCP/subagente de navegador o instala `playwright` en el proyecto).

Comprobaciones cubiertas:
1. **Consola y errores JS:** captura `console.error`, `pageerror` y promesas no manejadas al navegar por cada ruta.
2. **Tráfico de red y respuestas:** detecta peticiones fallidas (`4xx`/`5xx`), respuestas que filtren *stack traces*, mensajes de error SQL/ORM, rutas internas del servidor o PII innecesaria.
3. **Security Headers HTTP:** verifica presencia de `Content-Security-Policy`, `Strict-Transport-Security` (en HTTPS), `X-Content-Type-Options`, `X-Frame-Options` / `frame-ancestors`, `Referrer-Policy` y `Permissions-Policy` sobre la respuesta final tras redirecciones (y revisa manualmente la fortaleza de directivas CSP/HSTS).
4. **Cookies y almacenamiento cliente:** revisa que las cookies de sesión tengan `HttpOnly`, `Secure` (en HTTPS) y `SameSite`; inspecciona claves de `localStorage`/`sessionStorage` (sin imprimir valores) para detectar tokens sensibles o secretos expuestos a XSS.
5. **Código fuente expuesto en cliente:** detecta *sourcemaps* (`.map`) servidos o referenciados vía `sourceMappingURL` públicamente con HTTP `200`, claves privadas o endpoints administrativos filtrados en bundles JS.
6. **Responsive y Accesibilidad real:** valida desktop (`1440x900`) y mobile (`390x844`) buscando desbordamiento horizontal (`scrollWidth > innerWidth`) y ejecuta **axe-core** sobre el DOM renderizado si `@axe-core/playwright` está instalado.

### 3. Pruebas activas de robustez y seguridad (Pentest funcional controlado)
Ejecuta `--probe-forms` (en entorno de pruebas) o realiza pruebas dirigidas por flujo. El script omite por defecto formularios de borrado/pago/logout (usa `--include-risky-forms` solo con datos sintéticos) y limita `--max-forms 10` por ruta. **IDOR, Auth Bypass, CSRF, Open Redirect y payloads CRLF/URL no están automatizados**: ejecútalos manualmente o con el MCP/subagente de navegador.
1. **Validación de todos los campos (cliente + bypass hacia backend):** envía valores vacíos, longitudes extremas, tipos erróneos, caracteres Unicode/control y peticiones directas saltando atributos HTML (`required`, `maxlength`, `pattern`) para confirmar que **el servidor** valida y responde `400/422` limpio.
2. **XSS (Reflejado, Almacenado y DOM):** inyecta los marcadores inocuos de [security-probes-catalog.md](./references/security-probes-catalog.md) en inputs, parámetros URL y fragmentos `#`; verifica que no se ejecute ningún diálogo/handler y que el texto aparezca escapado (no como HTML ejecutable).
3. **Sondas seguras de SQLi / NoSQLi / Path Traversal:** envía sondas de detección no destructivas en campos de búsqueda, filtros, login y parámetros; falla la auditoría si el servidor responde `500`, expone errores de sintaxis SQL/base de datos o altera la autorización.
4. **Control de acceso (IDOR / Auth Bypass / CSRF):**
   * Intenta acceder a rutas y endpoints privados sin sesión.
   * Autenticado como **Usuario A**, intenta leer o modificar un recurso por ID del **Usuario B** (`403/404` esperado).
   * Verifica protección CSRF / validación de `Origin` en acciones que cambian estado.

### 4. Reporte y escalamiento a DAST profundo
Entrega hallazgos clasificados en **Crítico / Alto / Medio / Bajo** (equivalencia ejecutiva en `swe-methodology`: `Crítico` -> Crítico; `Alto`/`Medio` -> Importante; `Bajo` -> Recomendado) con URL redactada, campo/endpoint afectado, evidencia observada y remediación concreta.
Cuando necesites fuzzing masivo de endpoints ocultos, SSL/TLS o escaneo DAST exhaustivo fuera de lo visible en navegador, complementa esta auditoría ejecutando **OWASP ZAP** contra `staging`.

## Criterios de verificación
* Todas las pruebas activas se ejecutaron únicamente contra `localhost` o `staging` autorizado con datos sintéticos.
* Se revisaron consola, red, headers, cookies/storage, sourcemaps, formularios, control de acceso y vista móvil/escritorio.
* Ningún reporte imprime valores completos de tokens, contraseñas ni parámetros sensibles de query string.
