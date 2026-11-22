# Plano Maestro de 18 Puntos para Software Project Handover

Estructura unificada (`PROJECT-HANDOVER/`) diseñada para transferir un proyecto de software sin dependencia del autor original. Ajusta la profundidad según el nivel del proyecto (`Nivel 1: MVP`, `Nivel 2: Profesional`, `Nivel 3: Empresarial`).

---

## 1. Matriz de carpetas, documentos y nivel mínimo requerido

Leyenda de obligatoriedad: **O** = Obligatorio · **R** = Recomendado/Condicional (si aplica al stack) · **—** = Opcional / No requerido en este nivel.

| # | Carpeta en `PROJECT-HANDOVER/` | Documentos clave | N1 (MVP) | N2 (Prof.) | N3 (Empr.) | Skill de apoyo |
| :-: | :--- | :--- | :-: | :-: | :-: | :--- |
| `00` | `00-START-HERE/` | `INDEX.md`, `QUICKSTART.md`, `PROJECT_STATUS.md` | **O** | **O** | **O** | `swe-methodology` |
| `01` | `01-EXECUTIVE-CONTEXT/` | `PROJECT_CHARTER.md`, `BUSINESS_CASE.md`, `STAKEHOLDERS.md`, `PRODUCT_VISION.md`, `GLOSSARY.md` | R *(resumen)* | **O** | **O** | `swe-methodology` |
| `02` | `02-REQUIREMENTS-AND-DOMAIN/` | `FUNCTIONAL_REQUIREMENTS.md`, `NON_FUNCTIONAL_REQUIREMENTS.md`, `DOMAIN_REQUIREMENTS.md`, `SCOPE_AND_EXCLUSIONS.md` | R | **O** | **O** | `swe-domain-discovery` |
| `03` | `03-ARCHITECTURE-AND-DESIGN/` | `ARCHITECTURE.md` (C4), `DIAGRAMS.md`, `ADRS_INDEX.md` (enlaza `docs/adr/`) | **O** | **O** | **O** | `swe-architecture-design` |
| `04` | `04-CODEBASE-GUIDE/` | `CODEBASE_GUIDE.md`, `MODULES.md`, `ERROR_CATALOG.md`, `CONFIGURATION_REFERENCE.md` | **O** | **O** | **O** | `swe-architecture-design` |
| `05` | `05-DATA-AND-DATABASES/` | `DATABASE_GUIDE.md` (ERD), `DATA_DICTIONARY.md`, `MIGRATIONS_AND_SEEDS.md`, `BACKUP_AND_RECOVERY.md` (RTO/RPO) | R *(si hay BD)* | **O** | **O** | `swe-data-apis` |
| `06` | `06-APIS-AND-INTEGRATIONS/` | `API_GUIDE.md` (OpenAPI + RFC 9457), `EXTERNAL_INTEGRATIONS.md` (webhooks, SLAs, fallbacks) | R *(si hay API)* | **O** | **O** | `swe-data-apis` |
| `07` | `07-UX-UI-AND-ACCESSIBILITY/` | `DESIGN_SYSTEM_AND_FLOWS.md`, `ACCESSIBILITY_REPORT.md` (WCAG 2.2 AA), `I18N_AND_COMPATIBILITY.md` | — | R *(si hay UI)* | **O** | `swe-ux-accessibility` |
| `08` | `08-SECURITY-AND-PRIVACY/` | `SECURITY_HANDOVER.md` (Threat Model, Auth/RBAC, bóveda de secretos), `PRIVACY_COMPLIANCE.md` (ARCO/LFPDPPP/GDPR), `SBOM_AND_SCA_STATUS.md` | **O** *(base)* | **O** | **O** | `swe-security-privacy` |
| `09` | `09-QA-AND-TESTING/` | `TESTING_GUIDE.md`, `TEST_DATA_AND_ENVIRONMENTS.md`, `LAST_AUDIT_RESULTS.md` (incl. Playwright si aplica) | R | **O** | **O** | `swe-qa-testing` + `swe-browser-audit` |
| `10` | `10-DEVOPS-AND-OPERATIONS/` | `INFRASTRUCTURE_AND_DEPLOY.md`, `CICD_PIPELINES.md`, `ROLLBACK_PROCEDURES.md`, `OBSERVABILITY_AND_FINOPS.md` | **O** *(deploy)* | **O** | **O** | `swe-devops-operations` |
| `11` | `11-HISTORY-AND-KNOWN-ISSUES/` | `KNOWN_ISSUES.md`, `BUG_BACKLOG.md`, `TECHNICAL_DEBT.md`, `LESSONS_LEARNED.md`, `RISKS_REGISTER.md`, `OPEN_QUESTIONS.md`, `DECISIONS_HISTORY.md` | **O** *(issues/deuda)* | **O** | **O** | `swe-methodology` |
| `12` | `12-LEGAL-LICENSES-AND-IP/` | `THIRD_PARTY_LICENSES.md`, `COPYRIGHT.md`, `ASSET_LICENSES.md`, `IP_OWNERSHIP_AND_TRANSFER.md` | R *(licencias)* | **O** | **O** | `swe-legal-compliance` + `swe-security-privacy` |
| `13` | `13-MANUALS/` | `USER_MANUAL.md`, `ADMINISTRATOR_MANUAL.md`, `SUPPORT_MANUAL.md`, `OPERATIONS_MANUAL.md` | — | **O** *(según rol)* | **O** | `swe-devops-operations` + `swe-ux-accessibility` |
| `14` | `14-DELIVERABLES-INVENTORY/` | `DELIVERABLES_INVENTORY.md`, `ACCOUNTS_AND_ACCESS_MATRIX.md` | **O** | **O** | **O** | `swe-project-handover` |
| `15` | `15-TRANSFER-AND-SESSIONS/` | `ACCESS_TRANSFER_AND_REVOCATION.md`, `HANDOVER_SESSIONS_LOG.md` | R | **O** | **O** | `swe-project-handover` |
| `16` | `16-HANDOVER-ACCEPTANCE/` | `HANDOVER_ACCEPTANCE_CHECKLIST.md`, `HANDOVER_SIGN_OFF_ACTA.md` | **O** *(ligero)* | **O** | **O** | `swe-project-handover` |
| `17` | `17-APPENDICES/` | `APPENDICES_INDEX.md`, `LIVING_DOCUMENTATION_POLICY.md`, `AI_SYSTEMS_ADDENDUM.md` *(si usa IA/LLMs)* | **O** *(política viva)* | **O** | **O** | `swe-ai-engineering` + `swe-project-handover` |

