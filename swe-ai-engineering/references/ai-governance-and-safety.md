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

## 3. Costos, resiliencia y gobernanza
* **Control de costos por inferencia:** monitorear gasto por función/usuario/tenant y alertar picos anómalos.
* **Límites de tokens y solicitudes:** establecer `max_tokens`, límites de contexto de entrada y rate limiting por usuario.
* **Resiliencia:** timeouts adecuados, retries con backoff en errores transitorios y fallback de modelo o degradación elegante.
* **Evaluación de proveedores de IA:** revisar latencia, SLA, cumplimiento legal, privacidad y portabilidad (evitar acoplar toda la lógica a un único SDK propietario).
* **AI Governance y AI Risk Management:** definir responsables, inventario de usos de IA y revisión periódica de riesgos según el nivel del proyecto.

## 4. Desarrollo asistido por IA (Agentes / Copilots)
* Todo código generado por IA debe pasar las mismas reglas de **arquitectura, linting, pruebas automatizadas, SAST/secret scanning y Code Review** que el código humano.
* Prohibido pegar secretos reales o dumps de producción en prompts de desarrollo.

## Referencias internacionales
* **NIST AI RMF** (*Artificial Intelligence Risk Management Framework*)
* **ISO/IEC 42001** (Sistema de gestión de inteligencia artificial)
* **ISO/IEC 23894** (Gestión de riesgos en inteligencia artificial)
* **OWASP Top 10 for LLM Applications**
