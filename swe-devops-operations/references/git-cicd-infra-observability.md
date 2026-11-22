# Git, CI/CD, Infraestructura y Observabilidad

## 1. Git, control de versiones y colaboración

| Práctica | Aplicación |
| :--- | :--- |
| **Git** | Control de versiones distribuido. |
| **GitHub Flow / Trunk-Based / Git Flow** | Estrategia de ramas: **GitHub Flow** (`main` siempre desplegable + ramas `feat/*`/`fix/*` + PR) recomendado por defecto en web/SaaS; *Trunk-Based* para integración diaria con feature flags; *Git Flow* si hay múltiples versiones mantenidas en paralelo (ver matriz y comandos `gh CLI` en [github-workflows-and-rulesets.md](./github-workflows-and-rulesets.md)). |
| **Conventional Commits** | Estandarización de mensajes de commit (`feat:`, `fix:`, `chore:`, etc.). |
| **Pull Requests** | Revisión obligatoria antes de integrar cambios. |
| **Branch Protection** | Protección de ramas principales (`main`, `develop`) contra push directo o merges sin checks. |
| **CODEOWNERS** | Definir responsables de revisión por directorio o componente. |
| **Semantic Versioning** | Versionado semántico (`MAJOR.MINOR.PATCH`). |
| **Tags** | Identificar versiones y releases inmutables. |
| **Changelog** | Registrar cambios importantes por versión (`CHANGELOG.md`). |
| **Gitignore** | Evitar subir artefactos compilados, dependencias o archivos locales/secretos. |
| **Gitattributes** | Normalizar fin de línea (LF/CRLF) y comportamiento de archivos binarios. |
| **Commit Signing** | Verificar autoría de commits con GPG/SSH cuando corresponda. |
| **Release Management** | Gestionar cortes, notas de versión y publicación controlada. |

Ejemplo de estructura de ramas (cuando se usa Git Flow):
```text
main
└── develop
    ├── feature/login
    ├── feature/dashboard
    ├── feature/user-management
    ├── release/1.0.0
    └── hotfix/security-patch
```

---

## 2. CI/CD y automatización

### CI — Integración continua
* Restaurar dependencias y compilar el proyecto.
* Ejecutar linters y análisis estático.
* Ejecutar pruebas unitarias y pruebas de integración.
* Ejecutar análisis de dependencias (**SCA**) y buscar secretos expuestos.
* Generar reportes de calidad y validar Pull Requests automáticamente.

### CD — Entrega y despliegue continuo
* Generación de artefactos y versionado automático.
* Construcción y escaneo de imágenes Docker.
* Despliegue en ambientes de desarrollo y staging.
* Aprobaciones manuales para producción cuando sean necesarias.
* Ejecución de migraciones de base de datos controladas.
* **Health Checks**, verificación posterior al despliegue y capacidad de **Rollback**.

### Ambientes recomendados

| Ambiente | Propósito |
| :--- | :--- |
| **Local** | Desarrollo individual. |
| **Development** | Integración continua de cambios del equipo. |
| **Testing / QA** | Pruebas de calidad y validación funcional. |
| **Staging** | Simulación fiel de producción previa a liberar. |
| **Production** | Usuarios reales. |

---

## 3. Infraestructura, DevOps y contenedores

* **Infrastructure as Code (IaC)** (Terraform, OpenTofu) y documentación de infraestructura.
* **Docker** y **Docker Compose** para entornos locales reproducibles cuando convenga.
* **Kubernetes** únicamente cuando la escala o complejidad operativa lo justifique.
* Configuración por **variables de entorno** y gestión segura de secretos.
* Separación estricta de infraestructura por ambientes.
* **Reverse Proxy**, **balanceo de carga** y **Auto Scaling** cuando corresponda.
* **HTTPS**, **DNS** correctamente configurado, **Firewall** y gestión mínima de puertos.
* **Gestión de recursos** (límites de CPU/RAM) y **gestión de certificados**.
* **Health Checks**, **Readiness** y **Liveness Probes**.
* Estrategias de despliegue **Blue-Green** o **Canary** cuando aporten valor.
* Automatización de tareas operativas repetitivas.

---

## 4. Monitoreo, observabilidad y mantenimiento

### Observabilidad
* **Logging** centralizado, **Metrics**, **Distributed Tracing** y **Alerting**.
* **APM** (*Application Performance Monitoring*) y monitoreo de errores (**Sentry**).
* Monitoreo de disponibilidad, bases de datos, infraestructura y consumo de recursos.
* **Correlation IDs** y **dashboards operativos** (**Prometheus**, **Grafana**).

