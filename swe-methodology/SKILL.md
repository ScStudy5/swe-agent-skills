---
name: swe-methodology
description: >-
  Metodología maestra de ingeniería de software: clasifica proyectos según
  riesgo y tamaño, guía gestión de producto (MVP, DoR, DoD), documentación técnica,
  normas internacionales (ISO 25010, 12207, 27001, WCAG, OWASP, NIST) y enruta hacia
  las skills especializadas swe-*. Usar al iniciar proyectos, planificar entregas,
  definir estándares o realizar auditorías integrales.
---

# Metodología Maestra y Gobierno de Proyecto

Usa esta skill como punto de entrada para establecer estándares profesionales de desarrollo en aplicaciones web, PWAs, APIs, SaaS, apps móviles o sistemas empresariales.

## Principio rector

**Aplicación proporcional:** no todas las prácticas son obligatorias en todos los proyectos. Algunas son requisitos de seguridad o cumplimiento legal, otras estándares internacionales y otras recomendaciones de ingeniería. Ajusta el rigor según **riesgo, tamaño, datos manejados y naturaleza del sistema**.

## Flujo de trabajo

### 1. Clasificar el nivel del proyecto y su perfil
Antes de recomendar controles o auditar, pregunta explícitamente (si el usuario aún no lo indicó) **hasta qué nivel quiere llevar el proyecto**:

1. **Nivel 1 — MVP:** entrega rápida sin deuda tóxica y preparada para crecer (arquitectura clara, validación de entradas en servidor, secretos protegidos, tests críticos, HTTPS).
2. **Nivel 2 — Profesional (miles de usuarios / SaaS / App en vivo):** CI/CD con linters y tests completos, resiliencia (timeouts/retries/idempotencia), backups con restauración probada, WCAG 2.2 AA, auditoría en navegador (`swe-browser-audit`), monitoreo de errores, alertas de costos en nube y auditorías periódicas.
3. **Nivel 3 — Empresarial / Regulado:** SSDLC y Threat Modeling formal, gobernanza (RACI/SRS/BPMN/DAMA-DMBOK), cumplimiento ISO/OWASP ASVS/NIST SSDF, SLSA/Sigstore, ITIL 4, Chaos/Load testing y observabilidad distribuida.

*Si el proyecto pertenece a un sector crítico (fintech/banca, salud, gobierno) y el usuario elige `1. MVP`, aclara que el MVP sirve únicamente como prototipo controlado con datos sintéticos y señala qué bloqueadores regulatorios exige antes de producción real.*

Consulta la matriz en [standards-and-tools.md](./references/standards-and-tools.md), el perfil por producto en [product-profiles.md](./references/product-profiles.md) y la guía de extensiones opcionales (`modern-web-guidance`, `Context7`, Matt Pocock, Cloudflare Security Audit, etc.) en [ecosystem-integrations.md](./references/ecosystem-integrations.md).

### 2. Elegir el modo de operación

