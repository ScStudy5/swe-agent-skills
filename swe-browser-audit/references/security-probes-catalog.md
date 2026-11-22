# Catálogo de Sondas y Criterios de Auditoría con Playwright

> **Uso exclusivo en `localhost` o entornos `staging`/QA propios con datos de prueba.** Nunca ejecutes pruebas activas sobre producción con usuarios reales ni sobre dominios de terceros.

---

## 1. Auditoría pasiva: qué verificar en cada carga de página

### Consola y Red
* **Fallo esperado = 0:** no deben existir `console.error`, `pageerror` ni recursos rotos (`404`/`500`).
* **Fuga de errores internos:** buscar en respuestas HTTP/HTML/JSON cadenas como `SQLSTATE`, `SyntaxError`, `pg_`, `mysql_`, `Traceback (most recent call last)`, `System.Data.SqlClient`, rutas locales (`C:\Users\`, `/var/www/`).
* **PII excesiva:** validar que endpoints de listado no devuelvan campos innecesarios (`passwordHash`, `tokens`, teléfonos/CURP/direcciones de otros usuarios).

### Security Headers esperados
| Header | Objetivo |
| :--- | :--- |
| `Content-Security-Policy` | Mitigar XSS restringiendo orígenes de scripts/estilos/frames. |
| `X-Content-Type-Options: nosniff` | Evitar MIME-sniffing. |
| `X-Frame-Options` o CSP `frame-ancestors` | Prevenir Clickjacking. |
| `Strict-Transport-Security` | Forzar HTTPS (en entornos HTTPS/producción). |
| `Referrer-Policy` | Limitar fuga de URLs/parámetros sensibles en `Referer`. |
| `Permissions-Policy` | Restringir APIs del navegador (cámara, micrófono, geolocalización). |

### Cookies y Storage
* Cookies de sesión/auth: deben marcar **`HttpOnly`** (no accesibles desde `document.cookie`), **`Secure`** (en HTTPS) y **`SameSite=Lax`** o **`Strict`**.
* `localStorage` / `sessionStorage`: evitar guardar tokens de sesión de alto privilegio o claves de API si pueden gestionarse mediante cookies `HttpOnly`.

---

## 2. Sondas seguras de validación y ataque controlado

> **Cobertura del script `playwright_security_audit.mjs` (`--probe-forms`):** automatiza sondas de longitud límite (1,200 chars), Unicode/control, XSS DOM/img/svg (`AUDIT_XSS_TEXT_<b>probe</b>`, `<img>`, `<svg>`), SQLi básico (`' OR '1'='1`, `'`), NoSQLi (`{"$ne":null}`) y Path Traversal (`../../../../etc/passwd`) en formularios. Las pruebas de **CRLF, `javascript:` en URLs, Open Redirect, campos vacíos/tipos específicos, Auth Bypass, IDOR y CSRF** requieren ejecución dirigida manual o con MCP/subagente de navegador.

### A. Validación de límites y bypass de cliente
Probar en cada formulario (deshabilitando validación HTML o enviando vía `fetch`/API desde el contexto de prueba):
1. Campos obligatorios vacíos o solo espacios (`"   "`). *(Manual / dirigido)*
2. Strings muy largos (1,200 caracteres automatizado en script; probar hasta 5,000+ en campos críticos manualmente) para detectar falta de `maxLength` en servidor o `500`.
3. Tipos incorrectos en campos numéricos/fechas/emails (`"abc"`, `"9999-99-99"`, `"-1"` en cantidades/precios). *(Manual / dirigido)*
4. Caracteres Unicode especiales, emojis (`\u0000\u202E💥`, automatizado) y saltos de línea (`"test\r\nHeader: injected"` para CRLF, manual/dirigido).

### B. Sondas inocuas de XSS (Reflejado / Almacenado / DOM)
Inyectar marcadores únicos rastreables (sin efectos dañinos) y comprobar si se ejecutan o se insertan sin escapar:
* `AUDIT_XSS_TEXT_<b>probe</b>` *(automatizado en script; comprueba si la etiqueta `<b>` se renderiza como elemento HTML real en el DOM)*
* `"><img src=x onerror="window.__auditXssTriggered='img'">` *(automatizado en script)*
* `<svg onload="window.__auditXssTriggered='svg'">` *(automatizado en script)*
* `javascript:void(window.__auditXssTriggered='href')` *(manual / dirigido solo en campos de URL/enlace)*

**Criterio de fallo:** `window.__auditXssTriggered` cambia de valor, se dispara `page.on('dialog')`, o el nodo HTML inyectado aparece como elemento DOM en vez de texto escapado.

### C. Sondas seguras de SQLi / NoSQLi (Solo detección, nunca destructivas)
Enviar en buscadores, filtros, login y parámetros URL:
* `' OR '1'='1`
* `" OR "1"="1`
* `'; --`
* `1' AND '1'='2`
* `{"$ne": null}` *(en payloads JSON si el backend usa NoSQL)*

**Criterio de fallo:** el servidor responde `500`, expone mensajes de error de base de datos, tarda anómalamente o devuelve más registros/acceso autorizado cuando no debería. El resultado correcto es `400/422` o búsqueda literal vacía.

### D. Sondas de Path Traversal / Open Redirect
* En parámetros de archivo/descarga: `../../etc/passwd` o `..\windows\win.ini` (esperado: `400/403/404`).
* En parámetros `?redirect=` / `?next=` / `?returnTo=`: `https://evil.example.com` o `//evil.example.com` (esperado: rechazo o redirección interna únicamente).

### E. Control de acceso (Auth Bypass, IDOR y CSRF)
1. **Sin sesión:** abrir rutas privadas y llamar endpoints privados sin cookies ni `Authorization` (esperado: `401` o redirección a login sin filtrar datos en el HTML inicial).
2. **IDOR (Broken Object Level Authorization):** autenticado como Usuario A, solicitar `/api/orders/<ID_DE_B>` o editar un formulario cambiando un ID oculto a un recurso del Usuario B (esperado: `403` o `404`).
3. **CSRF:** enviar una petición `POST`/`PUT`/`DELETE` con sesión por cookie desde un origen distinto o sin token CSRF (esperado: rechazo `403`).

---

## 3. Cuándo complementar con OWASP ZAP
Playwright audita todo lo accesible desde la UI, formularios, consola, cookies y peticiones del navegador. Usa además **OWASP ZAP** (en CI o staging) cuando necesites:
* Fuzzing exhaustivo de rutas API no enlazadas desde la UI.
* Pruebas profundas de configuración TLS/cifrado.
* Escaneo automatizado completo contra OWASP Top 10 / API Security Top 10.
