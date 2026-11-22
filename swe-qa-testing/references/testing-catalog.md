# Catálogo de Pruebas y Buenas Prácticas de QA

## Principio fundamental
Todo proyecto debe tener una estrategia de pruebas. No basta con probar manualmente que los botones funcionan.

## 1. Tipos de prueba

| Tipo de prueba | Qué verifica |
| :--- | :--- |
| **Unit Testing** | Funciones, clases y unidades individuales aisladas. |
| **Integration Testing** | Comunicación e integración real entre componentes, módulos o base de datos. |
| **End-to-End (E2E)** | Flujos completos de extremo a extremo desde la perspectiva del usuario. |
| **Functional Testing** | Cumplimiento de requisitos y funcionalidades especificadas. |
| **Regression Testing** | Que los cambios nuevos no rompan funcionalidades anteriores. |
| **Smoke Testing** | Que las funciones esenciales del sistema operen tras un build o despliegue. |
| **Sanity Testing** | Que un cambio o corrección específica funcione correctamente. |
| **Acceptance Testing** | Que se cumplan formalmente los criterios de aceptación del negocio. |
| **UAT** (*User Acceptance Testing*) | Validación por usuarios finales o responsables del negocio. |
| **API Testing** | Contratos, códigos de respuesta, esquemas, errores y comportamiento de APIs. |
| **Contract Testing** | Compatibilidad de contratos entre consumidores y proveedores de servicios. |
| **Performance Testing** | Rendimiento general (latencia, tiempos de respuesta, uso de recursos). |
| **Load Testing** | Comportamiento del sistema bajo la carga normal y pico esperada. |
| **Stress Testing** | Comportamiento y punto de quiebre bajo condiciones extremas más allá del límite. |
| **Spike Testing** | Respuesta ante incrementos repentinos y bruscos de tráfico. |
| **Soak Testing** | Estabilidad y ausencia de fugas de memoria/conexiones durante periodos prolongados. |
| **Security Testing** | Vulnerabilidades, controles de autenticación/autorización e inyecciones. |
| **Accessibility Testing** | Accesibilidad para personas con distintas capacidades (WCAG 2.2, lectores de pantalla, teclado). |
| **Compatibility Testing** | Compatibilidad entre navegadores, dispositivos, resoluciones y sistemas operativos. |
| **Usability Testing** | Facilidad de uso, claridad de flujos y prevención de errores de usuario. |
| **Visual Regression Testing** | Cambios visuales o de maquetación inesperados entre versiones. |
| **Mutation Testing** | Calidad real y capacidad de detección de errores de las propias pruebas unitarias. |
| **Fuzz Testing** | Comportamiento y robustez ante entradas inesperadas, aleatorias o malformadas. |
| **Chaos Testing** | Resiliencia del sistema ante fallos controlados de infraestructura o red. |
| **LLM / AI Evaluations (Evals)** | Calidad, consistencia de salida estructurada, regresiones de prompts y resistencia a *prompt injection* en funciones con IA. |

---

## 2. Buenas prácticas de QA

* **Automatizar** las pruebas repetitivas.
* **Ejecutar en CI** las pruebas unitarias y de integración en cada cambio/PR.
* **Ejecutar E2E** en los flujos críticos del negocio.
* **Medir cobertura con criterio:** no perseguir el 100 % artificialmente ni depender exclusivamente de la cobertura de código (priorizar lógica crítica y mutaciones/aserciones reales).
* **Independencia y reproducibilidad:** mantener pruebas aisladas que no dependan del orden de ejecución ni de estado residual.
* **Sin dependencias externas inestables:** usar dobles de prueba, contenedores efímeros o entornos controlados.
* **Datos de prueba controlados:** utilizar datos sintéticos y **nunca utilizar información personal real** en entornos de prueba.
* **Cero pruebas rotas ignoradas:** corregir o actualizar las pruebas defectuosas en lugar de saltarlas (`skip`) indefinidamente.

---

## 3. Higiene previa a producción (*Release Hygiene*)
Antes de publicar, verificar explícitamente que:
* No existan errores críticos en consola ni enlaces/recursos rotos.
* No queden **endpoints de prueba/depuración** publicados ni **usuarios o contraseñas predeterminados**.
* No existan **datos ficticios / semillas de desarrollo** en producción.
* Los mensajes de error no revelen trazas ni información interna del servidor.
* Las validaciones críticas se ejecuten también en backend y los procesos críticos cuenten con pruebas automatizadas.
* Se haya probado el comportamiento **sin conexión (offline)** cuando aplique (PWA/móvil) y la degradación controlada cuando **falla un servicio externo**.

---

## 4. Estándares y herramientas recomendadas
* **Estándar:** ISO/IEC/IEEE 29119 (Pruebas de software).
* **Unitarias / Integración:** xUnit, NUnit, Jest, Vitest.
* **E2E:** Playwright, Cypress.
* **APIs:** Postman, Bruno.
* **Performance / Carga:** k6, JMeter.
* **Accesibilidad:** axe-core, Lighthouse.
