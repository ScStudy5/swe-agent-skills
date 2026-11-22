# Gestión de Producto y Documentación Técnica

## 1. Gestión de proyectos y desarrollo de producto

### Antes de desarrollar (Ingeniería de requisitos)
* **Definición del problema:** enunciar claramente qué problema se resuelve y por qué (evitar construir perfectamente el producto equivocado).
* **Identificación de usuarios y restricciones técnicas:** perfiles, roles, contexto de uso, presupuesto y límites del entorno.
* **Levantamiento de requisitos (SRS ligero en Nivel 1–2; formal en Nivel 3):**
  * **Funcionales:** qué debe hacer el sistema.
  * **No funcionales:** seguridad, rendimiento, fiabilidad, mantenibilidad, accesibilidad, compatibilidad (alineados a ISO/IEC 25010).
* **Requisitos verificables, sin contradicciones y priorización MoSCoW:** clasificar en *Must / Should / Could / Won't* y validar coherencia antes de construir.
* **Prototipos y validación temprana:** validar flujos críticos o modelado de procesos (**BPMN** en sistemas complejos) con usuarios/stakeholders antes de codificar en grande.
* **Historias de usuario, criterios de aceptación/rechazo y trazabilidad:** vincular requisitos clave con tareas, pruebas y releases.
* **Product Backlog, riesgos, estimaciones y definición de MVP:** alcance mínimo viable que aporta valor real y es mantenible.

### Durante el desarrollo y analítica de producto
* Metodología ágil adaptada al equipo (**Scrum**, **Kanban** u otra apropiada) y control de cambios en requisitos.
* **Definition of Ready (DoR)** y **Definition of Done (DoD)**.
* Seguimiento de tareas, incidencias, deuda técnica y evaluación de viabilidad/obsolescencia de dependencias.
* **Observación del producto (Product Analytics):** medir retención, embudos/conversión, funcionalidades usadas, abandono, feedback de usuarios y experiencia real (**RUM**) aplicando minimización de datos y política de privacidad.
* **Gobernanza formal (Nivel 3 / equipos grandes):** gestión de configuración (SCM), matriz **RACI**, gestión de proveedores tecnológicos y política explícita de soporte/mantenimiento por versión.

### Al finalizar una entrega / release
* Validación de requisitos y criterios de aceptación.
* Aprobación de funcionalidades (UAT cuando corresponda).
* Revisión de seguridad y validación de rendimiento.
* Actualización de documentación, `CHANGELOG.md` y registro de versión (SemVer + tag).

---

## 2. Documentación técnica recomendada

Un proyecto profesional debe poder ser comprendido, instalado, mantenido y continuado por otro desarrollador.

| Documento | Contenido | Nivel recomendado |
| :--- | :--- | :--- |
| `README.md` | Descripción, propósito, requisitos previos, instalación local, variables de entorno y comandos clave | Todos |
| `LICENSE` | Licencia de software explícita | Todos |
| `.env.example` | Plantilla de variables requeridas (sin valores secretos reales) | Todos |
| `CONTRIBUTING.md` | Flujo de ramas, commits, estilo de código, pruebas y cómo abrir PRs | Nivel 2 y 3 (o Open Source) |
| `CODE_OF_CONDUCT.md` | Normas de colaboración y convivencia | Open Source / equipos amplios |
| `CHANGELOG.md` | Historial de cambios por versión | Nivel 2 y 3 |
| `SECURITY.md` | Política y canal de reporte de vulnerabilidades | Nivel 2 y 3 |
| `ARCHITECTURE.md` | Visión general de arquitectura, componentes, límites y decisiones | Nivel 2 y 3 |
| **ADR** (`docs/adr/`) | Registro de decisiones arquitectónicas importantes | Nivel 2 y 3 |
| **API Documentation** | Contratos OpenAPI / Swagger, ejemplos de request/response y errores | Proyectos con API |
| **Database Documentation** | Modelo entidad-relación, diccionario de datos y reglas de retención | Proyectos con BD |
| **Environment & Deployment Guide** | Configuración de ambientes y procedimientos de despliegue | Nivel 2 y 3 |
| **Testing Guide** | Estrategia de pruebas, cómo ejecutarlas y datos de prueba | Nivel 2 y 3 |
| **Runbook** | Procedimientos operativos ante incidentes y tareas recurrentes | Nivel 2 y 3 |
| **Disaster Recovery Plan** | Recuperación ante desastres, RPO/RTO y restauración de respaldos | Nivel 3 |
| **User Manual** | Manual o guía de uso para usuarios finales / operadores | Según producto |

### Diagramas recomendados
* **Diagramas C4** (Contexto, Contenedores, Componentes, Código) para comunicar arquitectura a distintos niveles.
* **Diagramas de secuencia** para flujos críticos (autenticación, pagos, webhooks, procesos asíncronos).
* **Diagramas Entidad-Relación (ERD)** para bases de datos.
* **Diagramas de despliegue** para infraestructura y red.
* **Diagramas UML** cuando aporten claridad específica.
* Documentación explícita de flujos críticos y dependencias externas.

---

## 3. Plantilla estándar de ADR (Architecture Decision Record)

```markdown
# ADR-XXXX: [Título corto de la decisión]

- **Fecha:** YYYY-MM-DD
- **Estado:** Propuesto | Aceptado | Reemplazado por ADR-YYYY | Obsoleto
- **Contexto:** ¿Qué problema o restricción motiva esta decisión?
- **Opciones consideradas:**
  1. Opción A (pros / contras)
  2. Opción B (pros / contras)
- **Decisión:** ¿Qué se decidió y por qué?
- **Consecuencias:** Impacto técnico, deuda aceptada, riesgos y requisitos operativos.
```
