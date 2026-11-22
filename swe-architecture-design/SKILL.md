---
name: swe-architecture-design
description: >-
  Guía profesional para arquitectura de software y calidad de código: definición
  arquitectónica previa, SOLID, DRY, KISS, YAGNI, Clean Architecture, DDD, DI,
  API First, ADRs, estándares de código, linting, refactoring, deuda técnica y
  análisis estático (ISO 42010, ISO 25010, IEEE 1016). Usar al diseñar sistemas,
  revisar código/PRs, refactorizar o redactar ADRs.
---

# Arquitectura, Diseño y Calidad de Código

Aplica esta skill cuando diseñes la estructura de un sistema, revises la calidad de un código existente o documentes decisiones técnicas.

## Regla fundamental
**Arquitectura definida antes de implementar:** no escribas funcionalidades complejas sin haber establecido límites entre módulos, responsabilidades, dependencias y estrategia de evolución.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de introducir capas complejas (DDD, Clean Architecture completa o microservicios) en un MVP.

* **Documentación vigente del stack:** si vas a implementar patrones o código dependientes de un framework o librería concreta (React, Next.js, Prisma, Supabase, FastAPI, .NET, etc.) y **`Context7`** está disponible en el entorno, consulta primero la documentación de la versión exacta del proyecto para evitar APIs obsoletas o código genérico.

## Flujo de trabajo

### 1. Planificar o diseñar arquitectura (Proyecto / Módulo nuevo)
1. Evalúa el tamaño y complejidad real del sistema para evitar sobreingeniería (**KISS** y **YAGNI**) y **compara explícitamente 2–3 arquitecturas candidatas** antes de cerrar el stack:
   * Evalúa en cada opción: **experiencia del usuario (latencia y *cold starts* en capas gratuitas —p. ej. servicios que duermen tras 15 min vs. Edge/Workers—)**, costo operativo, límites del plan, portabilidad (*sin vendor lock-in*) y esfuerzo de mantenimiento.
   * Usa capas simples con separación de responsabilidades en MVPs.
   * Aplica **Clean Architecture** (dominio, aplicación, infraestructura, presentación) y **Domain-Driven Design (DDD)** cuando la lógica de negocio compleja lo justifique.
2. Verifica los principios estructurales en [architecture-and-code-quality.md](./references/architecture-and-code-quality.md):
   * Alta cohesión y bajo acoplamiento, **SOLID**, **Dependency Injection**, modularidad y escalabilidad.
   * **API First** y versionado cuando existan consumidores independientes.
3. Registra las decisiones clave en un **ADR** (*Architecture Decision Record*) y actualiza `ARCHITECTURE.md` (consulta **ISO/IEC/IEEE 42010** e **IEEE 1016** como referencia).

### 2. Auditar código y diseño existente
Inspecciona el código buscando:
1. **Acoplamiento y responsabilidades:** lógica de negocio mezclada con UI, rutas HTTP o acceso directo a BD; dependencias circulares o concretas sin inversión de dependencias.
2. **Complejidad y deuda técnica:** funciones largas, alta complejidad ciclomática/cognitiva, código duplicado (**DRY**), código muerto, estado mutable innecesario o manejo inconsistente de errores.
3. **Estándares e higiene:** convenciones de nombres, seguridad de tipos (*Type Safety*), logging sin fuga de datos sensibles, configuración de linters/formatters y análisis estático (ESLint, Prettier, EditorConfig, Roslyn/StyleCop, SonarQube, CodeQL, Semgrep).
4. **Propuesta de refactoring:** sugiere mejoras incrementales que conserven el comportamiento esperado y prioriza por impacto en mantenibilidad y riesgo.

### 3. Generar artefactos y configuración
Según la necesidad, genera:
* Propuesta de estructura de carpetas y diagrama de componentes (C4 / Mermaid).
* Archivos **ADR** listos para versionar en `docs/adr/`.
* Configuraciones base de `.editorconfig`, reglas de linter/formatter y checklists de **Code Review / Pull Request**.

## Criterios de verificación
* Cada recomendación arquitectónica justifica el problema que resuelve (sin patrones forzados ni abstracciones prematuras).
* Los hallazgos de auditoría señalan archivo/símbolo concreto, principio afectado y corrección sugerida.
* Toda decisión estructural relevante queda trazable en un ADR.
