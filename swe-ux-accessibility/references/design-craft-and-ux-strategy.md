# Estrategia UX, Dirección Visual Anti-Genérica y Crítica Visual con Playwright

Usa esta guía junto a [ux-a11y-compatibility.md](./ux-a11y-compatibility.md) antes y después de construir cualquier interfaz para pasar de una UI "que funciona" o "genérica" a un diseño profesional con intención visual, usabilidad validada y evidencia real en navegador.

---

## 1. Estrategia de producto e investigación con usuarios (UX Research)

Un buen diseño visual nunca rescata una experiencia confusa. Antes de diseñar pantallas:

* **Claridad de problema y *Jobs-to-be-Done* (JTBD):** define qué tarea concreta necesita completar el usuario, en qué contexto (oficina, móvil en movimiento, urgencia) y cuál es la señal de éxito en menos de 10 segundos.
* **Investigación proporcional al nivel del proyecto:**
  * **Nivel 1 (MVP):** 3–5 entrevistas breves o pruebas rápidas de prototipo con usuarios reales (o personas del perfil objetivo) para detectar fricciones críticas antes de programar.
  * **Nivel 2 (Profesional):** mapas de flujo (*User Flows / User Journeys*), arquitectura de información clara (máximo 5–7 ítems en navegación primaria), pruebas de usabilidad moderadas con 5 usuarios sobre tareas clave y análisis de embudos/abandono (RUM ético).
  * **Nivel 3 (Empresarial):** investigación continua, validación multi-rol, tests A/B controlados, evaluación formal bajo **ISO 9241-210** y accesibilidad auditada con usuarios reales de tecnologías de asistencia.
* **10 Heurísticas de Usabilidad (Nielsen) como filtro mínimo:** visibilidad del estado del sistema, lenguaje natural del usuario (no jerga técnica de BD), control y libertad (*deshacer/cancelar*), consistencia, prevención de errores antes que mensajes de error, reconocimiento antes que recuerdo, flexibilidad/atajos para usuarios frecuentes, estética minimalista sin ruido, recuperación clara ante errores y ayuda contextual.
* **Densidad calibrada al tipo de producto:**
  * *Landing / Editorial / Marketing:* mucho espacio en blanco, narrativa visual clara, 1 CTA principal por sección.
  * *SaaS / Dashboard / ERP:* mayor densidad informativa útil, tablas alineadas con números tabulares, filtros rápidos, cero decoración que robe espacio de trabajo.
  * *E-commerce:* fotografía protagonista, precio/disponibilidad/confianza inmediatos y checkout sin fricción.

---

## 2. Referencias visuales y dirección de arte (antes de escribir código)

Para elevar el criterio visual y evitar improvisar estilos incoherentes:

1. **Benchmarking con 2–3 referencias reales:** selecciona productos referentes del mismo dominio (o de un sector afín de alta calidad) y analiza explícitamente **qué funciona** en ellos:
   * Ritmo de espaciado y aire entre secciones.
   * Contraste tipográfico entre titulares, subtítulos, metadatos y cuerpo.
   * Tratamiento de superficies (fondos, bordes, elevación, uso de fotografía/ilustración).
   * Patrones de navegación, tablas, formularios y estados vacíos.
   * *(Regla ética y legal: extrae principios estructurales y criterio visual; **nunca** copies marca, copy, ilustraciones ni activos con derechos de autor).*
2. **Definir una Hoja de Dirección Visual breve (*Design Brief*) antes de codificar:** fija en 10–15 líneas el tono estético (ej. *editorial limpio*, *industrial preciso*, *cálido y humano*, *técnico de alto contraste*), el par tipográfico, la paleta base y las reglas de espaciado/movimiento. Mantén esa dirección consistente en toda la aplicación.

---

## 3. Reglas concretas contra diseños genéricos (*Design Tokens*)

Define siempre los valores como **Design Tokens** (CSS custom properties / tema de Tailwind / tokens de Design System) en lugar de números arbitrarios sueltos:

### A. Tipografía con jerarquía real
* **Emparejamiento intencional:** combina una fuente con carácter para títulos/display y una sans-serif limpia de alta legibilidad para interfaz/cuerpo (más una monoespaciada para código, IDs o métricas técnicas). Evita usar la fuente por defecto sin ajustar escala, peso ni tracking.
* **Escala modular y contraste claro:** diferencia drásticamente `display` / `h1` / `h2` / `body` / `caption` combinando **tamaño + peso + color** (ej. título en tono neutro más oscuro y peso `600–700`, cuerpo en tono secundario legible `400`, metadatos más compactos).
* **Microtipografía profesional:**
  * Interlineado ajustado por rol: `1.05–1.2` en titulares grandes (con *letter-spacing* ligeramente negativo `-0.02em`), `1.5–1.65` en párrafos.
  * Ancho de línea óptimo en bloques de lectura: **`45–75ch`** (`max-width: 65ch`).
  * Usar `text-wrap: balance` en titulares y `text-wrap: pretty` en párrafos cuando el navegador lo soporte.
  * Usar `font-variant-numeric: tabular-nums` en tablas, precios, contadores y métricas para que las columnas numéricas alineen perfectamente.

