# Software Engineering Agent Skills (`swe-*`)

Colección de **13 skills modulares e independientes** de buenas prácticas de ingeniería de software, calibradas para llevar proyectos desde **1. MVP**, pasando por **2. Profesional (miles de usuarios)** hasta **3. Empresarial**, con seguridad fuerte, flujo GitHub completo, cumplimiento legal base, flujo ordenado con agentes IA, pruebas en vivo y entrega formal (*handover*).

Escritas bajo el estándar abierto **Agent Skills (`SKILL.md`)**, compatibles con **Antigravity**, **Claude Code**, **OpenAI Codex**, **Cursor**, **OpenCode** y **Gemini CLI**.

---

## Skills incluidas (13)

| Skill | Área que cubre | Cuándo usarla |
| :--- | :--- | :--- |
| `swe-methodology` | Metodología base, selector de nivel (`1. MVP / 2. Profesional / 3. Empresarial`), perfiles por producto (`product-profiles.md`), integración con `modern-web-guidance`/`Context7` (`ecosystem-integrations.md`), documentación (`examples/`), checklist de auditoría (`audit-checklist.md`), diagnóstico rápido (`scripts/repo_audit_scan.py`) y normas ISO/OWASP/NIST | Al arrancar un proyecto, definir alcance/estándares, crear documentación o realizar auditorías rápidas/integrales |
| `swe-domain-discovery` | Descubrimiento independiente de brechas por industria y país (fintech/banca, salud, gobierno, videojuegos, e-commerce, menores, IoT): qué desarrollar en código vs. qué licencias/normas/auditorías externas faltan | Al plantear un proyecto de un sector específico y descubrir requisitos fuera de las buenas prácticas generales |
| `swe-browser-audit` | Auditoría dinámica en navegador real con Playwright (`scripts/playwright_security_audit.mjs`): consola, red, frontend, Security Headers, cookies, storage, sourcemaps, validación de campos, XSS, sondas seguras de SQLi/NoSQLi, IDOR/CSRF, `axe-core` y responsive | Para probar en vivo una app en `localhost` o `staging` autorizado buscando errores y vulnerabilidades |
| `swe-architecture-design` | Arquitectura, SOLID/DRY/KISS/YAGNI, Clean Architecture, DDD, patrones de resiliencia (Circuit Breaker/Bulkhead), portabilidad (sin Vendor Lock-in), calidad de código, linting y refactoring | Al diseñar arquitectura, crear ADRs o auditar estructura y calidad del código |
| `swe-security-privacy` | DevSecOps, SSDLC, Threat Modeling, OWASP Top 10/ASVS, autenticación/autorización, cifrado, privacidad (ARCO/LFPDPPP), licencias OSS/PI y cadena de suministro (SBOM/SCA) | Al diseñar flujos sensibles, revisar vulnerabilidades, gestionar secretos/dependencias/licencias o validar privacidad |
| `swe-qa-testing` | Estrategia de pruebas, pirámide de testing y 25 tipos de pruebas (Unit, Integration, E2E, Contract, Load, Security, Mutation, Fuzz, Chaos, LLM Evals, etc.) | Al definir estrategia QA, auditar suite de pruebas o escribir planes y casos de prueba |
| `swe-ux-accessibility` | UX/UI, Design Systems, diseño responsive (Mobile First), accesibilidad WCAG 2.2 AA / WAI-ARIA, RUM/analítica ética, compatibilidad e i18n/l10n | Al construir o auditar interfaces web/móviles, estados de UI, contraste, teclado y localización |
| `swe-data-apis` | Diseño de BD, normalización, concurrencia/DLQ, migraciones compatibles hacia atrás, RTO/RPO, backups probados, REST/OpenAPI, Problem Details (RFC 9457) y rendimiento | Al modelar bases de datos, diseñar o revisar APIs y resolver cuellos de botella o consultas N+1 |
| `swe-devops-operations` | Git (GitHub Flow / Trunk-Based / Git Flow, Conventional Commits, Rulesets/`gh CLI`), CI/CD endurecido por SHA (CI, CD con Environments/OIDC, Releases SemVer, CodeQL, Dependabot, validación PRs, `CODEOWNERS`, `.gitattributes`, Issue Forms), Docker/IaC/Kubernetes, incidentes/postmortem, observabilidad, DORA y FinOps | Al configurar repositorios GitHub, pipelines CI/CD, contenedores, despliegues, monitoreo y costos en nube |
| `swe-ai-engineering` | Seguridad y gobernanza de IA/LLMs en producto (NIST AI RMF, ISO 42001), prompt injection, alucinaciones, sesgos, Human-in-the-loop, versionado de prompts/modelos, evals y costos | Al diseñar, auditar o probar funciones de producto con LLMs, RAG, agentes o tool calling |
| `swe-project-handover` | Paquete integral de Software Project Handover y Documentación Viva (`PROJECT-HANDOVER/00-START-HERE` a `17-APPENDICES` + Regla 18): contexto ejecutivo, guía de código, memoria histórica/deuda, licencias/PI, manuales diferenciados, inventario, transferencia/revocación de accesos, sesiones supervisadas, acta de entrega y `scripts/handover_scaffold.py` | Al preparar la entrega formal de un proyecto, onboarding de sucesores o auditar completitud documental |
| `swe-legal-compliance` | Marco de Cumplimiento Legal y Regulatorio (LCS — 13 pilares + checklist `Legal Launch Readiness 0/36`): borradores base (Aviso de Privacidad integral/simplificado LFPDPPP, Términos y Condiciones, Cookies, PROFECO/LFPC arts. 76 Bis y 76 Bis 1), PI (INDAUTOR/IMPI, coautores), contratos B2B (EULA, SaaS, NDA, DPA, SLA), SAT/CFDI, evidencia NOM-151, controles técnico-legales y `scripts/legal_readiness_check.py` | Al generar borradores legales base, implementar controles técnico-legales (ARCO/consentimiento/log versionado) o evaluar preparación legal de lanzamiento |
| `swe-ai-workflow` | Context Engineering, ahorro radical de tokens y control de *vibe coding*: genera y audita `CONSTITUTION.md`, `AGENTS.md` (con puentes a `CLAUDE.md`/`GEMINI.md`/`.cursor/rules/`), `.ai/MEMORY.md`, `.ai/TASK_SPEC.md`, lectura selectiva, script antes que LLM, lotes pequeños verificados, regla de 2 intentos y `scripts/ai_context_kit.py` | Al configurar un repositorio para programar con agentes IA, reducir gasto de tokens o estructurar prompts vagos de *vibe coding* |

