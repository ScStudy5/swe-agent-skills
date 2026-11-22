# Transparencia de Estado: Problemas Conocidos, Deuda Técnica y Riesgos

- **Última actualización:** `[YYYY-MM-DD]`
- **Commit / Versión:** `[vX.Y.Z / <git-sha>]`
- **Responsable:** `[Rol / Nombre]`

> Plantilla consolidada del Punto 11 (`11-HISTORY-AND-KNOWN-ISSUES/`). En Nivel 2–3, separa cada sección en su archivo dedicado (`KNOWN_ISSUES.md`, `BUG_BACKLOG.md`, `TECHNICAL_DEBT.md`, `LESSONS_LEARNED.md`, `RISKS_REGISTER.md`, `OPEN_QUESTIONS.md`, `DECISIONS_HISTORY.md`).

---

## 1. Problemas conocidos activos (`KNOWN_ISSUES.md`)
| ID | Descripción | Impacto / Severidad | Condición que lo dispara | Workaround actual | Enlace / Ticket |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `KI-01` | `[Ej. Exportación CSV > 50k filas excede timeout]` | `[Medio]` | `[Reportes anuales sin filtro]` | `[Filtrar por trimestre]` | `[#123]` |

## 2. Deuda técnica consciente (`TECHNICAL_DEBT.md`)
| ID | Área / Archivo | Qué se simplificó y por qué | Riesgo si crece el tráfico | Esfuerzo estimado | Remediación sugerida |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TD-01` | `[src/reports/]` | `[Generación síncrona en MVP]` | `[Bloquea workers HTTP]` | `[M — 3 días]` | `[Mover a cola asíncrona + DLQ]` |

## 3. Registro de riesgos (`RISKS_REGISTER.md`)
| ID | Riesgo | Probabilidad | Impacto | Plan de mitigación / contingencia | Dueño |
| :--- | :--- | :-: | :-: | :--- | :--- |
| `R-01` | `[Dependencia única de proveedor externo X]` | `[Media]` | `[Alto]` | `[Interfaz desacoplada + fallback/degradación]` | `[Tech Lead]` |

## 4. Preguntas abiertas (`OPEN_QUESTIONS.md`)
| ID | Pregunta / Definición pendiente | Impacto | Quién decide | Fecha objetivo |
| :--- | :--- | :--- | :--- | :--- |
| `OQ-01` | `[Ej. ¿Política de retención de logs será de 90 o 365 días?]` | `[Costos + cumplimiento]` | `[Legal / PO]` | `[YYYY-MM-DD]` |

## 5. Lecciones aprendidas (`LESSONS_LEARNED.md`)
* **Qué funcionó bien (conservar):** `[Ej. Migraciones automáticas + pruebas de contrato evitaron regresiones en releases.]`
* **Qué falló o dolió (no repetir):** `[Ej. Un cambio sin índice en tabla de auditoría degradó latencia en prod; revisar EXPLAIN antes de merge.]`

## 6. Historial resumido de decisiones clave (`DECISIONS_HISTORY.md`)
| Fecha | Decisión | Contexto / Alternativas descartadas | Referencia ADR |
| :--- | :--- | :--- | :--- |
| `[YYYY-MM-DD]` | `[Ej. Adoptar monolito modular en lugar de microservicios]` | `[Equipo pequeño, prioridad velocidad y bajo costo operativo]` | `[../../docs/adr/ADR-0001.md]` |
