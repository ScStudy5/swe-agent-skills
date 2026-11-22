---
name: swe-ux-accessibility
description: >-
  Guía profesional de diseño UX/UI, diseño responsive (Mobile First), accesibilidad
  web (WCAG 2.2 AA, WAI-ARIA, ISO 9241-210) y compatibilidad tecnológica (navegadores,
  UTF-8, zonas horarias, i18n/l10n). Usar al diseñar o revisar interfaces, formularios,
  design systems, accesibilidad o soporte multiplataforma (para auditoría en vivo en
  navegador con axe-core usar swe-browser-audit).
---

# UX/UI, Responsive, Accesibilidad y Compatibilidad

Aplica esta skill en cualquier aplicación con interfaz de usuario (web, PWA, móvil o escritorio) y en requisitos de compatibilidad e internacionalización.

## Regla fundamental
**Experiencia consistente, moderna y accesible:** una aplicación profesional no funciona únicamente en una computadora ni solo con ratón y vista perfecta; debe adaptarse a múltiples dispositivos, resoluciones, idiomas y capacidades humanas, evitando diseño genérico o patrones HTML/CSS/JS obsoletos.

* **Nivel de rigor:** si el usuario no indicó el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`), pregúntalo o infiérelo del contexto para calibrar el alcance de Design System, auditoría WCAG formal e i18n/l10n.

* **Integración opcional del entorno:** si `modern-web-guidance` está disponible, consúltala **primero** para patrones actuales de HTML/CSS/JS (modales, formularios, animaciones, sanitización, Core Web Vitals). Si usas librerías UI (React, Tailwind, Next.js, Vue, etc.) y `Context7` está disponible, consulta sus docs vigentes antes de implementar. Para verificar accesibilidad, consola y responsive en vivo, complementa con `swe-browser-audit`.

## Flujo de trabajo

### 1. Planificar o diseñar interfaz y experiencia
1. **Mobile First y Responsive:** define breakpoints, CSS Grid/Flexbox, tipografía e imágenes adaptables, áreas táctiles suficientes (mínimo 44x44 px o equivalente cómodo en móvil), navegación adaptable y cero scroll horizontal no deseado.
2. **Design System y Estados de UI:** asegura componentes reutilizables, jerarquía visual clara y contempla siempre los **4 estados clave** de cada pantalla/componente:
   * Datos cargados (estado normal)
   * **Loading** (esqueletos o indicadores claros)
   * **Empty State** (estado vacío con guía accionable)
   * **Error** (mensajes comprensibles y recuperación)
   * Más confirmaciones para acciones destructivas/irreversibles.
3. **Accesibilidad desde el inicio (WCAG 2.2 AA):** estructura HTML semántica, contraste adecuado, foco visible, navegación completa por teclado, `WAI-ARIA` solo cuando el HTML semántico no baste, `prefers-reduced-motion` y compatibilidad con lectores de pantalla.
4. **Compatibilidad e i18n/l10n:** UTF-8, manejo normalizado de fechas y zonas horarias, externalización de textos (i18n) y formatos locales/monetarios (l10n).

Consulta el detalle completo en [ux-a11y-compatibility.md](./references/ux-a11y-compatibility.md).

### 2. Auditar UI, accesibilidad y compatibilidad
Revisa vistas, componentes o CSS buscando:
1. **Accesibilidad (WCAG 2.2 AA):** falta de `alt` en imágenes, inputs sin `<label>` o nombre accesible, `div`/`span` usados como botones sin soporte de teclado, foco oculto (`outline: none` sin reemplazo), contraste insuficiente, dependencia exclusiva del color para transmitir estado o errores, falta de subtítulos en multimedia.
2. **Responsive y UX:** anchos fijos que rompen en móvil, formularios incómodos en pantallas pequeñas, falta de validación clara en formularios, ausencia de estados vacíos/carga o acciones destructivas sin confirmación.
3. **Compatibilidad:** textos concatenados difíciles de traducir, fechas formateadas sin zona horaria, APIs modernas sin respaldo o dependencias obsoletas.
4. Recomienda verificación automatizada con **axe-core** y **Lighthouse** más pruebas manuales de teclado y lector de pantalla.

### 3. Generar artefactos y mejoras
Genera cuando se soliciten:
* Auditoría WCAG 2.2 AA con correcciones concretas de HTML/ARIA/CSS.
* Checklist de revisión UX/Responsive para un Design System o pantalla.
* Guía de internacionalización (`i18n`), fechas/zonas horarias y soporte de navegadores/dispositivos.

## Criterios de verificación
* Todo componente interactivo es operable al 100 % con teclado y tiene foco visible y rol/nombre accesible.
* Cada vista contempla estados de carga, vacío, error y prevención de acciones destructivas.
* Las fechas, monedas y textos siguen reglas claras de UTF-8, zona horaria e i18n/l10n cuando aplica.
