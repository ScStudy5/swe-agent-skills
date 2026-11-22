# Protocolo Formal de Transferencia, Sesiones Supervisadas y Cierre (Puntos 14, 15 y 16)

Un handover no termina al entregar archivos Markdown: termina cuando el sucesor **posee los accesos, puede operar el sistema sin ayuda y firma la aceptación formal**.

---

## Fase 1 — Inventario verificable de activos entregables (Punto 14)

Completa `14-DELIVERABLES-INVENTORY/DELIVERABLES_INVENTORY.md` y `ACCOUNTS_AND_ACCESS_MATRIX.md` listando todos los activos reales del proyecto:

1. **Código y artefactos:** repositorios Git (URLs, ramas principales, tags/releases vigentes), registros de contenedores/paquetes (Docker Hub, GHCR, npm, PyPI), pipelines CI/CD y secretos configurados en CI (solo nombres, nunca valores).
2. **Infraestructura y nube:** cuentas/suscripciones (AWS/Azure/GCP/Cloudflare/Vercel/Render), clusters, bases de datos, buckets de almacenamiento, colas, VPNs, alertas de facturación y topes de costo.
3. **Dominios, DNS y certificados:** registrador de dominios, zonas DNS, fechas de renovación, certificados TLS y correo transaccional (SPF/DKIM/DMARC).
4. **Servicios SaaS y terceros:** pasarelas de pago, proveedores de auth, analítica/monitoreo (Sentry, Grafana, Datadog), proveedores de IA/LLM, SMS/email, licencias de pago.
5. **Diseño, producto y gestión:** archivos Figma/Design System, tableros Jira/Linear/GitHub Projects, wikis, tiendas móviles (Apple Developer, Google Play Console) y cuentas de soporte.

---

## Fase 2 — Transferencia de propiedad, rotación y revocación (Punto 15A)

Usa [ACCESS_TRANSFER_AND_REVOCATION.md](../examples/ACCESS_TRANSFER_AND_REVOCATION.md) siguiendo este orden estricto (para no provocar bloqueos ni pérdidas de acceso):

1. **Alta del nuevo propietario (*Owner/Admin*):** otorgar privilegios de propietario al equipo receptor con MFA obligatorio y verificar que puede iniciar sesión y administrar la cuenta.
2. **Transferencia de facturación y titularidad:** cambiar método de pago, correo de facturación y contacto de recuperación/emergencia al titular receptor.
3. **Transferencia de bóveda de secretos:** migrar secretos a la bóveda del equipo receptor (1Password, Vault, AWS Secrets Manager, Azure Key Vault, etc.). **Prohibido enviar secretos por correo, WhatsApp o archivos planos.**
4. **Revocación del equipo saliente:** retirar permisos de repositorios, cloud, bases de datos, VPN, CI/CD, DNS y SaaS al personal saliente dejando evidencia con fecha y responsable.
5. **Rotación posterior a la revocación:** rotar obligatoriamente claves compartidas, API keys estáticas, contraseñas de BD, webhooks secrets, tokens de despliegue y llaves SSH que el equipo saliente conoció.

---

## Fase 3 — Sesiones supervisadas de transferencia práctica (Punto 15B)

Documenta en `15-TRANSFER-AND-SESSIONS/HANDOVER_SESSIONS_LOG.md` al menos las siguientes sesiones prácticas (con el **sucesor al teclado** mientras el autor original solo guía):

| Sesión | Objetivo verificable | Criterio de éxito |
| :--- | :--- | :--- |
| **1. Recorrido de arquitectura y negocio** | Explicar dominio, flujos críticos, decisiones históricas, deuda técnica y puntos frágiles. | El sucesor puede explicar el flujo principal de punta a punta y dónde vive cada regla crítica. |
| **2. Instalación y pruebas desde cero** | El sucesor clona el repo en una máquina limpia, configura variables desde `.env.example`, levanta servicios y ejecuta la suite de tests. | Entorno local funcional y tests pasando sin intervención manual del autor original. |
| **3. Despliegue y rollback controlado** | El sucesor ejecuta un cambio menor por el pipeline real (PR -> CI -> despliegue a `staging` y reversión/rollback). | Despliegue y rollback exitosos verificando health checks y logs. |
| **4. Simulación de incidente y backup/restore** | Simular un fallo representativo (error 500, caída de servicio externo o restauración de backup en entorno de pruebas) siguiendo `OPERATIONS_MANUAL.md`. | El sucesor diagnostica con logs/alertas, aplica el runbook y recupera el servicio dentro del objetivo esperado. |

*(En Nivel 1 / MVP se pueden combinar las sesiones 1–3 en una sola sesión práctica grabada y documentada).*

---

## Fase 4 — Cierre y Aceptación Formal (Punto 16)

1. Ejecutar `handover_scaffold.py audit` para validar completitud, ausencia de placeholders críticos y **cero fugas de secretos**.
2. Revisar cada criterio del checklist en [HANDOVER_ACCEPTANCE_ACTA.md](../examples/HANDOVER_ACCEPTANCE_ACTA.md).
3. Registrar explícitamente cualquier **excepción o pendiente acordado** con responsable y fecha límite (nunca ocultar brechas bajo una firma).
4. Firmar el **Acta de Entrega (`HANDOVER_SIGN_OFF_ACTA.md`)** por parte del responsable saliente, responsable técnico receptor y patrocinador/Product Owner, indicando si existe periodo de acompañamiento (*hypercare*) y su fecha de fin.
