---
name: swe-ai-engineering
description: >-
  Guía profesional para aplicaciones con IA/LLMs y desarrollo asistido por agentes:
  seguridad contra prompt injection y fuga de PII, control de alucinaciones y sesgos,
  salidas estructuradas, versionado de prompts/modelos, evaluaciones de regresión
  (evals), Human-in-the-loop, costos por inferencia y gobernanza (NIST AI RMF,
  ISO/IEC 42001, ISO/IEC 23894). Usar al diseñar, auditar o probar funciones con
  LLMs, RAG o agentes en producto (para configurar el flujo de desarrollo con agentes
  IA, ahorrar tokens y controlar vibe coding usar swe-ai-workflow).
---

# Ingeniería, Seguridad y Gobernanza de IA

Aplica esta skill cuando un proyecto integre modelos de lenguaje (LLMs), RAG, agentes con herramientas (*tool calling*) o pipelines de inferencia.

## Regla fundamental
**Salida probabilística bajo control determinista:** nunca confíes ciegamente en la respuesta de un modelo ni le des permisos directos sin validación de esquema, autorización del usuario real y límites de costo/riesgo.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto antes de exigir marcos formales de Nivel 3 (ISO/IEC 42001, inventario formal de riesgos).

## Flujo de trabajo

### 1. Planificar o diseñar funciones con IA
1. **Riesgo y supervisión (*Human-in-the-loop*):** clasifica qué acciones puede sugerir la IA y cuáles exigen confirmación humana explícita (pagos, borrados, cambios de permisos, decisiones legales/médicas).
2. **Arquitectura de prompts y contratos:** separa instrucciones de sistema de datos de usuario/RAG; exige salidas estructuradas (JSON Schema) cuando alimenten código o UI; versiona prompts y modelos explícitamente.
3. **Costos, control de bucles y resiliencia:** define límites de tokens de entrada/salida, **máximo de iteraciones por tarea**, **detección de llamadas recursivas**, bloqueo contra **ejecuciones concurrentes duplicadas**, cuotas/presupuestos por usuario/plan y presupuesto global (distinguiendo alertas vs. **topes estrictos de gasto** en el proveedor), caché cuando aplique, timeouts, retries acotados con **backoff exponencial + *jitter*** y fallback a otro modelo o degradación elegante.
4. **Privacidad:** evita enviar PII o secretos a proveedores externos sin anonimización/minimización y sin verificar políticas de no-entrenamiento/retención.

Consulta todas las prácticas y referencias (NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894) en [ai-governance-and-safety.md](./references/ai-governance-and-safety.md).

### 2. Auditar proyectos con IA / LLMs
Verifica sistemáticamente:
1. **Prompt Injection y Tool Calling:** ¿se inyectan documentos/web/inputs sin aislar? ¿Puede el modelo invocar herramientas con privilegios superiores al usuario actual?
2. **Validación de salidas:** ¿se renderiza Markdown/HTML del modelo sin sanitizar (riesgo XSS) o se ejecuta SQL/código generado sin validación estricta?
3. **Alucinaciones, sesgos y trazabilidad:** ¿hay citas/verificación contra fuentes reales en RAG? ¿Se registran versión de prompt/modelo y decisiones automatizadas sin guardar PII en logs?
4. **Control financiero y anti-bucles:** ¿existen límites de tokens, máximo de iteraciones por tarea, corte de llamadas recursivas, bloqueo de concurrencia duplicada, cuotas por usuario/global y topes duros de gasto en el proveedor para evitar facturas descontroladas?

### 3. Generar artefactos y evaluaciones (Evals)
Genera cuando se soliciten:
* Suite base de **Evals** (casos normales, bordes, formato JSON y casos adversarios de *prompt injection* para detectar regresiones al cambiar de modelo o prompt).
* Política de uso y protección de datos en IA / matriz de riesgos del proveedor.
* Contratos de salida estructurada y configuración de límites/fallbacks.

## Criterios de verificación
* Ninguna herramienta de agente confía en el prompt para validar autorización; la autorización vive siempre en el backend.
* Todo cambio de prompt o versión de modelo cuenta con casos de evaluación reproducibles.
* Los costos por inferencia están acotados con límites técnicos de tokens y tasa de peticiones.
