---
name: swe-data-apis
description: >-
  Guía profesional para bases de datos (modelado, normalización, ACID, índices,
  migraciones, backups y restore testing), APIs (REST, OpenAPI, versionado, DTOs,
  Problem Details RFC 9457, idempotencia, retries, Correlation IDs) y rendimiento
  (N+1, caché, Core Web Vitals, colas asíncronas, Performance Budgets). Usar al
  diseñar esquemas, contratos de API o diagnosticar cuellos de botella.
---

# Bases de Datos, APIs y Rendimiento

Aplica esta skill cuando diseñes o revises modelos de datos, contratos de API entre servicios o cuellos de botella de rendimiento.

## Regla fundamental
**Integridad de datos, contratos explícitos y optimización basada en evidencia:** protege la consistencia desde el esquema, desacopla contratos de API y optimiza cuellos de botella reales sin sobreingeniería prematura.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de exigir infraestructura de Nivel 3 (DRP formal, réplicas de lectura, DAMA-DMBOK).

## Flujo de trabajo

### 1. Planificar o diseñar datos, APIs y rendimiento
1. **Base de datos:**
   * Define convenciones claras de tablas, columnas, relaciones, identificadores (UUID/autoincrement según caso), fechas/zonas horarias (UTC), estrategia de concurrencia y límites de transacciones.
   * Aplica normalización equilibrada, integridad referencial, `constraints`, índices estratégicos, migraciones versionadas, `connection pooling` y estrategia de respaldos con **pruebas periódicas de restauración (*Restore Testing*)**.
   * Define políticas de retención, **Audit Trail**, cifrado, **Data Masking** en no-producción y **Soft Delete** solo cuando aporte valor sin romper integridad.
2. **APIs y comunicación entre servicios:**
   * Adopta **RESTful** cuando corresponda, documenta con **OpenAPI / Swagger**, versiona endpoints, usa **DTOs** y valida todas las solicitudes.
   * Estandariza errores con **Problem Details (RFC 9457)** y códigos HTTP semánticamente correctos.
   * Incorpora paginación, filtrado/ordenamiento, límites de tamaño, **Rate Limiting**, **CORS**, **timeouts**, **retries con backoff exponencial**, **idempotencia** en operaciones críticas y **Correlation IDs**.
3. **Rendimiento desde el diseño:**
   * Previene consultas **N+1**, pagina grandes volúmenes, usa caché con estrategia de invalidación clara, procesamiento asíncrono/colas cuando aplique y **Performance Budgets** (incluyendo **Core Web Vitals** en web).

Consulta el catálogo completo en [databases-apis-performance.md](./references/databases-apis-performance.md).

### 2. Auditar bases de datos, APIs y cuellos de botella
Busca sistemáticamente:
1. **Datos:** falta de migraciones reproducibles, ausencia de constraints/FKs, índices faltantes en claves de búsqueda/join, transacciones abiertas con llamadas HTTP externas, mezcla de datos de producción en dev/QA, respaldos nunca probados.
2. **APIs:** exposición directa de entidades de BD sin DTOs, errores inconsistentes o con stack traces, endpoints sin paginación o límites de payload, llamadas externas sin timeout o sin manejo de reintentos/idempotencia, ausencia de Correlation IDs.
3. **Rendimiento:** consultas N+1, cargas síncronas bloqueantes, falta de compresión/code splitting/lazy loading o fugas de memoria.

### 3. Generar artefactos y contratos
Genera cuando se soliciten:
* Esquemas SQL/migraciones, diccionario de datos o políticas de retención/backup.
* Especificaciones **OpenAPI**, modelos de error **RFC 9457** (ver plantilla en [rfc9457-error-examples.json](./examples/rfc9457-error-examples.json)) y colecciones de prueba (Postman/Bruno).
* Presupuestos de rendimiento, cuotas/fallbacks para integraciones LLM y plan de optimización priorizado por impacto.

## Criterios de verificación
* Ningún endpoint devuelve entidades internas sin DTO ni expone errores inconsistentes fuera del formato estándar.
* Toda operación de BD crítica usa transacciones ACID acotadas y migraciones versionadas.
* Cada optimización de rendimiento propuesta está respaldada por un cuello de botella real o riesgo medible (evitando optimización prematura sin datos).