> **Punto 18 (Transversal — Estándar de Documentación Viva):** no es una carpeta más sino una **regla de gobernanza permanente** materializada en `17-APPENDICES/LIVING_DOCUMENTATION_POLICY.md` y conectada a los PRs, DoD y releases (ver [living-documentation-standard.md](./living-documentation-standard.md)).

---

## 2. Qué debe responder cada sección crítica

### Punto 00 — `00-START-HERE/`
* ¿Qué hace este sistema en 3 párrafos y en qué estado real está hoy (producción, staging, pausado, con incidentes activos)?
* ¿Qué debo leer primero según mi rol (Desarrollador Backend/Frontend, DevOps, QA, Soporte, Product Owner)?
* ¿Cómo levanto el sistema localmente en menos de 30 minutos?

### Punto 04 — `04-CODEBASE-GUIDE/` (Onboarding real para sucesores)
* **`CODEBASE_GUIDE.md`:** mapa real de carpetas, puntos de entrada (`main`, routers, workers, cron jobs), flujo de una petición de extremo a extremo y "trampas conocidas" del código.
* **`MODULES.md`:** tabla de módulos/dominios, responsabilidades, dependencias internas/externas y propietario técnico.
* **`ERROR_CATALOG.md`:** códigos de error de dominio/API, causa habitual, impacto al usuario y diagnóstico rápido.
* **`CONFIGURATION_REFERENCE.md`:** inventario completo de variables de entorno (nombre, tipo, valor por defecto, obligatorio/opcional, ambiente donde aplica y efecto — **sin valores secretos**), feature flags y archivos de configuración.

### Punto 11 — `11-HISTORY-AND-KNOWN-ISSUES/` (Memoria histórica y transparencia)
* **`KNOWN_ISSUES.md`:** fallos conocidos activos, workarounds vigentes y condiciones que los disparan.
* **`BUG_BACKLOG.md`:** bugs abiertos priorizados por severidad con enlace al issue tracker.
* **`TECHNICAL_DEBT.md`:** atajos tomados conscientemente, impacto al escalar y esfuerzo estimado de remediación.
* **`LESSONS_LEARNED.md`:** qué funcionó bien, qué salió mal en incidentes o diseños previos y qué no repetir.
* **`RISKS_REGISTER.md`:** riesgos técnicos, operativos, de proveedor o regulatorios con probabilidad, impacto y mitigación.
* **`OPEN_QUESTIONS.md`:** decisiones de negocio o arquitectura aún pendientes de respuesta y quién debe decidirlas.
* **`DECISIONS_HISTORY.md`:** línea de tiempo de decisiones críticas que explica el *"por qué"* del sistema (complementando los ADRs en `docs/adr/`).

### Punto 12 — `12-LEGAL-LICENSES-AND-IP/`
* **`THIRD_PARTY_LICENSES.md`:** resumen de licencias OSS (MIT, Apache-2.0, BSD, GPL/LGPL, etc.) generado desde el lockfile/SBOM y alertas de compatibilidad.
* **`COPYRIGHT.md`:** titularidad de derechos de autor, avisos legales y licencia del código propio.
* **`ASSET_LICENSES.md`:** fuentes tipográficas, iconos, ilustraciones, audio/video, datasets y licencias de modelos de IA.
* **`IP_OWNERSHIP_AND_TRANSFER.md`:** registro de titularidad de dominios, cuentas de tiendas (App Store/Play Store), marcas, contratos de cesión de PI y acuerdos con terceros *(nota: referencia administrativa/técnica, validar con área legal)*.

### Punto 13 — `13-MANUALS/` (Diferenciados por perfil)
* **`USER_MANUAL.md`:** tareas de usuario final con pasos claros y mensajes frecuentes.
* **`ADMINISTRATOR_MANUAL.md`:** gestión de usuarios/roles, configuración de tenants/parámetros, reportes y auditoría.
* **`SUPPORT_MANUAL.md`:** triage L1/L2/L3, consultas diagnósticas seguras, errores frecuentes y árbol de escalamiento.
* **`OPERATIONS_MANUAL.md`:** runbooks de despliegue, reinicio, restauración de backups, respuesta a incidentes, rotación de certificados/secretos y postmortem.

---

## 3. Regla anti-duplicación con documentación existente en el repositorio
Si el repositorio ya cuenta con archivos vigentes en raíz o `docs/` (por ejemplo `README.md`, `ARCHITECTURE.md`, `SECURITY.md`, `docs/adr/`, `openapi.yaml`), **no copies y pegues texto que luego quede desincronizado**:
1. Referencia el archivo fuente con ruta relativa verificada o enlázalo desde la sección correspondiente de `PROJECT-HANDOVER/`.
2. Si el handover se entregará como paquete independiente fuera del repositorio (zip/PDF/wiki), genera una instantánea fechada indicando el commit SHA exacto (`git rev-parse --short HEAD`) del cual se extrajo.
