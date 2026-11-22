---
name: swe-ux-accessibility
description: >-
  Guía profesional de estrategia UX (investigación con usuarios, User Flows,
  arquitectura de información, 10 heurísticas de Nielsen), diseño responsive
  (Mobile First, 4 estados de UI, preservación de formularios, vistas de error y
  ErrorBoundary), accesibilidad transversal (WCAG 2.2 AA, WAI-ARIA, ISO 9241-210),
  SEO público, compatibilidad e i18n/l10n. Usar al diseñar flujos, formularios,
  accesibilidad o SEO (para dirección visual anti-genérica, tipografía, movimiento
  y crítica estética usar swe-ui-craft; para auditoría en vivo con axe-core y
  capturas usar swe-browser-audit).
---

# Estrategia UX, Responsive, Accesibilidad (WCAG 2.2 AA), SEO y Compatibilidad

Aplica esta skill como requisito transversal en cualquier aplicación con interfaz de usuario (web, PWA, móvil o escritorio) para asegurar usabilidad real, accesibilidad, resiliencia de UI, SEO público e internacionalización.

## Regla fundamental
**Usabilidad validada y accesibilidad transversal:** ninguna interfaz se considera lista si solo funciona con ratón, en pantalla grande o con vista perfecta, o si hace perder progreso al usuario.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto para calibrar UX Research, auditoría WCAG formal e i18n/l10n.
* **Límites con otras skills:**
  * **Dirección visual, exploración de 3 alternativas, tipografía, composición anti-genérica, movimiento y crítica estética** -> `swe-ui-craft`.
  * **Auditoría dinámica, `axe-core` y capturas en navegador real** -> `swe-browser-audit`.
  * **Implementación web moderna (`<dialog>`, Popover, CSS moderno)** -> `Modern Web Guidance` si está disponible; docs de librerías -> `Context7`.

## Flujo de trabajo

### 1. Planificar flujos UX, accesibilidad, SEO y compatibilidad
1. **Estrategia UX e investigación con usuarios:** define *Jobs-to-be-Done*, *User Flows*, arquitectura de información, aplica las **10 heurísticas de Nielsen** y valida con 3–5 usuarios cuando corresponda (ver [ux-research-and-product-strategy.md](./references/ux-research-and-product-strategy.md)).
2. **Mobile First, Responsive y Estados de UI:** define breakpoints, áreas táctiles ≥ `44×44px`, cero scroll horizontal, **enlaces legales/ayuda dentro de formularios siempre en `target="_blank" rel="noopener noreferrer"` o modal** (para nunca borrar lo escrito) y contempla siempre los **4 estados clave**:
   * Datos cargados (estado normal)
   * **Loading** (esqueletos o indicadores claros)
   * **Empty State** (estado vacío con guía accionable)
   * **Error** (mensajes comprensibles y recuperación, más confirmaciones para acciones destructivas/irreversibles).
3. **Accesibilidad desde el inicio (WCAG 2.2 AA):** estructura HTML semántica con atributo `lang`, contraste adecuado, foco visible, navegación completa por teclado (orden lógico de `Tab`, menús desplegables y foco controlado en modales), `WAI-ARIA` solo cuando el HTML semántico no baste, `prefers-reduced-motion`, compatibilidad con lectores de pantalla y **Declaración de Accesibilidad (`/accesibilidad`)**.
4. **Resiliencia UI, compatibilidad, i18n/l10n y SEO público:** UTF-8, fechas en UTC/ISO 8601, i18n/l10n, **`ErrorBoundary` global + vistas `400`/`403`/`404`/`500`/`503` + estado *offline*** y, en sitios públicos, metadatos (`title`, `description`, `favicon`, Open Graph, canónicas), `robots.txt`/`sitemap.xml` y `noindex` en paneles administrativos.

Consulta el detalle completo en [ux-research-and-product-strategy.md](./references/ux-research-and-product-strategy.md) y [ux-a11y-compatibility.md](./references/ux-a11y-compatibility.md).

### 2. Auditar UX, accesibilidad y compatibilidad
Revisa vistas, componentes y rutas buscando:
1. **Accesibilidad (WCAG 2.2 AA):** falta de `alt` en imágenes, inputs sin `<label>` o nombre accesible, `div`/`span` usados como botones sin teclado, foco oculto, contraste insuficiente, dependencia exclusiva del color, saltos de jerarquía `h1–h6` o falta de subtítulos.
2. **UX y Responsive:** anchos fijos que rompen en móvil, formularios que pierden progreso al abrir enlaces legales, falta de estados vacíos/carga/error o acciones destructivas sin confirmación.
3. **Compatibilidad y SEO:** textos concatenados difíciles de traducir, fechas sin zona horaria, páginas `404`/`500` faltantes o metadatos/enlaces rotos.
4. Ejecuta verificación automatizada con **`swe-browser-audit` (`axe-core`)** y **Lighthouse** más pruebas manuales de teclado y lector de pantalla. *(Para crítica estética/identidad sobre capturas usa `swe-ui-craft`.)*

### 3. Generar artefactos
Genera cuando se soliciten:
* Flujos de usuario (*User Flows*), evaluación heurística de Nielsen o guion de pruebas de usabilidad.
* Auditoría WCAG 2.2 AA con correcciones concretas de HTML/ARIA/CSS y borrador de `/accesibilidad`.
* Guía de internacionalización (`i18n`), fechas/zonas horarias y checklist de SEO público.

## Criterios de verificación
* Todo componente interactivo es operable al 100 % con teclado, tiene foco visible y rol/nombre accesible (`axe-core` sin violaciones).
* Cada vista contempla estados de carga, vacío, error, prevención de acciones destructivas y cero pérdida de estado en formularios.
* Las fechas, monedas, metadatos SEO y vistas de error (`400`/`403`/`404`/`500`/`503`) siguen los estándares definidos.
