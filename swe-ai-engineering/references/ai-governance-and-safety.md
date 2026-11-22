# Ingeniería, Seguridad y Gobernanza de IA

## 1. Seguridad y protección de datos en IA
* **Protección contra Prompt Injection (directa e indirecta):** separar claramente instrucciones del sistema de entradas de usuario y contenido recuperado (RAG, web, correos, archivos).
* **Validación de resultados generados por IA:** tratar toda salida del modelo como entrada no confiable; validar esquemas (JSON Schema), sanitizar HTML/Markdown antes de renderizar (XSS) y nunca ejecutar SQL o comandos sin parametrización/validación.
* **Mínimo privilegio en herramientas (*Tool Calling*):** restringir herramientas expuestas al modelo; validar permisos del usuario real en backend, no en el prompt.
* **Protección contra fuga de información:** evitar que el modelo filtre prompts internos, secretos o datos de otros tenants en sistemas multi-usuario.
* **Protección de datos enviados a modelos externos:** no enviar PII, credenciales ni código confidencial sin minimización/anonimización, consentimiento y revisión de retención/no-entrenamiento del proveedor.

## 2. Calidad, fiabilidad y supervisión
* **Gestión de alucinaciones:** usar *grounding* (RAG con citas verificables), permitir al modelo responder *"no tengo evidencia suficiente"* y validar datos críticos contra fuentes deterministas.
* **Evaluación de sesgos:** revisar resultados en distintos grupos/contextos cuando el sistema afecte personas o decisiones sensibles.
* **Evaluación de modelos y regresiones:** mantener conjuntos de pruebas (*evals*) para comparar precisión, formato y seguridad antes de cambiar de prompt o versión de modelo.
* **Versionado de prompts y modelos:** fijar identificadores explícitos de modelo y versionar prompts en Git (evitar alias flotantes sin control en producción).
* **Human-in-the-loop:** exigir confirmación humana para acciones irreversibles, financieras, de seguridad o de alto impacto.
* **Trazabilidad de decisiones automatizadas:** registrar qué modelo, versión de prompt y entrada originaron una decisión relevante (enmascarando PII en logs).

## 3. Costos, resiliencia, control de bucles y gobernanza
* **Control de costos y límites estrictos:** establecer **presupuesto por usuario / plan de suscripción** y **presupuesto global**, configurar **límites duros de gasto (*hard spending limits*)** en el proveedor (recordando que las alertas de gasto no rechazan solicitudes nuevas por sí solas) y registrar tokens, llamadas, costos y errores (sin PII) con alertas ante picos anómalos.
* **Límites de tokens y llamadas:** establecer límites estrictos de tokens de entrada y salida (`max_tokens`), cuotas por plan y **máximo de llamadas por usuario/tenant** (rate limiting).
* **Protección contra bucles en agentes y *tool calling*:**
  * Fijar un **máximo de iteraciones por tarea** (`max_iterations` / `max_steps`).
  * Implementar **detección y corte de llamadas recursivas** (ej. agente -> herramienta -> función -> agente).
  * Evitar que dos procesos ejecuten simultáneamente la misma tarea (**bloqueo / deduplicación / idempotencia** por tarea).
  * No permitir jamás que la IA acceda libremente a **operaciones administrativas** sin validación estricta en backend y confirmación humana.
* **Resiliencia controlada:** configurar **timeouts** estrictos, evitar **reintentos infinitos**, usar **backoff exponencial con *jitter*** solo en errores transitorios y prever fallback de modelo o degradación elegante.
* **Evaluación de proveedores de IA:** documentar APIs/proveedores, revisar latencia, SLA, cumplimiento legal, privacidad y portabilidad (evitar acoplar toda la lógica a un único SDK propietario).
* **AI Governance, Transparencia Pública y AI Risk Management:** definir responsables, inventario de usos de IA, revisión periódica de riesgos y, cuando el producto exponga funciones con IA a usuarios finales, publicar una **Política de Transparencia y Uso de IA (`/politica-ia`)** explicando qué funciones usan IA, qué datos se envían (y cuáles NO), política de no-entrenamiento, limitaciones/errores posibles, supervisión humana y canal para reportar respuestas incorrectas (ver `swe-legal-compliance/references/public-trust-and-legal-pages.md`).

## 4. Desarrollo asistido por IA (Agentes / Copilots)
* Todo código generado por IA debe pasar las mismas reglas de **arquitectura, linting, pruebas automatizadas, SAST/secret scanning y Code Review** que el código humano.
* Prohibido pegar secretos reales o dumps de producción en prompts de desarrollo.

## Referencias internacionales
* **NIST AI RMF** (*Artificial Intelligence Risk Management Framework*)
* **ISO/IEC 42001** (Sistema de gestión de inteligencia artificial)
* **ISO/IEC 23894** (Gestión de riesgos en inteligencia artificial)
* **OWASP Top 10 for LLM Applications**
