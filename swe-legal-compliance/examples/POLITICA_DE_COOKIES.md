# Política de Cookies y Tecnologías Similares — [Nombre del Proyecto]

> **BORRADOR BASE — REQUIERE REVISIÓN LEGAL:** Ajusta esta plantilla al inventario real de cookies/SDKs de tu aplicación y valídala con un abogado antes de publicar.

- **Versión:** `[v1.0.0]`
- **Última actualización:** `[YYYY-MM-DD]`

---

## 1. Qué son las cookies y cómo las usamos
Las cookies y tecnologías similares (`localStorage`, `sessionStorage`, identificadores de sesión) son pequeños archivos que se almacenan en su navegador o dispositivo para permitir el funcionamiento seguro de **[Nombre del Proyecto]**, recordar preferencias y —únicamente con su consentimiento previo— medir el rendimiento del sitio.

## 2. Clasificación de cookies utilizadas

| Categoría | Consentimiento previo | Finalidad |
| :--- | :-: | :--- |
| **Estrictamente necesarias** | No *(indispensables)* | Autenticación de sesión (`HttpOnly`), protección CSRF, balanceo de carga y recordar su elección de cookies. |
| **Preferencias / Funcionales** | Sí *(opcional)* | Recordar idioma, zona horaria o tema visual elegido. |
| **Analítica y rendimiento** | Sí *(opcional)* | Medir uso agregado y detectar errores/cuellos de botella de forma minimizada. |
| **Publicidad / Marketing** | Sí *(opcional)* | `[Indicar "No utilizamos cookies publicitarias de terceros" O describirlas claramente]`. |

## 3. Inventario real de cookies y almacenamiento cliente
*(Completa únicamente con las cookies que la aplicación realmente emite; verifica con `swe-browser-audit`.)*

| Nombre | Proveedor | Categoría | Duración | Propósito |
| :--- | :--- | :--- | :--- | :--- |
| `[session_id]` | Propia (`[tu-dominio.com]`) | Estrictamente necesaria | `[Sesión / 7 días]` | Mantener la sesión autenticada (`HttpOnly`, `Secure`, `SameSite=Lax`). |
| `[cookie_consent]` | Propia (`[tu-dominio.com]`) | Estrictamente necesaria | `[6 meses]` | Guardar las preferencias de consentimiento del usuario. |
| `[analytics_id]` | `[Proveedor o N/A]` | Analítica | `[Ej. 90 días]` | Métricas agregadas de navegación (solo si fue aceptada). |

## 4. Cómo gestionar o revocar su consentimiento
* **Sin casillas premarcadas:** las categorías opcionales permanecen desactivadas hasta que usted las acepte expresamente en el banner o en el **Centro de Privacidad**.
* **Revocación en cualquier momento:** puede modificar o retirar su consentimiento desde el enlace **"Preferencias de cookies"** en el pie de página del sitio o desde la configuración de su navegador.
* **Contacto:** para dudas sobre esta política, escriba a `[privacidad@tu-dominio.com]`.
