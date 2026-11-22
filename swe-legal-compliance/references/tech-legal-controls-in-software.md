# Controles Técnico-Legales dentro del Software (Puntos 10 y 11)

El cumplimiento legal no se resuelve solo colgando un PDF en el pie de página: el software debe implementar controles verificables que respalden lo prometido en el Aviso de Privacidad y los Términos y Condiciones.

---

## 1. Consentimiento granular y sin patrones oscuros (*Dark Patterns*)
* **Cero casillas premarcadas:** los checkboxes de aceptación de Términos/Privacidad, finalidades secundarias (marketing/newsletter) y cookies no esenciales deben iniciar siempre **desmarcados** (`checked = false`).
* **Separación estricta:** nunca mezcles en una sola casilla obligatoria la aceptación del servicio con el consentimiento para publicidad o cesión de datos a terceros.
* **Bloqueo previo en cookies/rastreadores:** ningún script de analítica publicitaria o pixel de terceros debe dispararse antes de que el usuario otorgue su consentimiento expreso (las cookies estrictamente necesarias de sesión/seguridad/CSRF sí pueden cargarse).
* **Simetría de decisión:** los botones *"Aceptar"* y *"Rechazar / Solo necesarias"* deben tener jerarquía visual y accesibilidad equivalentes.
* **No destruir formularios al consultar textos legales:** todo enlace a Términos, Aviso de Privacidad o Política de Cookies dentro de un formulario de registro, checkout o lista de espera **debe abrirse en nueva pestaña (`target="_blank" rel="noopener noreferrer"`) o en un modal accesible sin desmontar el formulario**, evitando que el usuario pierda los datos ya capturados.

---

## 1.5 Paridad obligatoria entre `LEGAL-DOCS/` y las páginas públicas de la app
* **Prohibido publicar resúmenes improvisados de 2–4 líneas** en `/privacidad`, `/terminos` o `/cookies`. La UI pública debe reflejar de forma íntegra y estructurada el contenido de `LEGAL-DOCS/`:
  * **Aviso de Privacidad (`/privacidad`):** identidad, domicilio y contacto del responsable; **tabla completa de datos personales recabados** (categoría, finalidad primaria vs. secundaria, retención y base legal); **transferencias y proveedores terceros** (hosting, BD, CDN, correo, IA y país/región); **procedimiento paso a paso y plazos legales ARCO**; revocación y mecanismo de notificación de cambios.
  * **Términos y Condiciones (`/terminos`):** alcance del servicio, elegibilidad/edad, uso aceptable y prohibiciones, propiedad intelectual, precios/cancelaciones/reembolsos (si aplica), limitación de responsabilidad, soporte y ley/jurisdicción aplicable.
  * **Política de Cookies (`/cookies`):** explicación clara de cookies y almacenamiento local (`localStorage`), **tabla concreta** (nombre exacto, proveedor, tipo esencial/opcional, finalidad y duración), cómo gestionarlas o revocarlas y enlace al banner/preferencias.
* Mientras existan marcadores legales pendientes de llenado o validación jurídica, mostrar claramente el estado de borrador antes de abrir cobros o tráfico comercial masivo.

---

## 2. Registro inmutable de aceptación y evidencia electrónica (Punto 11 / NOM-151)
Cada vez que un usuario acepta Términos y Condiciones, Aviso de Privacidad, Política de Cookies o un contrato B2B, el backend debe registrar un evento **append-only** (nunca sobrescribir aceptaciones anteriores) siguiendo [ACCEPTANCE_AUDIT_LOG_SCHEMA.json](../examples/ACCEPTANCE_AUDIT_LOG_SCHEMA.json):

* `acceptance_id`: UUID único del registro.
* `subject_id`: identificador interno del usuario/cuenta (o identificador pseudonimizado en formularios públicos).
* `document_type`: `terms_of_service` | `privacy_notice` | `cookie_policy` | `dpa` | `subscription_renewal`.
* `document_version`: versión semántica o fechada (p. ej. `2026-01-15` o `v2.1.0`).
* `document_sha256`: hash criptográfico `SHA-256` del texto exacto exhibido al usuario al momento de aceptar.
* `accepted_at_utc`: timestamp ISO 8601 en UTC generado por el **servidor** (nunca confiar en el reloj del cliente).
* `consent_scope`: objeto booleano granular (p. ej. `primary_purposes`, `marketing`, `analytics_cookies`).
* `evidence`: `ip_hash` o IP según retención legal, `user_agent`, `locale`, `source_channel` (`web`, `ios`, `android`, `api`) y, en Nivel 3 / contratos de alto valor, referencia `nom151_psc_constancia_id` emitida por un PSC acreditado bajo **NOM-151-SCFI-2016**.

