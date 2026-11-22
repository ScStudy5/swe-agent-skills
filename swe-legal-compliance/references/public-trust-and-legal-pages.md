# Estándar Adaptable de Páginas Institucionales, Legales, Confianza y Footer

> **Regla anti-plantilla ciega:** ningún proyecto debe copiar 50 políticas corporativas que no puede cumplir ni copiar textos idénticos de otra aplicación. Selecciona **únicamente las páginas que aplican** según el **Nivel (`N1 / N2 / N3`)** y los **activadores reales del proyecto**, y redacta cada una con los **datos, proveedores, flujos y vigencia reales** de esa aplicación.

---

## 1. Matriz de selección por Nivel y Activador del proyecto

### Nivel 1 — Base (cualquier sitio web público o MVP)
| Página / Ruta sugerida | Cuándo incluirla | Contenido mínimo real |
| :--- | :--- | :--- |
| **Acerca de** (`/acerca`) | Siempre | Quién desarrolla/opera el proyecto, propósito, actividad principal y canales oficiales. |
| **Contacto** (`/contacto` o `/soporte`) | Siempre | Correo oficial, formulario de contacto, motivo de consulta, tiempo estimado de respuesta y horarios (si existen). |
| **Aviso de Privacidad** (`/privacidad`) | Si captura cualquier dato personal (incluso formularios de contacto o *waitlist*) | Modalidad integral y simplificada conforme a legislación vigente (en México, LFPDPPP vigente y autoridad garante federal): responsable, domicilio, tabla de datos, finalidades primarias vs. secundarias, transferencias, derechos ARCO, revocación y cambios. |
| **Términos y Condiciones** (`/terminos`) | Si ofrece una aplicación, cuenta o servicio digital | Identificación, aceptación, alcance, uso permitido/prohibido, propiedad intelectual, disponibilidad, responsabilidades, legislación y contacto. |
| **Política de Cookies** (`/cookies`) | Si usa cookies, sesiones o rastreadores | Qué son, inventario exacto (nombre, categoría, finalidad, duración), consentimiento previo para no esenciales y panel/enlace **«Gestionar Cookies»**. |
| **Declaración de Accesibilidad** (`/accesibilidad`) | Siempre en sitios públicos | Estándar objetivo (**WCAG 2.2 AA**), nivel realmente evaluado, fecha de última auditoría, barreras conocidas y canal para reportar problemas de accesibilidad. |

### Nivel 2 — Aplicación funcional (web apps, PWAs, SaaS con cuentas)
Incluye todo lo de **Nivel 1**, más:

| Página / Ruta sugerida | Cuándo incluirla | Contenido mínimo real |
| :--- | :--- | :--- |
| **Centro de Ayuda y FAQ** (`/soporte` o `/ayuda`) | Siempre en N2+ | Preguntas frecuentes, guías rápidas, solución de problemas comunes, requisitos técnicos y canal con folio/SLA. |
| **Documentación** (`/docs`) | Apps complejas, APIs o herramientas técnicas | Funcionalidades, instrucciones de uso, limitaciones conocidas, API (OpenAPI) y registro de cambios/novedades. |
| **Estado del servicio** (`/estado` o en `/soporte`) | Aplicaciones en línea y APIs | Disponibilidad en vivo (`/healthz`), incidentes activos, mantenimientos programados e historial de incidencias. |
| **Política de Seguridad** (`/seguridad`) + **`/.well-known/security.txt`** | Siempre en N2+ | Canal de reporte de vulnerabilidades, divulgación responsable, alcance permitido, prohibición de pruebas destructivas y archivo estándar **RFC 9116** en `public/.well-known/security.txt`. |
| **Eliminación de cuentas y «Su elección de privacidad»** (`/panel` + `/privacidad#arco`) | Siempre que existan cuentas | Procedimiento claro de eliminación autoservicio y con folio, qué datos se borran, qué se conserva por obligación legal, plazos y gestión de opt-out/ARCO. |
| **Subprocesadores / Terceros** (`/subprocesadores` o sección dedicada) | Siempre que use proveedores externos | Lista real de proveedores (hosting, BD, CDN, correo, pagos, IA), función, datos tratados, transferencias internacionales y enlaces a sus políticas. |
| **Política de Uso Aceptable (AUP)** | Plataformas, APIs y apps multiusuario | Conductas prohibidas (abuso, bots/scraping, malware, suplantación, intentos de intrusión) y procedimiento de suspensión/apelación. |

