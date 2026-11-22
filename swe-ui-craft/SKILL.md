---
name: swe-ui-craft
description: >-
  Oficio de diseño visual, dirección de arte anti-genérica y Design Engineering:
  explora tesis visual y 3 direcciones distintas antes de codificar, define criterio
  de tipografía, composición, superficies, movimiento/microinteracciones (estilo
  Emil Kowalski) y crítica visual de identidad sobre capturas reales de Playwright.
  Usar al definir el aspecto visual de una interfaz, refinar diseño/animaciones o
  corregir pantallas genéricas (complementar accesibilidad/UX/SEO con
  swe-ux-accessibility y capturas en navegador con swe-browser-audit).
---

# Dirección Visual, Oficio UI (*Design Engineering*) y Crítica Estética

Aplica esta skill cuando diseñes, rediseñes o evalúes la calidad visual, composición y microinteracciones de una interfaz web, PWA, móvil o escritorio.

## Regla fundamental
**Criterio derivado del producto, nunca una receta fija:** un diseño distintivo no sale de aplicar siempre la misma fórmula (*bento + tarjetas + 60-30-10 + serif display*), sino de un **proceso explícito de decisiones** —tesis visual, exploración de alternativas reales, reglas concretas de oficio y crítica visual sobre capturas reales en navegador.

* **Lectura selectiva por tarea (ahorro de contexto):** no cargues todas las referencias a la vez; lee **solo** la micro-guía que corresponda a la fase actual.
* **Límites claros con otras herramientas:**
  * **Accesibilidad WCAG 2.2 AA, UX Research, formularios, errores y SEO** -> `swe-ux-accessibility` (requisito transversal irrenunciable).
  * **Implementación web moderna (`<dialog>`, Popover, CSS moderno, compatibilidad)** -> `Modern Web Guidance` si está instalada.
  * **Documentación vigente de librerías UI (React, Tailwind, Next.js, etc.)** -> `Context7` si está disponible.
  * **Capturas reales en navegador (`wide`/`desktop`/`tablet`/`mobile`, `light`/`dark`)** -> `swe-browser-audit`.

## Flujo de trabajo en 4 fases

### Fase 1 — Exploración visual antes de codificar (obligatoria en UI nueva o rediseño)
Lee [01-visual-exploration.md](./references/01-visual-exploration.md):
1. Redacta una **Tesis Visual** de 2–3 líneas derivada del producto (usuario, contexto, contenido dominante y sensación objetivo).
2. Presenta **3 direcciones visuales realmente distintas** (distinta composición, densidad, tipografía, tratamiento del contenido y 1–2 referencias razonadas indicando **qué principio se adopta y qué se descarta** — nunca la misma pantalla con otros colores).
3. Elige 1 dirección junto con el usuario y guarda un contrato compacto (`DESIGN_DIRECTION.md`, <40 líneas) con **qué patrones SÍ usar** y **qué patrones PROHIBIR** en este proyecto.

### Fase 2 — Tipografía, composición y superficies con intención
Lee [02-typography-and-composition.md](./references/02-typography-and-composition.md):
1. Elige la estructura que mejor sirva al contenido real (lista editorial, tabla operativa densa, lienzo enfocado, barra lateral fija, etc.) sin imponer tarjetas ni *bento* por defecto.
2. Define tokens del proyecto (tipografía, escala de espaciado, superficies, bordes, contraste óptico), garantiza `min-height: 100dvh` con *sticky footer* en páginas cortas y aplica *code splitting* por ruta.

### Fase 3 — Movimiento y microinteracciones con oficio
Lee [03-motion-craft.md](./references/03-motion-craft.md):
1. Decide primero **qué NO animar** (interacciones de alta frecuencia como navegación de teclado, filtros rápidos o cambio frecuente de pestañas deben ser instantáneas o `<= 150ms`).
2. Aplica juicios concretos: entradas *origin-aware* (`scale(0.96 -> 1)` + `opacity`), compresión táctil sutil (`scale(0.97)`), animaciones interrumpibles solo en `transform`/`opacity` y respeto estricto a `prefers-reduced-motion`.

### Fase 4 — Crítica visual de identidad sobre capturas reales
Lee [04-visual-critique.md](./references/04-visual-critique.md):
1. Captura la interfaz en ejecución con `swe-browser-audit` (`--screenshots-dir .audit-screenshots --color-scheme both`) en `wide` (`1920×1080`), `desktop` (`1440×900`), `tablet` (`768×1024`) y `mobile` (`390×844`), incluyendo al menos una página corta (`/login`, `/cookies` o `/404`).
2. Inspecciona las imágenes evaluando **identidad, ritmo, jerarquía del contenido, acabado óptico y ausencia de clichés** (además de overflow/contraste), corrige y vuelve a capturar antes de dar por cerrada la entrega.

## Criterios de verificación
* La dirección visual deriva de una tesis del producto y fue elegida entre alternativas distintas (no una plantilla transversal repetida).
* Cada decisión de layout, tipografía y movimiento responde al tipo de contenido real y evita componentes de relleno.
* El resultado fue validado mirando capturas reales en los 4 viewports (incluyendo páginas cortas y modo claro/oscuro si aplica), no solo leyendo código.
