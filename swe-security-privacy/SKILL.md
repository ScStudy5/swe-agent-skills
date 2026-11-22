---
name: swe-security-privacy
description: >-
  Guía profesional de seguridad (DevSecOps, SSDLC, Threat Modeling, OWASP Top 10/ASVS,
  NIST SSDF, ISO 27001), privacidad y protección de datos (Privacy by Design, ARCO,
  LFPDPPP, ISO 27701) y cadena de suministro (SCA, SBOM, lockfiles, CVEs). Usar al
  diseñar autenticación/autorización, auditar código/privacidad o revisar dependencias
  (para auditoría en vivo con Playwright usar swe-browser-audit; para gobernanza
  integral de LLMs/agentes usar swe-ai-engineering; para borradores legales y
  checklist Legal Launch Readiness 0/36 usar swe-legal-compliance).
---

# Seguridad, DevSecOps, Privacidad y Cadena de Suministro

Aplica esta skill cuando diseñes flujos críticos, implementes autenticación/autorización, manipules datos personales, revises dependencias o audites seguridad.

## Regla fundamental
**Security & Privacy by Design:** la seguridad y la privacidad no se agregan al final; forman parte de todo el ciclo de vida del desarrollo (**SSDLC**).

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de exigir controles formales de Nivel 3 (ASVS completo, SLSA, ISO 27001).

## Flujo de trabajo

### 1. Planificar o diseñar controles (Proyecto o funcionalidad nueva)
1. **Modelado de amenazas (*Threat Modeling*):** identifica activos sensibles, superficies de exposición (APIs, UI, almacenamiento, integraciones), vectores de ataque y controles antes de codificar.
2. **Control de acceso e identidad:** aplica **Least Privilege**, **Zero Trust**, **RBAC** (o **ABAC** si requiere contexto granular), **MFA** cuando corresponda, protocolos estándar (**OAuth 2.0 / OpenID Connect**) y gestión segura de sesiones/tokens/cookies.
3. **Privacidad desde el diseño:** aplica minimización de datos, **Privacy by Default**, consentimiento informado, retención/eliminación y derechos **ARCO** (considerando la **LFPDPPP** en México u otra normativa aplicable).
4. Consulta todas las prácticas y normas en [security-privacy-supply-chain.md](./references/security-privacy-supply-chain.md).

### 2. Auditar seguridad, privacidad y dependencias
Revisa el proyecto sistemáticamente en 5 capas:
1. **Secretos, bundle cliente y configuración:** verifica que no existan contraseñas, API keys privadas (`service_role`, tokens), certificados ni **claves/datos internos de negocio** (p. ej. respuestas correctas o reglas reservadas desde paquetes `shared`) expuestos en el repositorio, el **bundle JS del frontend**, la **consola del navegador** (`drop: ['console', 'debugger']` en build de producción) ni los logs; revisa `.gitignore`, variables de entorno separadas por ambiente, **TLS/HTTPS con redirección HTTP -> HTTPS**, **sin modo depuración (`DEBUG=false`) ni endpoints/usuarios de prueba en producción**, **sin archivos/buckets expuestos** (`.git`, `.sql`, `.env`, `.map` públicos, storage abierto), **Security Headers**, **CORS restringido**, **Rate Limiting** y cifrado en reposo.
2. **Código, cuentas, BD (RLS) y reglas críticas:** busca fallos de **OWASP Top 10 / API Security Top 10** (validación de entradas en servidor, **cálculo de precios/totales/permisos siempre en servidor**, codificación de salidas contra XSS, consultas parametrizadas, protección **IDOR/BOLA** verificando propietario del recurso en cada endpoint, rutas `/admin` con **MFA** y **Audit Logs**). Verifica higiene de cuentas/sesiones (**anti-enumeración de correos**, verificación de email, recuperación segura, **invalidación al cerrar sesión** y **revocación de sesiones comprometidas**) y, en BDs expuestas por API (p. ej. Supabase/PostgreSQL), **RLS activado y probado** con políticas `SELECT`/`INSERT`/`UPDATE`/`DELETE` más permisos de vistas, funciones y buckets de Storage.
3. **Privacidad y datos personales:** detecta PII en logs, falta de enmascaramiento (*data masking*) en ambientes no productivos, retención indefinida o datos reales usados en pruebas.
4. **Integraciones con IA / LLMs (si aplica):** verifica protección contra *prompt injection*, validación/sanitización de salidas, mínimo privilegio en herramientas de agentes y que no se envíe PII o secretos a APIs externas sin consentimiento ni política de no-entrenamiento.
5. **Cadena de suministro y anti-*Vibe Coding*:** verifica lockfiles, versiones fijadas, dependencias reales (sin paquetes inventados o inutilizados) y actualizadas (**SCA**), licencias de terceros, imágenes base de contenedores, **SBOM** y revisión consciente del `git diff` antes de subir código generado por IA.

### 3. Generar artefactos de seguridad y cumplimiento
Genera cuando se soliciten:
* Matriz de amenazas (*Threat Model*) y controles mitigantes.
* Política `SECURITY.md` y procedimiento de respuesta ante vulnerabilidades críticas.
* Checklist de revisión basado en **OWASP ASVS 5.0** / **NIST SSDF** adaptado al nivel del proyecto.
* Reglas/pasos de CI para **SAST** (CodeQL, Semgrep, SonarQube), **Secret Scanning** (Gitleaks), **Container Scanning** (Trivy) y **SBOM**.

## Criterios de verificación
* Ningún secreto real ni dato personal real aparece en código, ejemplos, logs o pruebas.
* Cada vulnerabilidad o brecha reportada incluye severidad (`Crítica/Alta/Media/Baja`; equivalencia ejecutiva en `swe-methodology`: `Crítica` -> Crítico; `Alta`/`Media` -> Importante; `Baja` -> Recomendado), ubicación, impacto y remediación concreta.
* Las recomendaciones distinguen entre requisitos de seguridad/cumplimiento y mejoras recomendadas.
