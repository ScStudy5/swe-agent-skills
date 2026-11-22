# Índice Maestro de Handover — [Nombre del Proyecto]

- **Última actualización:** `[YYYY-MM-DD]`
- **Versión / Commit de referencia:** `[vX.Y.Z / <git-sha>]`
- **Nivel del proyecto:** `[Nivel 1: MVP | Nivel 2: Profesional | Nivel 3: Empresarial]`
- **Estado actual:** `[En producción | En staging | En desarrollo | En mantenimiento]`
- **Responsable saliente / receptor:** `[Rol/Nombre saliente]` -> `[Rol/Nombre receptor]`

> **Advertencia de seguridad:** Este paquete NO contiene contraseñas, API keys ni archivos `.env` reales. Toda credencial se consulta exclusivamente en la bóveda documentada en `08-SECURITY-AND-PRIVACY/SECURITY_HANDOVER.md`.

---

## 1. Resumen ejecutivo en 60 segundos
- **Qué resuelve el sistema:** `[Descripción breve del problema y usuarios principales]`
- **Stack principal:** `[Lenguaje/Framework backend, frontend, BD, cloud/hosting]`
- **URLs clave:**
  - Producción: `[https://...]`
  - Staging / QA: `[https://...]`
  - Repositorio: `[URL del repo]`
  - Monitoreo / Errores: `[URL Sentry / Grafana / Dashboard]`

---

## 2. Ruta de lectura recomendada por rol

| Tu rol | Empieza leyendo en este orden |
| :--- | :--- |
| **Desarrollador nuevo (Onboarding)** | `00-START-HERE/QUICKSTART.md` -> `03-ARCHITECTURE-AND-DESIGN/ARCHITECTURE.md` -> `04-CODEBASE-GUIDE/CODEBASE_GUIDE.md` -> `11-HISTORY-AND-KNOWN-ISSUES/KNOWN_ISSUES.md` |
| **DevOps / SRE / Infra** | `10-DEVOPS-AND-OPERATIONS/INFRASTRUCTURE_AND_DEPLOY.md` -> `05-DATA-AND-DATABASES/BACKUP_AND_RECOVERY.md` -> `13-MANUALS/OPERATIONS_MANUAL.md` -> `14-DELIVERABLES-INVENTORY/DELIVERABLES_INVENTORY.md` |
| **QA / Seguridad** | `08-SECURITY-AND-PRIVACY/SECURITY_HANDOVER.md` -> `09-QA-AND-TESTING/TESTING_GUIDE.md` -> `11-HISTORY-AND-KNOWN-ISSUES/BUG_BACKLOG.md` |
| **Soporte / Operaciones** | `13-MANUALS/SUPPORT_MANUAL.md` -> `04-CODEBASE-GUIDE/ERROR_CATALOG.md` -> `11-HISTORY-AND-KNOWN-ISSUES/KNOWN_ISSUES.md` |
| **Negocio / Product Owner / Legal** | `00-START-HERE/PROJECT_STATUS.md` -> `01-EXECUTIVE-CONTEXT/PROJECT_CHARTER.md` -> `12-LEGAL-LICENSES-AND-IP/IP_OWNERSHIP_AND_TRANSFER.md` -> `16-HANDOVER-ACCEPTANCE/HANDOVER_SIGN_OFF_ACTA.md` |

---

## 3. Mapa completo del paquete (`PROJECT-HANDOVER/`)

| # | Sección | Propósito principal | Estado |
| :-: | :--- | :--- | :--- |
| `00` | `00-START-HERE/` | Índice, arranque rápido y estado actual del proyecto | `[Completo / En curso]` |
| `01` | `01-EXECUTIVE-CONTEXT/` | Charter, business case, stakeholders, visión y glosario | `[Completo / N/A]` |
| `02` | `02-REQUIREMENTS-AND-DOMAIN/` | Requisitos funcionales, no funcionales y dominio/regulación | `[Completo / N/A]` |
| `03` | `03-ARCHITECTURE-AND-DESIGN/` | Arquitectura C4, diagramas e índice de ADRs | `[Completo / En curso]` |
| `04` | `04-CODEBASE-GUIDE/` | Guía del código fuente, módulos, errores y configuración | `[Completo / En curso]` |
| `05` | `05-DATA-AND-DATABASES/` | Modelo de datos, diccionario, migraciones y backup/restore | `[Completo / N/A]` |
| `06` | `06-APIS-AND-INTEGRATIONS/` | Contratos OpenAPI, RFC 9457 e integraciones externas | `[Completo / N/A]` |
| `07` | `07-UX-UI-AND-ACCESSIBILITY/` | Design system, WCAG 2.2 AA e i18n/compatibilidad | `[Completo / N/A]` |
| `08` | `08-SECURITY-AND-PRIVACY/` | Seguridad, privacidad (ARCO/LFPDPPP/GDPR) y SBOM/SCA | `[Completo / En curso]` |
| `09` | `09-QA-AND-TESTING/` | Estrategia de pruebas, datos sintéticos y última auditoría | `[Completo / En curso]` |
| `10` | `10-DEVOPS-AND-OPERATIONS/` | Infraestructura, CI/CD, rollback, observabilidad y FinOps | `[Completo / En curso]` |
| `11` | `11-HISTORY-AND-KNOWN-ISSUES/` | Bugs conocidos, deuda técnica, riesgos, lecciones y decisiones | `[Completo / En curso]` |
| `12` | `12-LEGAL-LICENSES-AND-IP/` | Licencias OSS, copyright, activos y titularidad de PI | `[Completo / N/A]` |
| `13` | `13-MANUALS/` | Manuales de Usuario, Administrador, Soporte y Operaciones | `[Completo / N/A]` |
| `14` | `14-DELIVERABLES-INVENTORY/` | Inventario de activos digitales/físicos y matriz de cuentas | `[Completo / En curso]` |
| `15` | `15-TRANSFER-AND-SESSIONS/` | Transferencia/revocación de accesos y sesiones supervisadas | `[Completo / En curso]` |
| `16` | `16-HANDOVER-ACCEPTANCE/` | Checklist de aceptación formal y acta de entrega | `[Pendiente / Firmado]` |
| `17` | `17-APPENDICES/` | Anexos, política de documentación viva (Regla 18) y addendums | `[Completo / En curso]` |