---

## 3. Centro de Privacidad y Flujo de Derechos ARCO
Implementar un módulo o sección accesible desde la configuración de cuenta (y un canal público para ex-usuarios o no registrados):

1. **Acceso y Portabilidad (Exportación):** permitir descargar un paquete legible por máquina (`JSON` o `CSV`) con los datos personales del titular previa verificación de identidad (re-autenticación o enlace firmado con TTL corto).
2. **Rectificación:** permitir editar datos personales propios desde el perfil o solicitar corrección de datos verificados (con bitácora de cambio).
3. **Cancelación y Eliminación de cuenta:**
   * Flujo autoservicio visible (sin obligar a llamadas telefónicas o correos manuales innecesarios si el alta fue digital).
   * Confirmación explícita de consecuencias irreversibles.
   * **Eliminación real o anonimización criptográfica** en BD principal, índices de búsqueda y colas, respetando únicamente bloqueos de retención legal obligatoria (p. ej. comprobantes fiscales CFDI o bitácoras antifraude exigidas por ley, debidamente aislados y con fecha de purga).
4. **Oposición y Revocación:** interruptores (*toggles*) para desactivar correos promocionales, perfilamiento secundario o cookies opcionales con efecto inmediato y persistido en el historial de consentimiento.
5. **Trazabilidad de solicitudes ARCO:** generar un folio único, fecha de recepción UTC y alertas internas para responder dentro del plazo legal vigente.

---

## 4. Transparencia en cobros, suscripciones y cancelación (LFPC 76 Bis / 76 Bis 1)
* Mostrar **precio final desglosado** (subtotal, IVA/impuestos, moneda y periodicidad) antes del botón definitivo de pago.
* Enviar comprobante de compra/suscripción con acceso a facturación (CFDI) y enlace a políticas vigentes.
* En suscripciones con renovación automática: enviar aviso previo configurable antes del cobro y ofrecer botón **"Cancelar suscripción"** en pocos clics dentro de la cuenta, mostrando la fecha exacta hasta la cual conserva acceso.

---

## 5. Control de edad y protección de menores
* Si el servicio **no** está dirigido a menores de edad: incorporar declaración/verificación de mayoría de edad acorde a la jurisdicción antes de crear cuenta y cláusula de baja inmediata si se detecta uso por menores sin autorización.
* Si el servicio **sí** permite menores (EdTech, videojuegos, etc.): activar privacidad máxima por defecto (perfiles privados, cero publicidad comportamental), consentimiento parental verificable y aplicar además `swe-domain-discovery`.

---

## 6. Versionado de textos legales y re-aceptación
* Versionar cada documento legal en Git (junto con su hash `SHA-256`) y mantener accesible el historial de versiones publicadas.
* Cuando exista un cambio **sustancial** (nuevas finalidades de datos, nuevas transferencias, cambio de tarifas/condiciones), notificar con antelación razonable y solicitar re-aceptación registrada en el siguiente inicio de sesión o antes de aplicar las nuevas condiciones.

---

## 7. Comunicaciones comerciales, marketing y listas de espera (*Waitlists*)
* **Listas de espera y formularios de captura:** no basta con pedir un correo electrónico y asumir permiso indefinido para enviar publicidad. Explica qué tipo de avisos recibirá el usuario (p. ej. solo aviso de lanzamiento vs. boletines promocionales) y usa una casilla de consentimiento separada y desmarcada cuando incluya fines comerciales secundarios.
* **Requisitos mínimos antes de enviar mensajes (correo, SMS, WhatsApp):**
  * Obtener la autorización/consentimiento aplicable y registrar **cuándo y cómo** se obtuvo.
  * Identificar claramente al remitente y respetar las políticas de cada canal (**WhatsApp Business, SMS, correo electrónico**) y la legislación del país del destinatario (p. ej. LFPDPPP/LFPC en México; reglas específicas como TCPA/CAN-SPAM en EE. UU. o GDPR/ePrivacy en UE si hay destinatarios en esas jurisdicciones).
  * Incluir un mecanismo funcional y visible para **cancelar suscripciones (*unsubscribe*)** y respetar las bajas de inmediato.
  * No reutilizar datos capturados para finalidades incompatibles ni **comprar o importar listas de contactos** sin verificar su procedencia legítima y base legal.
