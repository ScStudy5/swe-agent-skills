---
name: swe-ux-accessibility
description: >-
  Guía profesional de estrategia UX (investigación con usuarios, flujos, heurísticas),
  dirección visual anti-genérica (referencias visuales, Design Tokens de tipografía,
  espaciado, color y animaciones), diseño responsive (Mobile First), accesibilidad web
  (WCAG 2.2 AA, WAI-ARIA, ISO 9241-210), SEO público, compatibilidad/i18n y crítica
  visual en navegador real con Playwright. Usar al investigar, diseñar, construir o
  auditar interfaces web/móviles (complementar capturas y auditoría en vivo con
  swe-browser-audit).
---

# UX/UI, Dirección Visual, Responsive, Accesibilidad y Compatibilidad

Aplica esta skill en cualquier aplicación con interfaz de usuario (web, PWA, móvil o escritorio) para lograr diseños profesionales (no genéricos), usables, accesibles y verificados visualmente en navegador real.

## Regla fundamental
**Diseño con intención, usabilidad probada y evidencia visual:** una interfaz profesional no es una plantilla genérica ni solo "funciona en tu pantalla"; parte de las necesidades del usuario, define reglas claras de tipografía/espaciado/color/movimiento, cumple accesibilidad **WCAG 2.2 AA** y se valida mirando capturas reales en navegador (desktop, tablet y móvil).

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto para calibrar el alcance de UX Research, Design System, auditoría WCAG formal e i18n/l10n.

* **Integración opcional del entorno:** si `modern-web-guidance` está disponible, consúltala **primero** para patrones actuales de HTML/CSS/JS (modales, formularios, animaciones, sanitización, Core Web Vitals). Si usas librerías UI (React, Tailwind, Next.js, Vue, etc.) y `Context7` está disponible, consulta sus docs vigentes antes de implementar. Para capturar screenshots reales y verificar accesibilidad, consola y responsive en vivo, complementa con `swe-browser-audit`.

## Flujo de trabajo

### 1. Planificar o diseñar interfaz y experiencia
1. **Estrategia UX e investigación con usuarios:** antes de diseñar pantallas, define problema, *Jobs-to-be-Done*, flujos principales (*User Flows*), arquitectura de información, densidad adecuada al producto y aplica las **10 heurísticas de Nielsen** (y pruebas ligeras de usabilidad con 3–5 usuarios cuando corresponda).
2. **Referencias visuales y dirección de arte (anti-genérico):** analiza 2–3 referencias reales del sector para afinar criterio visual (ritmo, contraste tipográfico, superficies, densidad — sin copiar marca ni activos) y fija una **Hoja de Dirección Visual + Design Tokens** antes de codificar:
   * **Tipografía:** par tipográfico intencional, escala modular clara, `line-height` por rol, ancho de lectura `45–75ch` y `tabular-nums` en métricas/tablas.
   * **Espaciado y composición:** escala `4px/8px` (micro/componente/grupo/sección), ley de proximidad, alineación en rejilla y variedad compositiva (evitar filas repetitivas de tarjetas genéricas).
   * **Color y superficies:** proporción `60-30-10`, neutros con matiz, bordes sutiles, contraste WCAG AA y evitar clichés genéricos (gradientes neón sin propósito, abuso de sombras/glassmorphism o emojis como iconos).
   * **Animaciones y oficio *Design Engineering*:** acciones frecuentes instantáneas o `<=150ms`, popovers/modales *origin-aware* (`scale(0.96->1)` + `opacity`), feedback táctil (`scale(0.97)`), solo `transform`/`opacity` y respeto a `prefers-reduced-motion`.
   * **Layout moderno y preservación de formularios:** `min-height: 100dvh` con *sticky footer* (cero footers flotando en páginas cortas), *code splitting* por ruta, patrones modernos (`<dialog>`, `dvh`, Container Queries) y **enlaces legales/ayuda dentro de formularios siempre con `target="_blank" rel="noopener noreferrer"` o modal** para nunca perder lo que el usuario ya escribió.