---

## Instalación

Puedes instalar **todas las 13 skills** o copiar únicamente las carpetas `swe-*` que necesites.

### Opción 1 — Instalación rápida con `skills` CLI (recomendado)

```bash
# Instalar todas las skills del repositorio (reemplaza <usuario>/<repo> por el repo publicado)
npx skills add <usuario>/swe-agent-skills

# O instalar solo una skill específica
npx skills add <usuario>/swe-agent-skills --skill swe-ai-workflow
```

### Opción 2 — Instalación por proyecto (`.agents/skills/`, estándar compartido)

Ideal para compartir las mismas skills con todo el equipo dentro del repositorio (compatible con Antigravity, Codex, OpenCode y herramientas compatibles con `.agents/skills/`):

**Linux / macOS (Bash):**
```bash
git clone --depth 1 https://github.com/<usuario>/swe-agent-skills.git /tmp/swe-agent-skills
mkdir -p .agents/skills
cp -r /tmp/swe-agent-skills/swe-* .agents/skills/
rm -rf /tmp/swe-agent-skills
```

**Windows (PowerShell):**
```powershell
git clone --depth 1 https://github.com/<usuario>/swe-agent-skills.git "$env:TEMP\swe-agent-skills"
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force "$env:TEMP\swe-agent-skills\swe-*" ".agents\skills\"
Remove-Item -Recurse -Force "$env:TEMP\swe-agent-skills"
```

### Opción 3 — Instalación global por herramienta

Copia las carpetas `swe-*` en la carpeta global de tu agente:

| Herramienta | Ruta global de skills | Ruta por proyecto |
| :--- | :--- | :--- |
| **Antigravity** | `~/.gemini/config/skills/` | `<proyecto>/.agents/skills/` |
| **Claude Code** | `~/.claude/skills/` | `<proyecto>/.claude/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `<proyecto>/.agents/skills/` |
| **Cursor** | `~/.cursor/skills/` | `<proyecto>/.cursor/skills/` o `.agents/skills/` |
| **OpenCode / Gemini CLI** | `~/.config/opencode/skills/` | `<proyecto>/.agents/skills/` |

### Verificación rápida tras instalar

1. Reinicia o abre una nueva sesión de tu agente y pregúntale: *"¿Qué skills `swe-*` tienes disponibles?"*.
2. (Opcional) Comprueba los scripts auxiliares (Python 3 estándar; Node.js + Playwright solo para `swe-browser-audit`):
   ```bash
   python3 .agents/skills/swe-methodology/scripts/repo_audit_scan.py .
   python3 .agents/skills/swe-ai-workflow/scripts/ai_context_kit.py audit .
   ```

---

## Principio de aplicación proporcional

No todas las prácticas aplican por igual a todos los proyectos. Todas las skills clasifican el proyecto en tres niveles antes de exigir controles:

1. **Nivel 1 — MVP sólido:** entrega rápida sin deuda tóxica y preparada para escalar (arquitectura clara, validación en servidor, secretos fuera del repo, tests críticos, HTTPS).
2. **Nivel 2 — Producción pequeña/mediana (miles de usuarios / SaaS / App en vivo):** CI/CD endurecido con linters y tests completos, resiliencia (timeouts/retries/idempotencia), backups con restauración probada, WCAG 2.2 AA, monitoreo de errores, alertas de costos en nube (FinOps) y auditorías periódicas.
3. **Nivel 3 — Empresarial / Regulado:** Threat Modeling formal, gobernanza (RACI/SRS/BPMN/DAMA-DMBOK), cumplimiento ISO/OWASP ASVS/NIST SSDF, SLSA/Sigstore, ITIL 4, Chaos/Load testing y observabilidad distribuida.

---

## Licencia

Distribuido bajo la licencia **Apache-2.0**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
