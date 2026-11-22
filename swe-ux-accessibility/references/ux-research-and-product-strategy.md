# Estrategia UX, Investigación con Usuarios y Usabilidad

Aplica esta guía antes de diseñar flujos o pantallas para asegurar que el producto resuelva la tarea real del usuario sin fricciones innecesarias. *(Para exploración de dirección visual, tipografía, composición, movimiento y crítica estética usa `swe-ui-craft`.)*

---

## 1. Investigación con usuarios (proporcional al nivel del proyecto)
* **Jobs-to-be-Done (JTBD) y contexto:** define qué tarea concreta intenta resolver el usuario, en qué dispositivo/entorno (móvil con una mano, oficina, prisa) y cuál es la señal de éxito en menos de 10 segundos.
* **Nivel 1 (MVP):** 3–5 conversaciones rápidas o pruebas de prototipo con usuarios del perfil objetivo para detectar confusiones críticas antes de programar.
* **Nivel 2 (Profesional):** mapas de flujo (*User Flows / Journeys*), arquitectura de información clara (máximo 5–7 opciones en navegación primaria), pruebas de usabilidad moderadas con 5 usuarios sobre tareas clave y analítica ética/RUM para detectar puntos de abandono.
* **Nivel 3 (Empresarial):** investigación continua multi-rol, validación formal bajo **ISO 9241-210** y pruebas de usabilidad/accesibilidad con usuarios reales de lectores de pantalla y tecnologías de asistencia.

---

## 2. 10 Heurísticas de Usabilidad (Nielsen) como filtro operativo
1. **Visibilidad del estado del sistema:** el usuario siempre sabe si está cargando, guardando o hubo error.
2. **Lenguaje del mundo real:** usa términos comprensibles para el usuario, nunca códigos internos de BD o jerga técnica.
3. **Control y libertad:** deshacer, cancelar y volver atrás sin trampas.
4. **Consistencia y estándares:** acciones iguales se ven y comportan igual en toda la app.
5. **Prevención de errores:** evita el error antes de mostrar un mensaje (validación en línea, confirmaciones explícitas para borrados irreversibles).
6. **Reconocimiento antes que recuerdo:** opciones y ayuda visibles en el momento de decidir.
7. **Flexibilidad y eficiencia:** atajos de teclado y flujos rápidos para usuarios frecuentes.
8. **Claridad sin ruido:** mostrar solo lo relevante para la tarea actual.
9. **Recuperación clara ante errores:** explicar qué pasó y cómo solucionarlo sin borrar lo que el usuario escribió.
10. **Ayuda contextual:** guías breves, FAQ y soporte accesible cuando hagan falta.

---

## 3. Reglas críticas de usabilidad en formularios y flujos
* **Preservación estricta de progreso:** todo enlace de consulta dentro de un formulario activo (Términos, Privacidad, Cookies, Ayuda) **debe abrirse en nueva pestaña (`target="_blank" rel="noopener noreferrer"`) o en modal accesible sin desmontar el formulario**.
* **4 estados obligatorios en cada vista:** estado normal con datos, **Loading** (esqueletos/indicadores), **Empty State** accionable y **Error** recuperable (más estado *offline* y `ErrorBoundary` + vistas `400`/`403`/`404`/`500`/`503`).
