# Arquitectura, Diseño y Calidad de Código

## 1. Arquitectura y diseño de software

### Principio fundamental
El proyecto debe tener una arquitectura definida antes de comenzar a implementar funcionalidades.

| Buena práctica | Descripción |
| :--- | :--- |
| **Arquitectura definida** | Establecer la arquitectura antes de desarrollar. |
| **Separación de responsabilidades** | Cada componente debe tener una responsabilidad clara. |
| **Bajo acoplamiento** | Evitar dependencias innecesarias entre módulos. |
| **Alta cohesión** | Mantener juntas las funcionalidades relacionadas. |
| **SOLID** | Aplicar los cinco principios de diseño orientado a objetos (SRP, OCP, LSP, ISP, DIP). |
| **DRY** | *Don't Repeat Yourself*: evitar duplicación innecesaria de lógica y conocimiento. |
| **KISS** | *Keep It Simple, Stupid*: evitar complejidad innecesaria. |
| **YAGNI** | *You Aren't Gonna Need It*: no implementar funcionalidades que todavía no se necesitan. |
| **Clean Architecture** | Separar dominio, aplicación, infraestructura y presentación cuando corresponda. |
| **Domain-Driven Design (DDD)** | Modelar el software de acuerdo con el dominio del negocio cuando aporte valor. |
| **Design Patterns** | Aplicar patrones de diseño cuando resuelvan problemas reales. |
| **Dependency Injection** | Gestionar dependencias sin acoplar implementaciones concretas. |
| **API First** | Definir contratos de API antes de implementar consumidores y proveedores, cuando sea conveniente. |
| **Versionado** | Controlar cambios incompatibles en APIs y componentes. |
| **Escalabilidad** | Diseñar considerando el crecimiento esperado. |
| **Modularidad** | Permitir evolucionar componentes independientemente. |
| **ADR** | Registrar decisiones arquitectónicas importantes (*Architecture Decision Records*). |

### Estándares y referencias
* **ISO/IEC/IEEE 42010:2022:** descripción de arquitectura de sistemas y software.
* **ISO/IEC 25010:2023:** modelo de calidad del producto software.
* **IEEE 1016:** descripción del diseño de software.

---

## 2. Calidad del código y estándares de programación

| Buena práctica | Descripción |
| :--- | :--- |
| **Coding Standards** | Convenciones de programación definidas y compartidas por el equipo. |
| **Naming Conventions** | Nombres claros, expresivos y consistentes. |
| **Linting** | Detección automática de problemas de estilo y errores potenciales. |
| **Formatting** | Formato automático y uniforme en todo el repositorio. |
| **Static Analysis** | Análisis estático del código para detectar bugs, smells y vulnerabilidades. |
| **Code Review** | Revisión de código por otros desarrolladores antes de integrar. |
| **Pull Requests** | Integrar cambios mediante solicitudes revisables y acotadas. |
| **Peer Review** | Revisión entre compañeros para compartir contexto y detectar fallos. |
| **Refactoring** | Mejorar la estructura interna del código sin cambiar su comportamiento esperado. |
| **Technical Debt Management** | Identificar, registrar y gestionar deuda técnica de forma consciente. |
| **Error Handling** | Gestionar errores de forma consistente y predecible sin tragar excepciones. |
| **Logging** | Registrar eventos relevantes sin exponer datos sensibles (contraseñas, tokens, PII). |
| **Documentation** | Documentar componentes, contratos públicos y decisiones importantes. |
| **Type Safety** | Utilizar sistemas de tipos apropiados para prevenir errores en tiempo de compilación/análisis. |
| **Immutability** | Evitar modificaciones innecesarias de estado compartido. |
| **Complexity Management** | Controlar complejidad ciclomática y cognitiva dividiendo funciones complejas. |
| **Code Duplication Detection** | Detectar y consolidar código duplicado. |
| **Dead Code Removal** | Eliminar código, importaciones, flags y archivos sin uso. |

### Herramientas recomendadas
* **Calidad y análisis estático:** SonarQube / SonarCloud, CodeQL, Semgrep.
* **Linters, formato y analizadores:** ESLint, Prettier, EditorConfig, Roslyn Analyzers, StyleCop.

---

## 3. Resiliencia, portabilidad y eficiencia desde el diseño

Especialmente importante al escalar de MVP a producción con miles de usuarios:

* **Design for Failure:** asumir que la red, APIs externas o discos fallarán; diseñar degradación controlada (**Graceful Degradation**) sin tumbar todo el sistema.
* **Patrones de resiliencia:** **Circuit Breaker** ante dependencias externas caídas y **Bulkhead Pattern** para aislar recursos/colas críticas y evitar fallos en cascada.
* **Portabilidad y evitar Vendor Lock-in innecesario:** abstraer servicios críticos externos (storage, correo, pagos, colas, LLM) detrás de interfaces simples cuando aporte valor, usar formatos estándar e interoperables y considerar **ISO/IEC 19941** y una estrategia de salida (*Exit Strategy*).
* **Eficiencia y sostenibilidad (*Green Software*):** evitar procesamiento y polling innecesario, controlar uso de memoria y transferencia de datos (reduciendo tanto huella energética como factura de nube).