#### Modo A — Planificar un proyecto nuevo
1. Define problema, usuarios, requisitos funcionales y no funcionales (usando **ISO/IEC 25010:2023**, priorización **MoSCoW** y criterios de aceptación verificables), alcance del **MVP**, **DoR** y **DoD**.
2. Establece la estructura documental base (`README.md`, `ARCHITECTURE.md`, ADRs, etc.) consultando [documentation-and-product.md](./references/documentation-and-product.md).
3. Coordina la aplicación por áreas activando (si están disponibles) o cubriendo las skills especializadas:
   * Regulación, licencias y requisitos específicos de industria (fintech, salud, gobierno, videojuegos, etc.) -> `swe-domain-discovery`
   * Arquitectura, resiliencia y calidad de código -> `swe-architecture-design`
   * Seguridad, privacidad, licencias y cadena de suministro -> `swe-security-privacy`
   * Pruebas y QA -> `swe-qa-testing`
   * Auditoría dinámica y seguridad en navegador (Playwright) -> `swe-browser-audit`
   * UX/UI, responsive, accesibilidad y analítica -> `swe-ux-accessibility`
   * Bases de datos, APIs, concurrencia y rendimiento -> `swe-data-apis`
   * Git, CI/CD, infraestructura, incidentes y FinOps -> `swe-devops-operations`
   * Aplicaciones con IA / LLMs / agentes en producto -> `swe-ai-engineering`
   * Context Engineering, ahorro de tokens y control de *vibe coding* al programar con IA (`CONSTITUTION.md`, `AGENTS.md`, `MEMORY.md`, `TASK_SPEC.md`) -> `swe-ai-workflow`
   * Cumplimiento legal base, borradores (privacidad/TyC/cookies/PI/contratos/fiscal/NOM-151) y lanzamiento `0/36` -> `swe-legal-compliance`
   * Paquete integral de entrega formal, transferencia de conocimiento y documentación viva (`PROJECT-HANDOVER/`) -> `swe-project-handover`
4. Si `modern-web-guidance` o `Context7` existen en el entorno, recomiéndalos o consúltalos para no generar diseño ni código genérico/obsoleto (ver [ecosystem-integrations.md](./references/ecosystem-integrations.md)).

#### Modo B — Auditar un repositorio o proyecto existente
1. Si hay Python 3 disponible, ejecuta primero el escaneo rápido de solo lectura usando el script [repo_audit_scan.py](./scripts/repo_audit_scan.py) desde la ruta resuelta de esta skill (no relativa al CWD del proyecto):
   `python3 <ruta-de-la-skill>/scripts/repo_audit_scan.py <ruta-del-repo>` (en Windows usa `python`; agrega `--format json` si necesitas procesar la salida estructurada).
   *(Detecta stack en raíz y monorepos estándar, documentación base, lockfiles, CI, archivos `.env` en disco o rastreados en Git —incluso anidados— y posibles secretos sin imprimir valores).*
2. Usa como guía base el checklist de [audit-checklist.md](./examples/audit-checklist.md) e inspecciona estructura, dependencias, CI/CD, datos y código.
3. Evalúa por bloques priorizando riesgos críticos (seguridad, secretos, pérdida de datos, fallos de producción, escalabilidad) antes que mejoras cosméticas.
4. Si la auditoría es profunda en un dominio, aplica la skill `swe-*` correspondiente.
5. Entrega un informe accionable agrupado en: **Crítico (bloqueante)**, **Importante (corto plazo)** y **Recomendado (mejora continua)**. *(Cuando consolides hallazgos de seguridad/navegador clasificados en 4 niveles: `Crítico` -> Crítico; `Alto`/`Medio` -> Importante; `Bajo` -> Recomendado).*

#### Modo C — Generar artefactos y plantillas
Genera directamente los documentos solicitados tomando como base [documentation-and-product.md](./references/documentation-and-product.md) y las plantillas listas de `./examples/`:
* [ARCHITECTURE.md](./examples/ARCHITECTURE.md) y registros **ADR** (*Architecture Decision Records*)
* [SECURITY.md](./examples/SECURITY.md), [CONTRIBUTING.md](./examples/CONTRIBUTING.md), `README.md`, `CHANGELOG.md`
* [pull_request_template.md](./examples/pull_request_template.md) y [dor-dod-checklist.md](./examples/dor-dod-checklist.md)
* *(Para generar, auditar o cerrar un paquete completo de transferencia `PROJECT-HANDOVER/` de 18 puntos, usa `swe-project-handover`.)*

## Criterios de verificación
* Todo requisito o recomendación indica a qué nivel de riesgo aplica (evita sobreingeniería innecesaria en MVPs).
* Las referencias normativas y herramientas recomendadas coinciden con el stack real del proyecto (consulta [standards-and-tools.md](./references/standards-and-tools.md)).
* Las brechas detectadas incluyen un paso concreto de remediación.