### Nivel 3 — Condicionales por modelo de negocio o módulo (activar SOLO si el proyecto tiene ese módulo)
| Activador del proyecto | Páginas / políticas específicas a generar |
| :--- | :--- |
| **Cobra dinero, ventas o suscripciones** | **Política de Reembolsos y Cancelaciones** (LFPC arts. 76 Bis / 76 Bis 1 en México), información transparente de planes/renovaciones, garantías/entregas (e-commerce), **SLA** y contratos B2B (**DPA / MSA / EULA**). |
| **Integra Inteligencia Artificial / LLMs / Agentes** | **Política de Transparencia y Uso de IA (`/politica-ia`)**: qué funciones usan IA, proveedores usados, qué datos se envían (y cuáles NO), si se entrena o no con datos del usuario, limitaciones/errores posibles, supervisión humana y cómo reportar una salida incorrecta. |
| **Aloja contenido generado por usuarios / comunidad** | **Política de Comunidad / Moderación**, **Política de Contenido**, procedimiento de retiro por infracción de **Propiedad Intelectual / DMCA** (aviso y contranotificación) y apelaciones. |
| **Accesible a menores de edad** | **Política de Menores**: restricciones de edad, privacidad máxima por defecto, cero publicidad comportamental y consentimiento parental verificable. |
| **Distribuye software, SDK o código abierto** | **Licencia de Software** explícita (propietaria o OSS como MIT/Apache-2.0) y avisos de licencias de terceros (sin confundir licencia con Términos del Servicio). |
| **Publicidad o enlaces de afiliados** | **Política de Anuncios** y **Divulgación de Afiliados**. |

---

## 2. Arquitectura estándar de Footer por categorías

Organiza el pie de página en columnas claras mostrando **únicamente los enlaces activos** para el nivel y módulos del proyecto:

```text
Producto                 Soporte                     Legal                        Confianza y Privacidad
- Acerca de              - Centro de ayuda / FAQ     - Términos y condiciones     - Política de seguridad
- Documentación / Guías  - Contacto / Reportar bug   - Aviso de privacidad        - Declaración de accesibilidad
- Novedades / Changelog  - Estado del servicio       - Política de cookies        - Subprocesadores / Terceros
                                                     - Licencias / PI             - Política de IA (si aplica)
                                                     - Reembolsos (si cobra)      - Gestionar Cookies
                                                                                  - Su elección de privacidad
```

* **Accesos directos recomendados en el footer (patrón SaaS moderno):**
  1. **`Gestionar Cookies`:** abre directamente el panel de preferencias de cookies desde cualquier página.
  2. **`Su elección de privacidad`:** lleva directamente al centro de privacidad/ARCO, opt-out de marketing/analítica y eliminación de cuenta.

---

## 3. Archivo estándar `public/.well-known/security.txt` (RFC 9116)

En proyectos **Nivel 2 y 3**, publica el archivo de texto plano en `/.well-known/security.txt` con fecha de expiración renovable:

```text
Contact: mailto:seguridad@[tu-dominio.com]
Expires: 2027-11-22T00:00:00.000Z
Preferred-Languages: es, en
Canonical: https://[tu-dominio.com]/.well-known/security.txt
Policy: https://[tu-dominio.com]/seguridad
```

---

## 4. Regla de adaptación por proyecto (cero copy-paste)
Antes de publicar cualquier página de esta matriz, verifica que:
1. Cada proveedor listado en **Subprocesadores** y **Aviso de Privacidad** corresponde al stack real desplegado (no dejes nombres de otro proyecto ni niegues compartir datos si usas servicios externos).
2. Los enlaces legales dentro de formularios abren en **`target="_blank" rel="noopener noreferrer"`** o modal sin perder progreso.
3. Cada documento incluye **versión, fecha de vigencia** e historial de cambios, y cuenta con revisión jurídica/contable antes de operar comercialmente.
