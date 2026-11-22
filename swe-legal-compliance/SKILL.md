---
name: swe-legal-compliance
description: >-
  Marco integral de cumplimiento legal y regulatorio para productos digitales
  (LCS — 13 pilares + checklist Legal Launch Readiness 0/36): genera borradores base
  (Aviso de Privacidad integral/simplificado LFPDPPP, Términos y Condiciones, Política
  de Cookies, cancelaciones/reembolsos PROFECO/LFPC arts. 76 Bis y 76 Bis 1), guía PI
  (INDAUTOR/IMPI, cesión entre coautores), contratos B2B/equipo (EULA, SaaS, NDA, DPA,
  SLA), obligaciones fiscales (SAT/CFDI/IVA), evidencia electrónica (NOM-151-SCFI-2016)
  y controles técnico-legales en software. Usar al preparar documentos legales base o
  validar preparación legal de lanzamiento (para regulación vertical de industrias
  específicas usar swe-domain-discovery; para seguridad de código usar
  swe-security-privacy).
---

# Cumplimiento Legal, Regulatorio y Preparación de Lanzamiento (LCS)

Aplica esta skill cuando necesites estructurar el paquete legal base de un producto digital, generar borradores iniciales listos para revisión jurídica, diseñar controles técnico-legales dentro del software o evaluar la preparación legal de lanzamiento (`0/36`).

## Reglas fundamentales
1. **Guía técnico-operativa, NO asesoría legal certificada:** todo borrador o checklist producido con esta skill es un punto de partida estructurado que **debe ser validado y ajustado por un abogado habilitado** (y un contador público en materia fiscal) antes de publicarse con usuarios o cobros reales. Incluye siempre esta advertencia en los borradores generados.
2. **Jurisdicción verificada y cero normas inventadas:** confirma siempre el país/jurisdicción principal (incluye marco detallado para **México** y adaptabilidad internacional para UE/GDPR, EE. UU./CCPA y LATAM). Cuando tengas búsqueda web disponible, verifica reformas vigentes (LFPDPPP vigente y autoridad garante federal, LFPC art. 76 Bis 1, reglas vigentes del SAT/CFDI) en lugar de citar normas desactualizadas de memoria.
3. **Cero secretos ni datos fiscales/personales reales en plantillas:** usa siempre marcadores explícitos (`[RAZÓN SOCIAL]`, `[RFC]`, `[DOMICILIO]`, `[CORREO ARCO]`) hasta que el responsable legal los complete en su canal autorizado.
4. **Nivel de rigor proporcional:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto:
   * **Nivel 1 — MVP (piloto / sin cobros masivos):** Aviso de Privacidad integral y simplificado, Términos y Condiciones básicos, Política de Cookies, acuerdo de coautores/titularidad y registro mínimo de aceptación.
   * **Nivel 2 — Profesional (SaaS / E-commerce / Producción):** los 13 pilares operativos (PROFECO/LFPC 76 Bis y 76 Bis 1, cancelaciones/reembolsos, controles ARCO y exportación/eliminación en app, registro de marca IMPI / obra INDAUTOR, CFDI/SAT, contratos B2B según modelo y log versionado con hash).
   * **Nivel 3 — Empresarial / Regulado:** cumplimiento formal 36/36 con auditoría legal externa, DPA/SLA/MSA negociables, conservación probatoria NOM-151-SCFI-2016, gobernanza multi-jurisdicción (GDPR/CCPA) y coordinación obligatoria con `swe-domain-discovery`.

## Flujo de trabajo

### Modo A — Generar el paquete de borradores legales (`LEGAL-DOCS/`)
1. **Capturar contexto mínimo:** país/jurisdicción, tipo de titular (persona física, moral o equipo de coautores), modelo de negocio (gratuito, SaaS, suscripción con renovación automática, e-commerce, B2B/B2C), tipos de datos recolectados (PII, sensibles, menores, pagos) y nivel (`1/2/3`).
2. **Consultar los 13 pilares:** revisa [legal-compliance-framework-13.md](./references/legal-compliance-framework-13.md) para identificar qué documentos, trámites y contratos aplican al proyecto.
3. **Crear el andamiaje con el script (opcional y seguro):** usa [legal_readiness_check.py](./scripts/legal_readiness_check.py) desde la ruta resuelta de esta skill (previsualiza primero con `--dry-run`):
   ```bash
   # Previsualizar qué documentos se crearán (sin escribir en disco)
   python3 <ruta-de-la-skill>/scripts/legal_readiness_check.py init <ruta-del-repo>/LEGAL-DOCS --level 2 --dry-run

   # Generar borradores base y checklist 0/36 sin sobrescribir archivos existentes
   python3 <ruta-de-la-skill>/scripts/legal_readiness_check.py init <ruta-del-repo>/LEGAL-DOCS --level 2 --project-name "MiProducto"
   ```
   *(En Windows usa `python` en lugar de `python3`.)*
