# Estándares Internacionales, Matriz de Rigor y Herramientas

## 1. Matriz de aplicación proporcional por nivel

| Área | Nivel 1 (MVP / Pequeño) | Nivel 2 (Producto / SaaS) | Nivel 3 (Empresarial / Regulado) |
| :--- | :--- | :--- | :--- |
| **Arquitectura** | Capas claras, KISS/YAGNI, bajo acoplamiento | Modularidad, API First, ADRs clave | Clean Arch / DDD según dominio, ADRs formales, ISO 42010 |
| **Seguridad** | HTTPS, validación servidor, hash contraseñas, 0 secretos en Git | OWASP Top 10, RBAC, Rate Limit, SCA/Secret Scan en CI | SSDLC completo, Threat Modeling, Zero Trust, MFA, OWASP ASVS, NIST SSDF |
| **Pruebas** | Unit en lógica crítica + smoke manual/básico | Unit + Integration + E2E flujos críticos en CI | Pirámide completa + Contract, Load/Stress, Security, A11y |
| **UX / A11y** | Responsive Mobile First, estados loading/error | Design System, WCAG 2.2 AA en flujos clave | WCAG 2.2 AA auditado, i18n/l10n, usabilidad formal |
| **Datos / APIs** | Migraciones versionadas, backups automáticos, HTTP codes | OpenAPI, RFC 9457, índices revisados, restore test | Encriptación en reposo, masking, audit trail, DRP |
| **DevOps / Ops** | Git con PRs, linter en CI, logs básicos | CI/CD por ambientes, Docker, APM/errores (Sentry) | IaC, scanning contenedores/IaC, Blue-Green/Canary, métricas DORA |

---

## 2. Estándares y normas internacionales de referencia

> ISO/IEC 25010:2023 define nueve características de calidad del producto (incluyendo seguridad, fiabilidad, mantenibilidad, capacidad de interacción, eficiencia de desempeño y flexibilidad), muy útiles para redactar requisitos no funcionales.

| Norma / Estándar | Aplicación principal | Referencia oficial |
| :--- | :--- | :--- |
| **ISO/IEC 25010:2023** | Modelo de calidad del producto software | https://www.iso.org/standard/78176.html |
| **ISO/IEC/IEEE 12207** | Procesos del ciclo de vida del software | https://www.iso.org/standard/63712.html |
| **ISO/IEC/IEEE 42010:2022** | Descripción de arquitectura de sistemas y software | https://www.iso.org/standard/74393.html |
| **ISO/IEC 27001:2022** | Sistema de gestión de seguridad de la información (SGSI) | https://www.iso.org/standard/27001 |
| **ISO/IEC 27002:2022** | Controles de seguridad de la información | — |
| **ISO/IEC 27005** | Gestión de riesgos de seguridad | — |
| **ISO/IEC 27034** | Seguridad de aplicaciones | — |
| **ISO/IEC 27701** | Gestión de información de privacidad (extensión de 27001) | — |
| **ISO/IEC 29100** | Marco de privacidad | — |
| **ISO/IEC/IEEE 29119** | Estándar de pruebas de software | — |
| **ISO 9001** | Gestión de calidad organizacional | — |
| **ISO/IEC 20000-1** | Gestión de servicios de TI | — |
| **ISO 22301** | Continuidad del negocio | — |
| **ISO 31000** | Gestión de riesgos | — |
| **ISO/IEC 38500** | Gobierno corporativo de TI | — |
| **ISO/IEC 40500** | WCAG 2.0 adoptado como estándar ISO | — |
| **ISO 9241-210 / 9241-110** | Diseño centrado en las personas y principios de interacción | — |
| **ISO/IEC 15288** | Procesos del ciclo de vida de sistemas | — |
| **IEEE 1016** | Descripción del diseño de software | — |
| **WCAG 2.2 / WAI-ARIA** | Accesibilidad web | https://www.w3.org/TR/wcag/ |
| **OWASP ASVS 5.0** | Verificación de seguridad de aplicaciones | https://asvs.owasp.org/ |
| **NIST SSDF (SP 800-218)** | Marco de desarrollo seguro de software | https://csrc.nist.gov/pubs/sp/800/218/final |
| **NIST AI RMF / ISO 42001 / ISO 23894** | Gobernanza y gestión de riesgos en inteligencia artificial | — |
| **ISO/IEC 19941** | Interoperabilidad y portabilidad en cloud computing | — |
| **ISO 8000 / ISO 11179 / DAMA-DMBOK** | Calidad, metadatos y gobierno de datos (Nivel 3 / Data) | — |
| **SLSA Framework / Sigstore** | Integridad de builds, provenance y firma de artefactos | — |
| **FinOps Framework** | Gestión financiera y optimización de costos en la nube | — |
| **Green Software / SCI** | Ingeniería sostenible y eficiencia energética | — |
| **ITIL 4** | Gestión de incidentes, problemas y operación de servicios | — |
| **CIS Controls** | Controles críticos de ciberseguridad | — |

---

## 3. Catálogo consolidado de herramientas profesionales recomendadas

No es necesario usar todas las herramientas, sino cubrir las áreas relevantes para el proyecto:

| Categoría | Herramientas recomendadas |
| :--- | :--- |
| **Control de versiones** | Git, GitHub |
| **CI/CD** | GitHub Actions, Azure DevOps |
| **Calidad de código** | SonarQube, SonarCloud, ESLint, Prettier, EditorConfig, Roslyn Analyzers, StyleCop |
| **Análisis de seguridad (SAST)** | SonarQube, CodeQL, Semgrep |
| **DAST** | OWASP ZAP |
| **Dependencias (SCA) y Licencias** | Dependabot, Renovate, FOSSA, ORT, ScanCode Toolkit |
| **Secret Scanning** | Gitleaks, GitHub Secret Protection |
| **Pruebas unitarias** | xUnit, NUnit, Jest, Vitest |
| **Pruebas E2E** | Playwright, Cypress |
| **API Testing** | Postman, Bruno |
| **Performance Testing** | k6, JMeter |
| **Accesibilidad** | axe-core, Lighthouse |
| **Contenedores y escaneo** | Docker, Trivy |
| **Infraestructura como Código (IaC)** | Terraform, OpenTofu |
| **Monitoreo y errores** | Prometheus, Grafana, Sentry |
| **Documentación API** | Swagger / OpenAPI |
| **Diagramas** | Draw.io, PlantUML |
| **Gestión de proyectos** | GitHub Projects, Jira |
