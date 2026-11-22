# Seguridad, DevSecOps, Privacidad y Cadena de Suministro

## 1. Seguridad y DevSecOps

### Principio fundamental
La seguridad no debe agregarse al final. Debe formar parte de todo el ciclo de desarrollo (**SSDLC**).

| Buena práctica | Descripción |
| :--- | :--- |
| **DevSecOps** | Integrar seguridad en desarrollo, pruebas y despliegue. |
| **SSDLC** | Ciclo de vida de desarrollo seguro. |
| **Threat Modeling** | Identificar amenazas antes de implementar. |
| **Security by Design** | Diseñar considerando la seguridad desde el inicio. |
| **Least Privilege** | Dar únicamente los permisos estrictamente necesarios. |
| **Zero Trust** | No confiar automáticamente en usuarios, dispositivos o servicios. |
| **MFA** | Autenticación multifactor (especialmente obligatoria para cuentas administrativas y operaciones sensibles). |
| **RBAC** | Control de acceso basado en roles. |
| **ABAC** | Control de acceso basado en atributos cuando sea necesario. |
| **IDOR / BOLA** | Verificar autorización por recurso y propietario en cada endpoint (nunca confiar en el ID recibido; probar acceso cruzado entre Usuario A y Usuario B). |
| **OAuth 2.0 / OpenID Connect** | Gestionar autorización y autenticación mediante protocolos apropiados. |
| **Autenticación, cuentas y sesiones** | Verificar correo cuando corresponda, recuperación segura de contraseñas (tokens de un solo uso con TTL corto), **anti-enumeración de cuentas** (no revelar si un correo está registrado en mensajes de error), cookies (`HttpOnly`, `Secure`, `SameSite`), expiración de sesiones, **invalidación en servidor al cerrar sesión**, **revocación inmediata de sesiones comprometidas** y evitar tokens permanentes. |
| **Row Level Security (RLS) y BaaS** | En bases de datos expuestas por API (p. ej. PostgreSQL/Supabase): activar **RLS** en todas las tablas expuestas, definir políticas explícitas `SELECT`/`INSERT`/`UPDATE`/`DELETE`, probar acceso cruzado entre usuarios, revisar permisos de vistas/funciones/Storage y **nunca exponer `service_role` key en el frontend** (la clave pública `anon`/`publishable` no es un secreto; la seguridad depende de RLS y permisos). Regla: *tener autenticación no significa que la BD esté protegida*. |
| **Cifrado en tránsito** | Usar TLS/HTTPS en todas las comunicaciones con redirección forzada **HTTP -> HTTPS**. |
| **Cifrado en reposo** | Proteger información almacenada sensible y claves criptográficas. |
| **Gestión de secretos** | Nunca subir contraseñas, API keys o certificados al repositorio ni exponerlos en el frontend; usar variables de entorno separadas por ambiente, gestores de secretos y **revocar/rotar claves** de inmediato ante cualquier sospecha. |
| **Precios y reglas críticas en servidor** | Recalcular precios, descuentos, totales, límites y permisos siempre en servidor desde fuentes confiables (nunca confiar en valores enviados por el cliente). |
| **Sin modo depuración ni archivos expuestos** | Desactivar `DEBUG` en producción, eliminar endpoints de prueba y credenciales predeterminadas, no exponer `.git/`, `.env`, dumps `.sql`, `.map` privados ni buckets públicos, y limitar tamaño/tipo de archivos subidos. |
| **Higiene de bundle cliente y consola en producción** | En monorepos/paquetes compartidos, **nunca importar hacia el frontend datos sensibles o claves de negocio** (respuestas correctas, reglas antifraude, márgenes internos o credenciales) que queden legibles en DevTools/Sources; eliminar trazas `console.*`/`debugger` en builds de producción (ej. `drop: ['console', 'debugger']`) y desactivar sourcemaps públicos (`sourcemap: false`). |
| **Enlaces y tokens que caducan** | Usar URLs firmadas y tokens de recuperación/descarga con expiración corta (TTL) y de un solo uso cuando corresponda. |
| **Gestión de vulnerabilidades** | Detectar, priorizar y corregir vulnerabilidades con SLA definido. |
| **SAST** | Analizar código fuente en busca de problemas de seguridad. |
| **DAST** | Analizar aplicaciones en ejecución contra ataques reales. |
| **SCA** | Analizar dependencias y componentes de terceros. |
| **Secret Scanning** | Detectar credenciales expuestas en commits y archivos. |
| **Container Scanning** | Revisar imágenes y contenedores. |
| **IaC Scanning** | Revisar configuraciones de infraestructura como código. |
| **SBOM** | Generar inventario formal de componentes y dependencias (*Software Bill of Materials*). |
| **Security Headers** | Configurar encabezados HTTP de seguridad (CSP, HSTS, X-Content-Type-Options, etc.). |
| **Rate Limiting** | Evitar abuso y fuerza bruta en endpoints. |
| **Input Validation** | Validar entradas en servidor (obligatorio) y cliente (UX). |
| **Output Encoding** | Prevenir inyecciones y XSS mediante codificación/parametrización adecuada. |
| **Audit Logs** | Registrar operaciones relevantes de seguridad sin registrar secretos. |
| **Backup Security** | Proteger respaldos (cifrado/acceso) y comprobar su restauración. |
| **Penetration Testing** | Realizar pruebas de penetración autorizadas en sistemas expuestos o críticos. |

