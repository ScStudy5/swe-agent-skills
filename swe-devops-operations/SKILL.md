---
name: swe-devops-operations
description: >-
  Guía profesional de Git (GitHub Flow, Trunk-Based, Git Flow, Conventional Commits,
  SemVer, Rulesets/Branch Protection), CI/CD completo en GitHub Actions endurecido
  por commit SHA (CI, CD con Environments/OIDC, Releases, CodeQL, Dependabot,
  validación de PRs), infraestructura/contenedores (IaC, Docker, Kubernetes,
  Blue-Green/Canary) y observabilidad/FinOps (logging, tracing, Sentry,
  Prometheus/Grafana, métricas DORA). Usar al configurar repositorios GitHub,
  pipelines, despliegues, costos en nube o monitoreo.
---

# Git, CI/CD, Infraestructura y Observabilidad

Aplica esta skill cuando configures el flujo de trabajo de un repositorio, diseñes pipelines CI/CD, prepares infraestructura/contenedores o establezcas monitoreo y mantenimiento operativo.

## Regla fundamental
**Nunca despliegues directamente a producción** un cambio que no haya pasado por las verificaciones automatizadas correspondientes al riesgo de ese proyecto. Además, el trabajo no termina al publicar: debes saber qué ocurre en producción.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de proponer Kubernetes, despliegue multi-región o Blue-Green/Canary en proyectos pequeños.

## Flujo de trabajo

### 1. Planificar o configurar Git, CI/CD, Infraestructura y Observabilidad
1. **Git, GitHub y colaboración:** elige explícitamente el flujo de ramas (**GitHub Flow** recomendado por defecto en web/SaaS, **Trunk-Based Development** con feature flags o **Git Flow** si hay múltiples versiones mantenidas), **Conventional Commits**, Pull Requests con **Rulesets / Branch Protection** (comandos `gh CLI` y estrategia de merge en [github-workflows-and-rulesets.md](./references/github-workflows-and-rulesets.md)), `CODEOWNERS`, **Semantic Versioning**, tags, `CHANGELOG.md`, `.gitignore`, `.gitattributes`, Issue Forms y firma de commits cuando corresponda.
2. **Pipelines CI/CD endurecidos (SHA pinning + OIDC):**
   * **CI y seguridad:** restaurar dependencias -> compilar -> linters/análisis estático -> unit + integration tests -> validación de título/tamaño de PR -> SCA/secret scanning (Gitleaks/Trivy) + CodeQL -> Dependabot para Actions y dependencias.
   * **CD y Releases:** artefactos con checksums -> tags SemVer y GitHub Releases automáticos -> despliegue progresivo con **GitHub Environments** (`staging` -> `production` con aprobación manual y autenticación **OIDC** sin llaves cloud estáticas), migraciones controladas, **Health Checks**, verificación post-despliegue y **Rollback**.
3. **Infraestructura y contenedores:** **IaC** (Terraform/OpenTofu), Docker/Docker Compose, Kubernetes solo si la complejidad lo justifica, variables de entorno y secretos seguros, separación de ambientes, Reverse Proxy, HTTPS/TLS (con redirección HTTP -> HTTPS), DNS, firewall/puertos, permisos mínimos del servidor, protección perimetral (**CDN/WAF contra DDoS, bots y scraping**), límites de recursos/serverless/ancho de banda, autoscaling acotado, `readiness`/`liveness probes` y despliegues **Blue-Green** o **Canary** cuando aporten valor.
4. **Observabilidad, alertas y mantenimiento:** **Logging** estructurado con **Correlation IDs**, **Metrics**, **Distributed Tracing**, **Alerting** (caídas, errores 4xx/5xx, consumo/costos, actividad sospechosa, fallos de autenticación y fallos de backups), **APM**, monitoreo de errores (**Sentry**), disponibilidad (**Uptime Kuma** / probes), BD y métricas (**Prometheus/Grafana**), página de estado / aviso de mantenimiento cuando aplique, seguimiento de **métricas DORA** y rutina de actualización de dependencias/parches/certificados.

Consulta el detalle completo en [git-cicd-infra-observability.md](./references/git-cicd-infra-observability.md) y la guía operativa de GitHub en [github-workflows-and-rulesets.md](./references/github-workflows-and-rulesets.md).

### 2. Auditar flujos de entrega y operación
Revisa el proyecto buscando:
1. **Repositorio y GitHub:** ausencia de `.gitignore`/`.gitattributes`/`CODEOWNERS`, push directo a `main` permitido, falta de Rulesets/Branch Protection, ausencia de Dependabot o convenciones de PR/release.
2. **CI/CD y hardening:** builds manuales, acciones sin fijar por **commit SHA** (usando `@master`/`@main` o tags mutables sin control), permisos amplios en `GITHUB_TOKEN`, riesgo de *script injection* en `run:`, llaves cloud estáticas en lugar de **OIDC**, despliegues sin tests o migraciones acopladas sin rollback.
3. **Infraestructura:** secretos en Dockerfile o archivos IaC, contenedores corriendo como `root`, imágenes sin escanear (**Trivy**), falta de límites de CPU/memoria o health checks.
4. **Operación:** falta de alertas accionables, ausencia de dashboards/APM o logs sin Correlation IDs que impiden depurar incidentes.

### 3. Generar artefactos de automatización y operación
Genera cuando se soliciten tomando como base las plantillas endurecidas de `./examples/`:
* **Workflows de GitHub Actions (fijados por SHA):**
  * CI + secret scanning: [ci-baseline-github-actions.yml](./examples/ci-baseline-github-actions.yml)
  * CD progresivo (`staging` -> `production` con Environments, aprobación manual, OIDC y rollback): [cd-deploy-github-actions.yml](./examples/cd-deploy-github-actions.yml)
  * Releases SemVer automáticos con checksums: [release-semver-github-actions.yml](./examples/release-semver-github-actions.yml)
  * Validación de PRs (Conventional Commits + tamaño): [pr-validation-github-actions.yml](./examples/pr-validation-github-actions.yml)
  * Análisis SAST con CodeQL: [codeql-security-github-actions.yml](./examples/codeql-security-github-actions.yml)
* **Configuración de repositorio GitHub:** [dependabot.yml](./examples/dependabot.yml), [CODEOWNERS](./examples/CODEOWNERS), [gitignore-baseline.txt](./examples/gitignore-baseline.txt), [gitattributes-baseline.txt](./examples/gitattributes-baseline.txt) e Issue Forms ([issue-bug-report.yml](./examples/issue-bug-report.yml) y [issue-feature-request.yml](./examples/issue-feature-request.yml)).
* **Contenedores e IaC:** [Dockerfile](./examples/Dockerfile) y [docker-compose.yml](./examples/docker-compose.yml) (entorno reproducible) o esqueletos IaC.
* **Operación y FinOps:** **Runbook** operativo, matriz de alertas, límites duros de presupuesto en nube/APIs y definición de SLIs/SLOs/métricas DORA.

## Criterios de verificación
* Todo pipeline de producción incluye verificaciones de calidad/seguridad, acciones fijadas por commit SHA (con Dependabot activo), mínimo privilegio (`permissions: contents: read`), health check y mecanismo de rollback.
* Las configuraciones de contenedores e IaC separan claramente configuración por ambiente, nunca incrustan secretos y fijan límites máximos de auto-escalado y alertas/topes de costo en la nube.
* Se evita introducir complejidad operativa innecesaria (como Kubernetes o múltiples instancias sin techo) en proyectos Nivel 1 o sin justificación de escala real.