4. **Personalizar borradores desde las plantillas base:**
   * Aviso de Privacidad Integral y Simplificado -> [AVISO_DE_PRIVACIDAD_INTEGRAL.md](./examples/AVISO_DE_PRIVACIDAD_INTEGRAL.md)
   * Términos y Condiciones (incluye uso aceptable, precios, renovaciones/cancelaciones LFPC 76 Bis 1 y reembolsos) -> [TERMINOS_Y_CONDICIONES.md](./examples/TERMINOS_Y_CONDICIONES.md)
   * Política de Cookies y consentimiento granular -> [POLITICA_DE_COOKIES.md](./examples/POLITICA_DE_COOKIES.md)
   * Acuerdo de colaboración/cesión entre coautores y guía de contratos B2B (EULA, SaaS, NDA, DPA, SLA) -> [COAUTHOR_IP_ASSIGNMENT_OUTLINE.md](./examples/COAUTHOR_IP_ASSIGNMENT_OUTLINE.md)
   * Esquema técnico de log de aceptación versionado (compatible con evidencia NOM-151) -> [ACCEPTANCE_AUDIT_LOG_SCHEMA.json](./examples/ACCEPTANCE_AUDIT_LOG_SCHEMA.json)

### Modo B — Implementar controles técnico-legales dentro del software (Punto 10 y 11)
Consulta [tech-legal-controls-in-software.md](./references/tech-legal-controls-in-software.md) para traducir obligaciones legales a requisitos implementables en código:
1. **Consentimiento granular en UI y preservación de formularios:** sin casillas premarcadas, separación entre finalidades primarias/secundarias, cookies no esenciales bloqueadas antes del consentimiento y **enlaces legales dentro de formularios abriendo siempre en nueva pestaña (`target="_blank" rel="noopener noreferrer"`) o modal** para no perder el progreso del usuario.
2. **Paridad `LEGAL-DOCS/` ↔ UI pública:** las páginas públicas (`/privacidad`, `/terminos`, `/cookies`) deben publicar el contenido íntegro y estructurado (responsable, tabla de datos y finalidades, transferencias/terceros, tabla exacta de cookies y procedimiento/plazos ARCO), **nunca resúmenes improvisados de 2–4 líneas**.
3. **Evidencia electrónica de aceptación:** persistir versión exacta del documento, hash `SHA-256` del texto aceptado, timestamp UTC, canal y trazabilidad (ver [ACCEPTANCE_AUDIT_LOG_SCHEMA.json](./examples/ACCEPTANCE_AUDIT_LOG_SCHEMA.json)); integrar constancia de conservación **NOM-151-SCFI-2016** cuando el modelo exija valor probatorio reforzado.
4. **Centro de Privacidad y derechos ARCO:** flujo de solicitud ARCO con acuse y seguimiento de plazos, exportación portable de datos y eliminación/anonimización de cuenta respetando retenciones legales obligatorias.
5. **Control de edad y renovaciones transparentes:** filtro de edad / consentimiento parental verificable cuando aplique y botón/flujo claro de cancelación de suscripciones sin fricción abusiva.

### Modo C — Auditar preparación legal de lanzamiento (`Legal Launch Readiness 0/36`)
1. Ejecuta el diagnóstico de solo lectura con [legal_readiness_check.py](./scripts/legal_readiness_check.py):
   ```bash
   python3 <ruta-de-la-skill>/scripts/legal_readiness_check.py audit <ruta-del-repo>/LEGAL-DOCS --level 2
   ```
   *(Agrega `--format json` para salida estructurada. Códigos de salida: `0` sin bloqueadores de seguridad, `1` error de argumentos, `2` **bloqueador crítico**: archivo `.env` o secreto detectado en `LEGAL-DOCS/`).*
2. Evalúa sistemáticamente los 36 criterios de [legal-launch-readiness-36.md](./references/legal-launch-readiness-36.md) y calcula el puntaje real `X/36` separando lo que se resuelve en **documentos/código** de lo que requiere **trámite externo o revisión de abogado/contador**.
3. Si el producto pertenece a un sector altamente regulado (fintech, salud, gobierno, videojuegos, menores), complementa obligatoriamente con `swe-domain-discovery`.

## Criterios de verificación
* Todo borrador generado incluye advertencia explícita de que requiere validación de abogado habilitado (y contador público en temas fiscales) antes de entrar en vigor.
* Se distinguen claramente documentos redactables, controles técnico-legales en software y trámites/registros externos (INDAUTOR, IMPI, SAT, NOM-151).
* El puntaje `Legal Launch Readiness (X/36)` refleja evidencia verificada (sin marcar ítems completados con placeholders pendientes) y `legal_readiness_check.py audit` reporta **0 secretos ni archivos `.env`**.
