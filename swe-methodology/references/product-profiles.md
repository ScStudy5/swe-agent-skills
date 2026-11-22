# Perfiles de Ingeniería por Tipo de Producto

Selecciona únicamente el perfil que corresponde al proyecto actual para aplicar los controles exactos sin sobrecargar otros dominios.

| Tipo de producto | Controles y prácticas adicionales prioritarias |
| :--- | :--- |
| **SaaS / Aplicaciones Web Multi-tenant** | Aislamiento estricto entre clientes (`tenant_id` validado en servidor en cada consulta), gestión de planes/cuotas, facturación idempotente (webhooks verificados), onboarding, RBAC por organización, rate limiting por tenant y SEO/Core Web Vitals. |
| **APIs y Microservicios / Sistemas Distribuidos** | Contratos OpenAPI, versionado, Problem Details (RFC 9457), idempotencia, Circuit Breaker, Dead Letter Queues, correlación distribuida (`Correlation ID`), consistencia eventual manejada con seguridad y pruebas de contrato. |
| **Aplicaciones Móviles (iOS / Android / Multiplataforma)** | Almacenamiento local seguro (Keychain/Keystore, nunca tokens en texto plano), permisos mínimos justificados, manejo de modo offline/reconexión, certificate pinning cuando corresponda, tamaño de binario y reglas de publicación en App Store / Play Store. |
| **Aplicaciones de Escritorio** | Instaladores y binarios firmados digitalmente, canal seguro de actualizaciones automáticas, aislamiento de permisos locales y compatibilidad entre sistemas operativos (Windows/macOS/Linux). |
| **Sistemas Financieros / Pagos** | Auditoría transaccional inmutable, conciliación periódica, idempotencia estricta en cobros/movimientos, doble verificación/MFA, controles antifraude, cifrado reforzado y retención legal. |
| **Sistemas Médicos / Salud** | Seguridad del paciente (Human-in-the-loop en alertas clínicas), trazabilidad completa de accesos a expedientes, cifrado estricto, retención y cumplimiento regulatorio sanitario aplicable. |
| **Sistemas Empresariales (ERP/CRM/Internos)** | Integración segura con sistemas existentes, SSO (OIDC/SAML), RBAC/ABAC granular, auditoría de cambios, importación/exportación validada y soporte por versión. |
| **IoT (Internet of Things)** | Identidad única por dispositivo, seguridad de firmware, actualizaciones OTA firmadas y con rollback, comunicación cifrada y resiliencia ante desconexiones. |
| **Videojuegos / Tiempo Real** | Validación autoritativa en servidor (*anti-cheat*), sincronización y compensación de latencia, protección de economía virtual y pruebas de carga/picos. |
