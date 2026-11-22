# 03 — Oficio de Movimiento y Microinteracciones (*Motion Craft*)

Inspirado en principios de *Design Engineering* (*Agents with Taste* / *Animations on the Web*): el buen movimiento pasa casi desapercibido y hace que la interfaz se sienta física, rápida y confiable.

---

## 1. Primera regla: decide qué NO animar
* **Acciones de alta frecuencia = `0ms` o `<= 120ms`:** navegar con teclado, cambiar de pregunta, seleccionar un filtro rápido o alternar pestañas que el usuario pulsa decenas de veces al día **no** deben llevar animaciones lentas.
* **Nunca animes solo para "verse moderno":** si una animación no aporta **feedback inmediato**, **orientación espacial** (de dónde viene un panel) o **continuidad de estado**, elimínala.

---

## 2. Juicios concretos de duración, escala y curvas
| Tipo de interacción | Duración recomendada | Curva / comportamiento |
| :--- | :---: | :--- |
| **Feedback táctil en botones** (`:active`) | `100–150ms` | Ligera compresión (`transform: scale(0.97)`) que da respuesta física inmediata. |
| **Hover / cambio de estado sutil** | `120–160ms` | `ease-out` sobre color, borde o elevación discreta (`translateY(-1px)`). |
| **Popovers, dropdowns y tooltips** | `150–200ms` | **Consciente del origen (*origin-aware*):** `transform-origin` hacia el disparador + `scale(0.96 -> 1)` + `opacity: 0 -> 1` con `cubic-bezier(0.16, 1, 0.3, 1)`. |
| **Modales y drawers** | `200–260ms` | Entrada con `ease-out`; salida ligeramente más rápida (`150–180ms`) con `ease-in`. Nunca superar `350–400ms`. |
| **Progreso continuo / spinners** | Continuo | Única excepción donde `linear` es la curva correcta. |

---

## 3. Reglas técnicas irrenunciables
* **Interrumpibilidad:** usa transiciones CSS o *springs* interrumpibles para que, si el usuario revierte una acción a mitad de la animación, el elemento responda sin saltos bruscos.
* **Solo propiedades del compositor:** anima exclusivamente **`transform`** y **`opacity`** (y `clip-path` con moderación). Evita animar `width`, `height`, `top`, `left` o `margin` que disparan *layout reflow* y tirones en móvil.
* **No animar desde `scale(0)`:** los elementos de interfaz nacen cerca de su tamaño final (`0.95–0.98`), nunca desde cero como dibujos animados.
* **Accesibilidad obligatoria:** incluye siempre `@media (prefers-reduced-motion: reduce)` reduciendo desplazamientos/escalas a fundidos mínimos o cambios instantáneos.
* **Plataforma moderna:** cuando aplique y exista soporte progresivo, apóyate en `<dialog>`, Popover API y View Transitions con degradación limpia.