### B. Espaciado, rejilla y composición
* **Escala base `4px / 8px`:** restringe márgenes y rellenos a una escala disciplinada (`4, 8, 12, 16, 24, 32, 48, 64, 96px`) agrupada por intención:
  * *Micro* (`4–8px`): icono con texto, etiqueta con input.
  * *Componente* (`12–16px`): padding interno de botones, inputs y controles.
  * *Grupo* (`20–32px`): separación entre bloques relacionados o interior de tarjetas.
  * *Sección* (`48–96px`): respiro estructural entre secciones principales.
* **Ley de proximidad:** el espacio **dentro** de un componente o grupo relacionado debe ser siempre menor que el espacio **entre** grupos distintos.
* **Alineación y variedad compositiva:** alinea elementos sobre una rejilla real; **evita el patrón genérico** de repetir indefinidamente filas de 3 tarjetas idénticas centradas con un icono en un círculo arriba. Alterna composiciones (bento asimétrico, bloque editorial con vista de producto, listas limpias con divisores sutiles, tablas funcionales).

### C. Color y superficies
* **Proporción 60-30-10:** ~60 % superficies neutras limpias, ~30 % superficies secundarias/texto/bordes, ~10 % color de acento reservado para acciones primarias y foco.
* **Neutros con matiz y bordes sutiles:** prefiere neutros ligeramente cálidos o fríos acordes a la marca y jerarquía de superficies (fondo -> contenedor -> elevado) apoyada en **bordes finos de baja opacidad (`1px`)** más que en sombras difusas pesadas.
* **Semántica accesible:** define tokens de estado (`success`, `warning`, `danger`, `info`) verificando contraste mínimo **WCAG AA** (`4.5:1` texto normal, `3:1` texto grande y componentes UI) tanto en modo claro como oscuro.
* **Antipatrones genéricos a evitar:** gradientes morado/azul neón sin relación con la marca, abuso de *glassmorphism* con texto poco legible, exceso de tarjetas anidadas dentro de tarjetas, sombras exageradas y uso de emojis como sustituto de iconografía profesional.

### D. Animaciones y microinteracciones
* **Propósito funcional, nunca decoración lenta:** cada animación debe comunicar feedback inmediato (hover/press/loading), orientar espacialmente (abrir panel/drawer) o dar continuidad de estado.
* **Duraciones y curvas calibradas:**
  * Microinteracciones (botones, toggles, tooltips): `120–180ms`.
  * Transiciones de layout/modales/drawers: `200–320ms` (evitar animaciones > `400ms` que hagan sentir lenta la app).
  * Curvas naturales: `ease-out` para entradas (ej. `cubic-bezier(0.16, 1, 0.3, 1)`), `ease-in` para salidas; evitar `linear` salvo en spinners/progreso continuo.
* **Rendimiento y accesibilidad:** anima preferentemente propiedades del compositor (**`transform`** y **`opacity`**) evitando reflows (`width`, `height`, `top`, `left`), y respeta siempre `@media (prefers-reduced-motion: reduce)`.

### E. Iconografía e imaginería
* Usa **un solo set de iconos coherente** (mismo grosor de trazo, esquinas y tamaño óptico: `16px`, `20px`, `24px`).
* Usa imágenes reales, recortes consistentes (`aspect-ratio` + `object-cover`) y nunca mezcles ilustraciones 3D, flat y fotos de stock incompatibles en la misma vista.

---

## 4. Ciclo de Crítica Visual (*Visual Design Critique*) con Playwright

No apruebes una interfaz solo leyendo código HTML/CSS: **mírala renderizada en navegador real** usando `swe-browser-audit`:

1. **Capturar evidencia real en navegador:** ejecuta el script de Playwright con `--screenshots-dir` sobre las rutas clave:
   ```bash
   node <ruta-de-swe-browser-audit>/scripts/playwright_security_audit.mjs http://localhost:3000 \
     --routes /,/dashboard,/login --screenshots-dir .audit-screenshots --out audit-report.json
   ```
   *(Agrega `--color-scheme both` si la aplicación soporta modo claro y modo oscuro.)*
2. **Inspeccionar las capturas (`desktop` `1440×900`, `tablet` `768×1024`, `mobile` `390×844` — tanto *above the fold* como `fullPage`)** aplicando este checklist de crítica visual:
   * **Test de los 3 segundos (primer pantallazo):** ¿se entiende de inmediato qué es el producto y cuál es la acción principal *above the fold* sin hacer scroll?
   * **Jerarquía y tipografía:** ¿destaca el titular principal sobre subtítulos y cuerpo? ¿Algún bloque tiene líneas demasiado largas (`>75ch`), texto cortado o huérfanos incómodos?
   * **Espaciado y alineación:** ¿hay elementos apretados, márgenes inconsistentes, bordes desalineados o exceso de espacio muerto?
   * **Identidad vs. genérico:** ¿se ve como una plantilla genérica repetitiva o tiene dirección visual coherente y limpia?
   * **Contraste y estados:** ¿todo texto, placeholder, borde de input y botón tiene contraste claro en modo claro y oscuro?
   * **Responsive real:** ¿hay overflow horizontal, menús rotos, botones demasiado pequeños en móvil o tablas que desbordan sin scroll contenido?
3. **Iterar y volver a capturar:** corrige los hallazgos detectados y ejecuta una nueva captura con Playwright para confirmar visualmente la mejora antes de dar por cerrada la tarea. *(No subas carpetas temporales de capturas a Git).*