### Referencias importantes
* **OWASP Top 10** y **OWASP API Security Top 10**
* **OWASP ASVS 5.0:** https://asvs.owasp.org/
* **OWASP SAMM**
* **NIST SSDF (SP 800-218):** https://csrc.nist.gov/pubs/sp/800/218/final
* **ISO/IEC 27001:2022**, **ISO/IEC 27002:2022**, **ISO/IEC 27034**, **CIS Controls**

---

## 2. Privacidad y protección de datos personales

Especialmente importante si el proyecto administra usuarios, cuentas, información financiera, datos médicos o información personal (PII).

* **Privacy by Design** y **Privacy by Default** (configuraciones más restrictivas por defecto).
* **Minimización de datos:** recolectar únicamente lo indispensable para la finalidad declarada.
* **Consentimiento informado** y gestión granular de permisos cuando corresponda.
* **Documentos legales visibles:** Política de privacidad, Términos y condiciones, Política de cookies.
* **Derechos ARCO:** Acceso, Rectificación, Cancelación y Oposición, según legislación aplicable.
* **Retención y eliminación:** políticas claras de cuánto tiempo se conserva la información y cómo se purga.
* **Anonimización y seudonimización** cuando los datos se usen para analítica o entornos no productivos.
* **Control de acceso** estricto a información personal y **registro de tratamiento de datos**.
* **Gestión de incidentes de privacidad** y notificación oportuna.
* **Protección de datos en respaldos** y **restricción de información sensible en logs**.
* **México:** considerar la **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)** y su normativa aplicable cuando corresponda al responsable del tratamiento.
* **Estándares:** ISO/IEC 27701, ISO/IEC 29100.

---

## 3. Gestión de dependencias y cadena de suministro

Una aplicación con código propio excelente sigue siendo vulnerable por dependencias externas comprometidas o desactualizadas:

* Mantener dependencias actualizadas y fijar versiones reproducibles.
* Utilizar **lockfiles** (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, etc.) y verificar integridad de paquetes.
* Revisar **licencias de terceros** para evitar incompatibilidades legales.
* Detectar paquetes abandonados y evitar dependencias innecesarias o de fuentes no confiables.
* Analizar vulnerabilidades conocidas (**SCA**), revisar imágenes base de contenedores y generar **SBOM**.
* Automatizar actualizaciones mediante herramientas como **Dependabot** o **Renovate**.
* Establecer un **procedimiento de respuesta ante vulnerabilidades críticas** (triage, parcheo, rotación de secretos si aplica, re-despliegue).
* **Candado anti-*Vibe Coding*:** todo código o paquete sugerido por IA debe pasar linter, tipado, pruebas y revisión humana del `git diff` verificando que cada dependencia exista realmente en el registro oficial (evitar *slopsquatting* o paquetes inutilizados) y que no debilite auth, precios ni permisos.

### Herramientas recomendadas
* **SAST / Seguridad:** SonarQube, CodeQL, Semgrep.
* **DAST:** OWASP ZAP.
* **Dependencias / Secretos / Contenedores:** Dependabot, Renovate, Gitleaks, GitHub Secret Protection, Trivy.
* **Licencias y propiedad intelectual:** FOSSA, ORT, ScanCode Toolkit.

---

## 4. Licencias, propiedad intelectual y seguridad de releases

* **Licencias de código abierto y terceros:** identificar licencias de librerías, verificar compatibilidad entre sí (ej. evitar copyleft incompatible en software propietario cerrado), revisar licencias de recursos gráficos/fuentes/datasets/modelos y respetar atribuciones legales.
* **Condiciones comerciales de APIs y contratos:** validar límites de uso comercial y propiedad intelectual del código desarrollado.
* **Integridad de artefactos y distribución:** verificación mediante hashes, firma digital de ejecutables/paquetes (**Sigstore** / **SLSA** según nivel) y procedimiento para retirar versiones vulnerables.

---

## 5. Seguridad y privacidad en aplicaciones con IA / LLMs

*(Para cobertura completa de gobernanza, alucinaciones, sesgos, evals y costos de IA, aplica la skill `swe-ai-engineering`.)*

Cuando el proyecto integre modelos de lenguaje (LLMs), RAG o agentes de IA (referencia: **OWASP Top 10 for LLM Applications**):

* **Defensa contra Prompt Injection (directa e indirecta):** separar claramente instrucciones del sistema de datos no confiables (documentos recuperados, correos, entradas web); nunca confiar ciegamente en texto externo para decidir acciones privilegiadas.
* **Validación y sanitización de salidas:** tratar toda respuesta del modelo como entrada no confiable; validar esquemas, escapar HTML/Markdown antes de renderizar (prevención de XSS) y jamás ejecutar SQL/comandos generados por el modelo sin parametrización y validación estricta.
* **Mínimo privilegio en herramientas (*Tool Calling*):** restringir qué herramientas puede invocar un agente, exigir confirmación humana para acciones destructivas/financieras y validar permisos del usuario real en el backend (no delegar autorización al prompt).
* **Protección de PII y secretos hacia proveedores externos:** no enviar datos personales sensibles, credenciales ni código propietario sin anonimización/minimización, consentimiento informado y verificación de la política de retención y no-entrenamiento del proveedor LLM.
* **Control de abuso y costos:** aplicar límites de tokens, tamaño de entrada y rate limiting por usuario/tenant.
* **Logging seguro:** evitar registrar prompts completos con PII o secretos en logs sin enmascaramiento.
