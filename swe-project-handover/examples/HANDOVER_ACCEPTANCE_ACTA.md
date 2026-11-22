# Checklist de Aceptación Formal y Acta de Entrega (`HANDOVER_ACCEPTANCE`)

- **Proyecto:** `[Nombre del Proyecto]`
- **Versión / Commit entregado:** `[vX.Y.Z / <git-sha>]`
- **Nivel del proyecto:** `[Nivel 1: MVP | Nivel 2: Profesional | Nivel 3: Empresarial]`
- **Fecha de cierre:** `[YYYY-MM-DD]`

---

## 1. Checklist de Project Handover Acceptance

### A. Documentación e integridad del paquete
- [ ] Estructura `PROJECT-HANDOVER/` completa para el nivel acordado (`00-START-HERE` a `17-APPENDICES`).
- [ ] `handover_scaffold.py audit` ejecutado con **0 secretos**, **0 archivos `.env`** y sin placeholders críticos pendientes.
- [ ] `04-CODEBASE-GUIDE/` (`CODEBASE_GUIDE.md`, `MODULES.md`, `ERROR_CATALOG.md`, `CONFIGURATION_REFERENCE.md`) refleja el código real del commit entregado.
- [ ] `11-HISTORY-AND-KNOWN-ISSUES/` documenta con transparencia bugs conocidos, deuda técnica, riesgos y preguntas abiertas.
- [ ] `12-LEGAL-LICENSES-AND-IP/` documenta licencias de terceros, copyright, activos y titularidad.
- [ ] `13-MANUALS/` contiene los manuales requeridos para el nivel (Usuario, Administrador, Soporte, Operaciones).
- [ ] `17-APPENDICES/LIVING_DOCUMENTATION_POLICY.md` (Regla 18) integrada al flujo de PRs y releases.

### B. Autonomía técnica y operativa demostrada
- [ ] El equipo sucesor clonó, configuró, levantó el entorno local y corrió la suite de pruebas desde cero sin ayuda del autor.
- [ ] El equipo sucesor ejecutó un despliegue controlado y validó el procedimiento de rollback.
- [ ] Se validó un procedimiento de respuesta a incidentes / restauración de backup (Nivel 2–3).

### C. Propiedad, accesos y seguridad
- [ ] Inventario de activos entregables (`14-DELIVERABLES-INVENTORY/`) verificado al 100 %.
- [ ] Propiedad y facturación de repositorios, cloud, dominios y SaaS transferidas al titular receptor con MFA.
- [ ] Accesos del equipo saliente revocados y secretos compartidos rotados.

---

## 2. Excepciones o pendientes acordados (si existen)

| ID | Pendiente acordado | Responsable | Fecha compromiso | Criterio de cierre |
| :--- | :--- | :--- | :--- | :--- |
| `PEND-01` | `[Ninguno / describir brecha aceptada explícitamente]` | `[Nombre]` | `[YYYY-MM-DD]` | `[Verificación concreta]` |

---

## 3. Periodo de acompañamiento (*Hypercare*)
- **¿Aplica periodo de acompañamiento?** `[Sí / No]`
- **Vigencia:** `[YYYY-MM-DD]` al `[YYYY-MM-DD]`
- **Alcance y canal:** `[Ej. Soporte reactivo de dudas en horario laboral vía <canal>; sin acceso de escritura a producción]`

---

## 4. Acta de Entrega y Aceptación (`HANDOVER_SIGN_OFF_ACTA`)

Con la firma de este documento, las partes confirman la entrega y recepción del código fuente, activos inventariados, accesos transferidos y paquete documental `PROJECT-HANDOVER/` correspondiente al commit `[<git-sha>]`, sujeto únicamente a los pendientes explícitamente registrados en la Sección 2.

| Rol | Nombre completo | Organización / Área | Firma / Aprobación | Fecha |
| :--- | :--- | :--- | :--- | :--- |
| **Responsable saliente (Entrega)** | `[Nombre]` | `[Área]` | `[Firma / ID PR]` | `[YYYY-MM-DD]` |
| **Responsable técnico receptor (Acepta)** | `[Nombre]` | `[Área]` | `[Firma / ID PR]` | `[YYYY-MM-DD]` |
| **Product Owner / Patrocinador (Vo. Bo.)** | `[Nombre]` | `[Área]` | `[Firma / ID PR]` | `[YYYY-MM-DD]` |
