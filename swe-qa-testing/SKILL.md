---
name: swe-qa-testing
description: >-
  Guía profesional de pruebas y aseguramiento de calidad (QA): pirámide de pruebas,
  25 tipos de testing (Unit, Integration, E2E, Contract, API, Load, Stress, Spike,
  Soak, Security, Accessibility, Mutation, Fuzz, Chaos, LLM Evals), estrategia de
  cobertura, datos sintéticos y automatización en CI (ISO/IEC/IEEE 29119). Usar al
  definir estrategias de QA, auditar suites de pruebas o redactar planes y casos
  de prueba (para auditoría dinámica de seguridad en navegador usar swe-browser-audit).
---

# Pruebas y Aseguramiento de Calidad (QA)

Aplica esta skill cuando diseñes una estrategia de pruebas, audites la suite de testing de un proyecto o generes planes y casos de prueba.

## Regla fundamental
**Todo proyecto debe tener una estrategia de pruebas:** no basta con probar manualmente que los botones funcionan. Las pruebas deben ser proporcionales al riesgo, automatizadas en CI y reproducibles.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de exigir pruebas avanzadas de Nivel 3 (Chaos, Load masivo, Mutation).

## Flujo de trabajo

### 1. Planificar estrategia de pruebas (Proyecto nuevo o módulo)
1. Define la pirámide de pruebas adecuada al tipo de sistema (web, API, móvil, microservicios, empresarial):
   * **Base:** Unit Testing rápido e independiente en lógica de negocio.
   * **Capa media:** Integration Testing + API / Contract Testing entre módulos y servicios.
   * **Cima:** End-to-End (E2E) y Smoke Testing sobre flujos críticos de negocio.
2. Selecciona qué pruebas especializadas aplican según riesgo en [testing-catalog.md](./references/testing-catalog.md) (rendimiento/carga, seguridad, accesibilidad, compatibilidad, regresión visual, mutation, fuzz, chaos, UAT).
3. Define política de datos de prueba: datos sintéticos/controlados, **nunca información personal real** en entornos de prueba.

### 2. Auditar la suite de pruebas existente
Evalúa:
1. **Cobertura útil vs. ilusoria:** verifica que los flujos críticos, bordes y errores estén probados (no perseguir el 100 % sin criterio ni depender solo de la métrica de cobertura).
2. **Calidad y confiabilidad:** busca pruebas frágiles (*flaky*), dependientes de orden o de datos externos inestables, pruebas comentadas/ignoradas en lugar de corregidas, o mocks excesivos que ocultan fallos de integración.
3. **Automatización en CI:** confirma que unitarias e integración corren en cada PR y E2E en flujos críticos o pre-despliegue.
4. **Higiene de datos:** verifica que no haya PII real en fixtures o semillas de prueba.

### 3. Generar artefactos y casos de prueba
Genera según la petición:
* Documento `Testing Guide` / Plan de QA (alcance, tipos de prueba, herramientas, criterios de entrada/salida, **ISO/IEC/IEEE 29119**).
* Casos de prueba estructurados (escenarios felices, límites, errores, concurrencia/seguridad).
* Implementación o refactorización de pruebas con las herramientas del stack (xUnit, NUnit, Jest, Vitest, Playwright, Cypress, Postman/Bruno, k6, JMeter, axe-core).

## Criterios de verificación
* La estrategia distingue claramente qué corre en cada commit/PR, qué corre nightly/pre-release y qué requiere validación manual (UAT/usabilidad).
* Toda prueba propuesta es independiente, determinista y usa datos controlados sin PII.
* No se recomiendan pruebas omitidas o assertions relajadas para "hacer pasar" la suite.