3. **Mobile First, Responsive y Estados de UI:** define breakpoints, CSS Grid/Flexbox, áreas táctiles ≥ `44×44px`, cero scroll horizontal y contempla siempre los **4 estados clave** de cada pantalla/componente:
   * Datos cargados (estado normal)
   * **Loading** (esqueletos o indicadores claros)
   * **Empty State** (estado vacío con guía accionable)
   * **Error** (mensajes comprensibles y recuperación)
   * Más confirmaciones para acciones destructivas/irreversibles.
4. **Accesibilidad desde el inicio (WCAG 2.2 AA):** estructura HTML semántica con atributo `lang`, contraste adecuado, foco visible, navegación completa por teclado (orden lógico de `Tab`, menús desplegables y foco controlado en modales), `WAI-ARIA` solo cuando el HTML semántico no baste, `prefers-reduced-motion` y compatibilidad con lectores de pantalla.
5. **Compatibilidad, i18n/l10n y SEO/publicación web:** UTF-8, manejo normalizado de fechas y zonas horarias, externalización de textos (i18n), formatos locales/monetarios (l10n) y, en sitios públicos, metadatos (`title`, `description`, `favicon`, Open Graph, URLs canónicas), `robots.txt`/`sitemap.xml`, `noindex` en paneles administrativos y páginas `404`/`500` limpias.

Consulta el detalle completo en [design-craft-and-ux-strategy.md](./references/design-craft-and-ux-strategy.md) y [ux-a11y-compatibility.md](./references/ux-a11y-compatibility.md).

### 2. Auditar UI, criterio visual, accesibilidad y compatibilidad
Revisa vistas, componentes, CSS y **capturas reales en navegador** buscando:
1. **Crítica visual en vivo con Playwright (`swe-browser-audit`):** ejecuta `playwright_security_audit.mjs` con `--screenshots-dir` para capturar `desktop` (`1440×900`), `tablet` (`768×1024`) y `mobile` (`390×844`) (*above the fold* y `fullPage`, y `--color-scheme both` si hay modo oscuro), inspecciona las imágenes capturadas evaluando test de 3 segundos, jerarquía tipográfica, espaciado, alineación, contraste e identidad visual, corrige y vuelve a capturar.
2. **Accesibilidad (WCAG 2.2 AA):** falta de `alt` en imágenes, inputs sin `<label>` o nombre accesible, `div`/`span` usados como botones sin soporte de teclado, foco oculto (`outline: none` sin reemplazo), contraste insuficiente, dependencia exclusiva del color para transmitir estado o errores, falta de subtítulos en multimedia.
3. **Responsive y UX:** anchos fijos que rompen en móvil, formularios incómodos en pantallas pequeñas, falta de validación clara en formularios, ausencia de estados vacíos/carga o acciones destructivas sin confirmación.
4. **Compatibilidad:** textos concatenados difíciles de traducir, fechas formateadas sin zona horaria, APIs modernas sin respaldo o dependencias obsoletas.
5. Recomienda verificación automatizada con **axe-core** y **Lighthouse** más pruebas manuales de teclado y lector de pantalla.

### 3. Generar artefactos y mejoras
Genera cuando se soliciten:
* **Hoja de Dirección Visual y Design Tokens** (tipografía, escala de espaciado `4/8px`, paleta `60-30-10`, superficies y movimiento) basada en referencias del dominio.
* **Informe de Crítica Visual + Auditoría WCAG 2.2 AA** apoyado en capturas de Playwright con correcciones concretas de HTML/ARIA/CSS.
* Flujos de usuario (*User Flows*), evaluación heurística de Nielsen o guía de pruebas de usabilidad.
* Guía de internacionalización (`i18n`), fechas/zonas horarias, SEO público y soporte de navegadores/dispositivos.

## Criterios de verificación
* La interfaz sigue un sistema coherente de Design Tokens (tipografía, espaciado, color y animaciones) en lugar de estilos arbitrarios o plantillas genéricas.
* Todo componente interactivo es operable al 100 % con teclado y tiene foco visible y rol/nombre accesible.
* Cada vista contempla estados de carga, vacío, error y prevención de acciones destructivas.
* Cuando existe una app web en ejecución, el diseño se verificó visualmente con capturas reales en navegador (`desktop`, `tablet` y `mobile`), no solo leyendo código.