### Mantenimiento continuo
* Actualización de dependencias y aplicación de parches de seguridad.
* Corrección de errores y gestión de deuda técnica.
* Revisión periódica de vulnerabilidades, certificados y compatibilidad con nuevas versiones.
* Pruebas de recuperación, análisis de logs y eliminación de funcionalidades obsoletas.

### Indicadores clave (incluyendo métricas DORA)

| Indicador | Qué mide |
| :--- | :--- |
| **Availability** | Disponibilidad del sistema. |
| **MTTR** | Tiempo medio de recuperación tras un incidente (*DORA*). |
| **MTTD** | Tiempo medio de detección de un incidente. |
| **Error Rate** | Porcentaje de solicitudes o ejecuciones con error. |
| **Latency** | Tiempo de respuesta. |
| **Throughput** | Solicitudes o transacciones procesadas por unidad de tiempo. |
| **Deployment Frequency** | Frecuencia de despliegues a producción (*DORA*). |
| **Change Failure Rate** | Porcentaje de despliegues que provocan fallos o rollbacks (*DORA*). |

### Herramientas recomendadas
* **CI/CD:** GitHub Actions, Azure DevOps.
* **Contenedores / IaC:** Docker, Trivy, Terraform, OpenTofu.
* **Monitoreo / Errores:** Prometheus, Grafana, Sentry.

---

## 5. Gestión de incidentes, releases confiables y FinOps

### Gestión de incidentes y operación
* **Clasificación de severidad y escalamiento:** definir qué es un incidente Crítico/Alto/Medio y quién responde.
* **Comunicación y respuesta:** procedimiento claro de emergencia, mitigación/rollback y registro histórico de incidentes.
* **Blameless Postmortem y RCA:** tras un incidente relevante, documentar la causa raíz sin buscar culpables y crear acciones preventivas concretas.
* **Resiliencia operativa:** definir **RTO / RPO**, validar failover cuando aplique, hacer simulacros de recuperación y planificar ventanas de mantenimiento. *(En Nivel 3: alineado a **ITIL 4** e **ISO/IEC 20000-1**).*

### Ingeniería de releases y distribución
* **Canales y candidatos:** gestionar **Release Candidates (RC)** y canales (`Preview` / `Beta` / `Stable`) según el producto.
* **Integridad de builds:** verificación con hashes, builds reproducibles, migraciones compatibles hacia atrás y retiro seguro de versiones vulnerables *(Nivel 3: **SLSA Framework** y **Sigstore**)*.

### FinOps, límites duros en nube y escalado progresivo

> **Advertencia crítica sobre Azure, AWS y GCP:** en la mayoría de los proveedores cloud grandes, las **alertas de presupuesto solo envían correos/notificaciones y NO apagan los recursos automáticamente**. Si se agotan los créditos gratuitos o hay un bucle de tráfico, la factura sigue subiendo.

* **Topes reales y protección desde el día 1:**
  * Configurar **topes duros (*hard spending caps*)** en plataformas/APIs que lo soporten (ej. límites mensuales de gasto en APIs de IA o servicios con *spend limit*).
  * En Azure/AWS/GCP: configurar alertas escalonadas (50 %, 80 %, 100 %), fijar **límites máximos estrictos de auto-scaling** (ej. `maxReplicas = 1 o 2` en MVP), poner **retención corta de logs** y revisar qué recursos cobran **por hora aunque no haya tráfico** (BDs administradas, NAT Gateways, IPs fijas, App Service Plans).
  * En **Nivel 1 (MVP)** y proyectos pequeños, preferir plataformas con precio fijo/tope predecible antes de aprovisionar servicios empresariales sin techo.
* **Control de recursos y Unit Economics:** vigilar cómputo, almacenamiento, transferencia de datos (*egress*), apagar entornos dev/staging ociosos y medir costo por usuario activo/transacción (**FinOps Framework** + **Green Software / SCI**).
* **Cuándo SÍ activar prácticas de alto costo (si el proyecto escala mucho):**
  * **En MVP / pequeña escala:** 1 instancia optimizada + BD en la misma región, SSR solo si se necesita SEO/carga pública crítica, CDN gratuito/incluido y monitoreo básico de errores.
  * **Cuando el tráfico y negocio escalen fuerte:** activar **múltiples instancias con auto-scaling acotado**, **SSR/Edge** donde mejore conversión, **CDN dedicado**, **APM completo y distributed tracing**, y réplicas/escalado de base de datos.
