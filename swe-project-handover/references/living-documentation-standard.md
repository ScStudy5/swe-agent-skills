# Estándar de Documentación Viva (Punto 18)

La documentación de entrega pierde valor en semanas si se trata como un evento único. Esta política establece las reglas operativas para que `PROJECT-HANDOVER/` (y la documentación técnica del repositorio) permanezca sincronizada con el sistema real durante toda su vida útil.

---

## 1. Principio rector: *Docs-as-Code*
* La documentación técnica vive **versionada en Git junto al código** (en `PROJECT-HANDOVER/` y `docs/`), se revisa en los mismos Pull Requests que los cambios funcionales y pasa verificaciones automáticas en CI.
* **Regla de fuente única:** evita copiar información volátil en varios documentos. Cuando un dato existe en código/esquema (p. ej. `openapi.yaml`, `.env.example`, migraciones SQL), enlázalo en lugar de duplicarlo manualmente.

---

## 2. Matriz de disparadores obligatorios de actualización

Todo Pull Request o release que introduzca alguno de los cambios siguientes **no cumple la Definition of Done (DoD)** hasta actualizar los documentos correspondientes:

| Tipo de cambio en el proyecto | Documentos que DEBEN actualizarse en el mismo PR / Release |
| :--- | :--- |
| Nueva variable de entorno, flag o cambio de configuración | `.env.example` + `04-CODEBASE-GUIDE/CONFIGURATION_REFERENCE.md` |
| Nuevo módulo, cambio de estructura o punto de entrada | `04-CODEBASE-GUIDE/CODEBASE_GUIDE.md` y `MODULES.md` |
| Decisión arquitectónica relevante o cambio de proveedor/stack | Nuevo ADR en `docs/adr/` + `03-ARCHITECTURE-AND-DESIGN/ARCHITECTURE.md` + `11-HISTORY-AND-KNOWN-ISSUES/DECISIONS_HISTORY.md` |
| Cambio de esquema de BD, política de retención o backup | `05-DATA-AND-DATABASES/DATABASE_GUIDE.md`, `DATA_DICTIONARY.md` y `BACKUP_AND_RECOVERY.md` |
| Nuevo endpoint, cambio breaking o código de error | Spec OpenAPI + `06-APIS-AND-INTEGRATIONS/API_GUIDE.md` + `04-CODEBASE-GUIDE/ERROR_CATALOG.md` |
| Nueva integración externa o webhook | `06-APIS-AND-INTEGRATIONS/EXTERNAL_INTEGRATIONS.md` + `14-DELIVERABLES-INVENTORY/DELIVERABLES_INVENTORY.md` |
| Cambio de permisos, auth, secretos o flujo de PII | `08-SECURITY-AND-PRIVACY/SECURITY_HANDOVER.md` y `PRIVACY_COMPLIANCE.md` |
| Cambio en CI/CD, infraestructura, alertas o costos | `10-DEVOPS-AND-OPERATIONS/INFRASTRUCTURE_AND_DEPLOY.md` y `OBSERVABILITY_AND_FINOPS.md` |
| Incidente relevante, bug conocido o deuda técnica aceptada | `11-HISTORY-AND-KNOWN-ISSUES/KNOWN_ISSUES.md`, `TECHNICAL_DEBT.md` y `LESSONS_LEARNED.md` |
| Nueva dependencia con licencia restrictiva o activo visual/IA | `12-LEGAL-LICENSES-AND-IP/THIRD_PARTY_LICENSES.md` o `ASSET_LICENSES.md` |
| Cambio visible en flujos de usuario, admin o soporte | Manual correspondiente en `13-MANUALS/` |
| Alta/baja de personal o cambio de accesos | `14-DELIVERABLES-INVENTORY/ACCOUNTS_AND_ACCESS_MATRIX.md` + `15-TRANSFER-AND-SESSIONS/ACCESS_TRANSFER_AND_REVOCATION.md` |

---

## 3. Control de frescura y cadencia de revisión
* **Metadatos mínimos en documentos clave:** incluir en la cabecera `Última actualización (YYYY-MM-DD)`, `Responsable (rol)` y `Commit/Versión de referencia`.
* **Verificación automática recomendada en CI:**
  * Ejecutar `handover_scaffold.py audit PROJECT-HANDOVER --level <1|2|3>` para garantizar **0 fugas de secretos / `.env`** y detectar secciones rotas.
  * Verificar enlaces rotos en Markdown (p. ej. `lychee` o script en CI) en proyectos Nivel 2–3.
* **Revisión periódica de vigencia:**
  * **Nivel 1 (MVP):** antes de cada hito mayor o cambio de desarrollador.
  * **Nivel 2 (Profesional):** revisión trimestral de `PROJECT_STATUS.md`, `KNOWN_ISSUES.md`, `ACCOUNTS_AND_ACCESS_MATRIX.md` y prueba de `QUICKSTART.md`.
  * **Nivel 3 (Empresarial):** revisión trimestral auditada + prueba semestral de restauración de backups y rotación de accesos reflejada en el handover.
