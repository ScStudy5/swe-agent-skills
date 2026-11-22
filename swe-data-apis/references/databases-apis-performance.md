# Bases de Datos, APIs y Rendimiento

## 1. Bases de datos y gestión de información

| Buena práctica | Descripción |
| :--- | :--- |
| **Database Design** | Diseñar correctamente el modelo de datos según los patrones de acceso e integridad. |
| **Normalización** | Evitar redundancia innecesaria y anomalías de actualización. |
| **Referential Integrity** | Mantener relaciones consistentes entre entidades. |
| **Constraints** | Utilizar restricciones de integridad (`NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY`). |
| **Indexing** | Optimizar consultas frecuentes mediante índices adecuados (sin sobreindexar escrituras). |
| **Query Optimization** | Evitar consultas costosas, `SELECT *` innecesarios y escaneos completos. |
| **Transactions** | Garantizar operaciones atómicas cuando corresponda. |
| **ACID** | Garantizar Atomicidad, Consistencia, Aislamiento y Durabilidad en transacciones. |
| **Connection Pooling** | Reutilizar conexiones eficientemente bajo concurrencia. |
| **Migrations** | Versionar y automatizar cambios en la estructura de datos de forma reversible/controlada. |
| **Backup** | Realizar respaldos periódicos automatizados (BD, archivos/documentos y configuraciones críticas), verificando que realmente se generen y manteniendo copias fuera del proveedor principal (*off-site*) cuando el riesgo lo amerite. |
| **Restore Testing** | Comprobar periódicamente que los respaldos realmente se pueden recuperar (no basta con tener backups; hay que demostrar su restauración). |
| **Row Level Security (RLS) y Permisos** | En bases de datos expuestas vía API/BaaS (p. ej. PostgreSQL/Supabase) o multi-tenant: activar **RLS** en todas las tablas expuestas, crear políticas `SELECT`/`INSERT`/`UPDATE`/`DELETE`, probar acceso cruzado entre usuarios, revisar permisos de vistas/funciones y políticas por bucket de Storage, y nunca exponer llaves privilegiadas (`service_role`) en el cliente. |
| **Data Encryption** | Proteger datos sensibles en tránsito y en reposo. |
| **Data Masking** | Ocultar o anonimizar información sensible en entornos no productivos. |
| **Data Retention** | Definir cuánto tiempo se conserva cada tipo de información y cuándo se purga. |
| **Audit Trail** | Registrar quién modificó qué y cuándo en operaciones importantes. |
| **Soft Delete** | Aplicar eliminación lógica cuando sea apropiado (cuidando índices únicos e integridad). |
| **Disaster Recovery** | Preparar recuperación ante desastres (RPO/RTO definidos). |
| **Data Validation** | Garantizar integridad y formato de los datos antes de persistir. |

### Convenciones adicionales recomendadas
* Convenciones uniformes para tablas, columnas y relaciones.
* Política de fechas y zonas horarias (almacenamiento en UTC).
* Política de identificadores (UUIDv4/v7, secuenciales internos vs IDs públicos).
* Estrategia de concurrencia (bloqueo optimista/pesimista) y límites de duración de transacciones.
* Gestión de datos históricos / archivado.
* Separación estricta de datos de **producción, desarrollo y pruebas**.
* Control de acceso mínimo a la base de datos y **monitoreo de consultas lentas**.

---

## 2. APIs y comunicación entre servicios

Reglas para proyectos con backend, frontend, apps móviles o integraciones externas:

* **RESTful API** cuando sea apropiado (o GraphQL/gRPC cuando el caso lo justifique).
* **OpenAPI / Swagger** como contrato vivo y documentación de endpoints.
* **Versionado de endpoints** para evolucionar sin romper clientes existentes.
* **DTOs (Data Transfer Objects)** para desacoplar el contrato público del modelo interno de BD.
* **Validación estricta de solicitudes** y **respuestas HTTP correctas** (`200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `429`, `5xx`).
* **Manejo estandarizado de errores:** usar **Problem Details (RFC 9457)** (`type`, `title`, `status`, `detail`, `instance`) para que todas las APIs comuniquen errores de forma consistente.
* **Paginación**, **filtrado** y **ordenamiento** en colecciones.
* **Rate Limiting** y **límites de tamaño de solicitudes** contra abuso de recursos.
* **Autenticación y autorización** en cada endpoint protegido + **CORS** configurado estrictamente.
* **Timeouts** explícitos en toda llamada de red.
* **Retries con backoff exponencial** (y *jitter*) solo en fallos transitorios.
* **Idempotencia** en operaciones que lo requieran (ej. pagos, creación mediante `Idempotency-Key`).
* **Correlation IDs** propagados entre servicios para trazabilidad de solicitudes.
* **Contratos de API** validados (y herramientas como **Postman** o **Bruno**).

---

## 3. Rendimiento y optimización

### Prácticas de alto impacto y costo ~0 (Aplicar desde el inicio)
* **Base de datos y backend:**
  * **Solo columnas útiles:** evitar `SELECT *` y traer únicamente los campos necesarios.
  * **Prevención de N+1 Queries**, **índices en consultas comunes** y **paginación** en listados.
  * **Servidor junto a la BD** (misma región/VPC para reducir latencia y evitar cobros por transferencia entre regiones).
  * **Pool de conexiones**, **peticiones independientes en paralelo** y **colas de trabajos / Background Jobs** para procesos pesados.
* **Frontend y red:**
  * **Imágenes en WebP / AVIF**, **fuentes propias (*self-hosted*)**, **compresión Brotli/Gzip** y **caché en el navegador** (`Cache-Control`).
  * **Retardo en búsqueda (*debounce*)**, **evitar llamadas duplicadas** (deduplicación/caché cliente) y **evitar renders innecesarios**.
  * **Virtualizar listas largas**, **JS por página (*code splitting*)**, **Lazy Loading**, **Tree Shaking** y **scripts de terceros diferidos** (`defer`/`async`).
  * **Probar velocidad real en móviles y redes lentas** (throttling 3G/4G) y optimizar **Core Web Vitals** (LCP, INP, CLS).
* **Presupuestos y pruebas:** definir **Performance Budgets**, vigilar **fugas de memoria** y probar carga con **k6** / **JMeter**.

### Prácticas según escala (Evitar sobrecostos innecesarios, activar cuando el proyecto escale mucho)
* **Múltiples instancias y auto-scaling:** innecesario en MVPs pequeños (1 instancia optimizada suele bastar); **indispensable con techo máximo de réplicas** cuando el proyecto escale a alto tráfico o alta disponibilidad.
* **Render en servidor (SSR / Edge):** en dashboards privados suele convenir SPA estática por costo/simplicidad; **conviene** en sitios públicos dependientes de SEO o primer pintado crítico y escala grande.
* **CDN dedicado, caché distribuida (Redis cluster) y réplicas de lectura:** comenzar con opciones incluidas/simples y escalarlas cuando las métricas reales muestren saturación.

---

## 4. Resiliencia, concurrencia y gobierno práctico de datos

* **Concurrencia, pagos e integridad:** prevenir **condiciones de carrera** (*race conditions*) mediante bloqueos optimistas/pesimistas, restricciones `UNIQUE` e **idempotencia** en operaciones críticas y webhooks. En pagos en línea: delegar a pasarela especializada (PCI-DSS, sin guardar datos completos de tarjetas), **verificar firmas de webhooks**, confirmar el estado del pago directamente en el backend, evitar cargos duplicados y definir un procedimiento operativo para **resolver pagos fallidos** (*dunning*/reintentos).
* **Colas y fallos asíncronos:** usar **Dead Letter Queues (DLQ)** para mensajes fallidos tras agotar reintentos y evitar estados inconsistentes entre BD y servicios externos (patrón *Outbox* o reconciliación cuando corresponda).
* **Migraciones compatibles hacia atrás:** separar cambios de esquema destructivos en fases (*expand and contract*) para desplegar sin tiempo de inactividad.
* **Continuidad (RTO y RPO):** definir cuánto tiempo máximo puede estar caído el sistema (**RTO**) y cuántos datos máximos se tolera perder (**RPO**), alineando con esto la frecuencia de backups y *restore testing*.
* **Gobierno y portabilidad de datos (Nivel 2–3):** definir **Data Ownership** (responsable de cada conjunto de datos), calidad y detección de duplicados, clasificación de sensibilidad, eliminación segura, validación estricta de importaciones/exportaciones y formatos portables (referencias Nivel 3: **ISO 8000**, **ISO/IEC 11179**, **DAMA-DMBOK**).

---

## 5. Integración, costos y resiliencia en APIs de IA / LLMs

*(Ver también `swe-ai-engineering` para gobernanza, evals, sesgos y seguridad de prompts.)*

Cuando la aplicación consuma modelos de lenguaje o embeddings externos:

* **Salidas estructuradas:** exigir y validar esquemas estrictos (JSON Schema) en respuestas que alimentan lógica de negocio.
* **Presupuestos y cuotas:** definir límites de tokens de entrada/salida, cuotas por usuario/tenant y alertas de gasto.
* **Resiliencia de red:** configurar **timeouts** acordes a inferencia/streaming, **retries con backoff exponencial** solo en errores transitorios (`429`/`5xx`) y **fallback** a un modelo secundario o degradación elegante si el proveedor cae.
* **Caché:** cachear embeddings y respuestas deterministas o frecuentes cuando corresponda para reducir latencia y costo.
* **Versionado y observabilidad:** fijar versiones de modelo/prompts explícitas y medir latencia por petición, tasa de error y consumo de tokens (con Correlation IDs).
