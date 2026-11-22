# Transferencia de Propiedad, Accesos y Revocación (Puntos 14 y 15)

- **Proyecto:** `[Nombre del Proyecto]`
- **Fecha de ejecución:** `[YYYY-MM-DD]`
- **Responsable saliente:** `[Nombre / Rol]`
- **Responsable receptor:** `[Nombre / Rol]`

> **Regla estricta de seguridad:** Nunca pegues contraseñas, tokens, llaves privadas ni archivos `.env` en este documento. Registra únicamente identificadores de cuenta, niveles de permiso, ubicación en bóveda y fecha de rotación/revocación.

---

## 1. Matriz de cuentas, propiedad y revocación

| Activo / Plataforma | Cuenta / Organización | Nuevo Owner (MFA verificado) | Facturación transferida | Acceso saliente revocado | Claves/Tokens rotados | Fecha verificación |
| :--- | :--- | :--- | :-: | :-: | :-: | :--- |
| **Repositorio Git** (GitHub/GitLab) | `[org/repo]` | `[Usuario receptor]` | `[Sí / N/A]` | `[ ]` | `[ ]` *(deploy keys, PATs)* | `[YYYY-MM-DD]` |
| **Cloud / Hosting** (AWS/Azure/GCP/CF) | `[Cuenta / Suscripción]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(IAM, API keys)* | `[YYYY-MM-DD]` |
| **Base de datos administrada** | `[Instancia / Cluster]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(DB passwords)* | `[YYYY-MM-DD]` |
| **Dominio y DNS** | `[Registrador / Zona]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(API tokens DNS)* | `[YYYY-MM-DD]` |
| **Bóveda de secretos** | `[1Password / Vault / KeyVault]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(maestra/accesos)* | `[YYYY-MM-DD]` |
| **CI/CD y Registros** | `[Actions / GHCR / npm]` | `[Usuario receptor]` | `[N/A]` | `[ ]` | `[ ]` *(secrets CI)* | `[YYYY-MM-DD]` |
| **Observabilidad / Errores** | `[Sentry / Grafana]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(DSN / tokens)* | `[YYYY-MM-DD]` |
| **Servicios SaaS / Pagos / IA** | `[Stripe / OpenAI / Resend]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[ ]` *(API & webhook secrets)* | `[YYYY-MM-DD]` |
| **Diseño y Gestión** | `[Figma / Jira / Stores]` | `[Usuario receptor]` | `[ ]` | `[ ]` | `[N/A]` | `[YYYY-MM-DD]` |

---

## 2. Registro de sesiones supervisadas (`HANDOVER_SESSIONS_LOG.md`)

| Sesión | Fecha | Participantes (Sucesor al teclado) | Resultado verificable | Grabación / Notas |
| :--- | :--- | :--- | :--- | :--- |
| **1. Arquitectura, negocio y deuda** | `[YYYY-MM-DD]` | `[Nombres]` | `[Aprobada / Pendiente]` | `[Enlace interno]` |
| **2. Instalación y tests desde cero** | `[YYYY-MM-DD]` | `[Nombres]` | `[Aprobada / Pendiente]` | `[Sin intervención del autor]` |
| **3. Despliegue + Rollback en staging** | `[YYYY-MM-DD]` | `[Nombres]` | `[Aprobada / Pendiente]` | `[Health check OK]` |
| **4. Simulación de incidente / Restore** | `[YYYY-MM-DD]` | `[Nombres]` | `[Aprobada / Pendiente]` | `[Runbook validado]` |

---

## 3. Verificación final de cierre de accesos
- [ ] El equipo receptor puede administrar el 100 % de las cuentas críticas con MFA habilitado.
- [ ] Todos los accesos individuales del equipo saliente fueron revocados (o acotados con fecha de expiración explícita si hay periodo de *hypercare*).
- [ ] Todas las credenciales compartidas, contraseñas de BD, webhooks y API keys conocidas por el equipo saliente fueron rotadas y probadas en producción/staging.
