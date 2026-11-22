---
name: swe-domain-discovery
description: >-
  Analiza la descripción de un proyecto (fintech, banco, salud, gobierno, videojuegos,
  e-commerce, IoT, EdTech, etc.) para investigar requisitos regulatorios, estándares
  de industria y brechas técnicas que las skills generales no cubren según país y
  etapa, generando un plan de qué desarrollar en código y qué validar externamente.
  Usar al plantear un proyecto de un sector regulado o negocio específico.
---

# Descubrimiento de Dominio, Regulación y Brechas

Usa esta skill de forma independiente cuando el usuario describa el tipo de negocio o industria de su proyecto y necesite descubrir **todo lo que falta más allá de las buenas prácticas generales de software**.

## Regla fundamental
**No asumas jurisdicción ni inventes normativas:** los requisitos legales, financieros, sanitarios o de industria dependen del país y cambian con el tiempo. Verifica en fuentes oficiales cuando tengas acceso a búsqueda web y aclara que el análisis es técnico-informativo (no sustituye asesoría legal oficial).

## Flujo de trabajo

### 1. Capturar el contexto mínimo del proyecto
Extrae de la descripción del usuario (o pregunta brevemente si falta):
1. **Sector / modelo de negocio:** fintech/banca, salud, gobierno, videojuegos, e-commerce, educación/menores, IoT, etc.
2. **País o jurisdicción de operación:** determina qué leyes y reguladores aplican.
3. **Nivel objetivo del proyecto (preguntar si no lo indicó):**
   * **1. MVP:** prototipo o primera versión controlada (sin dinero ni datos reales de usuarios en sectores regulados).
   * **2. Profesional:** producción real pequeña/mediana (miles de usuarios).
   * **3. Empresarial:** escala corporativa, cumplimiento estricto y auditorías formales.
   *(Si el sector es regulado —fintech, salud, gobierno— y el usuario elige `1. MVP`, diseña una ruta segura de pruebas/simulación y marca los bloqueadores legales obligatorios antes de pasar a Nivel 2/3 con usuarios reales).*
4. **Activos sensibles involucrados:** pagos/dinero, datos biométricos/clínicos, menores de edad, firma oficial, economía virtual, hardware físico.

### 2. Identificar brechas frente al estándar base
1. Toma como base cubierta las prácticas generales de ingeniería (arquitectura, OWASP, ACID, pruebas, CI/CD, WCAG 2.2 AA).
2. Consulta el mapa inicial de sectores en [domain-catalog.md](./references/domain-catalog.md) para identificar qué piezas técnicas y regulatorias específicas suele necesitar ese giro.
3. Si tu entorno tiene búsqueda web disponible, **investiga en fuentes oficiales vigentes** del país/sector:
   * Reguladores y leyes aplicables (licencias, permisos, retención obligatoria de datos, residencia de datos).
   * Estándares técnicos obligatorios o de facto del sector (ej. PCI-DSS, HL7/FHIR, normas de firma electrónica, políticas de App Store / Play Store / Steam / consolas).
   * Opciones de arquitectura que reducen carga regulatoria (ej. usar BaaS o pasarelas reguladas en lugar de custodiar fondos o tarjetas directamente).
   Si no tienes acceso a internet, indícalo explícitamente y señala qué puntos exactos debe confirmar el usuario.

### 3. Producir el Plan de Desarrollo y Cumplimiento
Entrega la respuesta estructurada en tres bloques claros:

1. **Qué SÍ debe diseñarse y construirse en el software (Desarrollo técnico):**
   * Modelos de datos y reglas críticas del dominio (ej. *double-entry ledger* y conciliación en fintech; historial clínico inmutable en salud; servidor autoritativo anti-cheat en videojuegos).
   * Controles de seguridad y privacidad adicionales al estándar base.
   * Integraciones externas recomendadas para reducir riesgo legal/técnico.
   * Pruebas especializadas del dominio (carga, concurrencia financiera, interoperabilidad, compatibilidad).
2. **Qué NO se resuelve solo con código (Gestión legal, licencias y auditorías):**
   * Licencias o registros ante autoridades, certificaciones, avisos legales, pólizas y pruebas de penetración / auditorías independientes obligatorias.
3. **Ruta MVP vs. Producción Real:**
   * Qué puedes construir hoy de forma segura en un MVP controlado y qué bloqueadores debes resolver **antes** de recibir usuarios, pacientes o dinero real.

### 4. Artefacto opcional para el proyecto
Si el usuario va a iniciar el desarrollo en el repositorio, ofrece generar `docs/domain-requirements.md` con los requisitos específicos descubiertos para que sirva como referencia durante toda la construcción.

## Criterios de verificación
* Se distingue claramente entre lo técnico construible en código y los trámites/certificaciones externas.
* Todo estándar o ley citada corresponde al país indicado (o se marca como pendiente de verificación si falta país o acceso web).
* Incluye advertencia clara de que el resultado es guía técnica e informativa y no reemplaza asesoría legal o regulatoria certificada.
