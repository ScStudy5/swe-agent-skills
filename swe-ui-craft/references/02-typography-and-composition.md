# 02 — Tipografía, Composición y Superficies con Intención

Las reglas de esta guía no son una plantilla única: son herramientas para traducir la dirección elegida en interfaz sólida y con acabado profesional.

---

## 1. Composición guiada por el contenido (no tarjetas ni *bento* por defecto)
* **Pregunta antes de envolver en tarjeta:** ¿realmente necesita un recuadro con borde y sombra, o basta una lista con divisores finos, espacio en blanco y tipografía clara? El exceso de tarjetas anidadas vuelve cualquier interfaz genérica y pesada.
* **Densidad acorde a la tarea:**
  * *Editorial / Lectura / Landing:* ancho de lectura cómodo (`45–75ch`), respiro amplio entre secciones, una acción principal clara *above the fold*.
  * *Operativo / Dashboard / SaaS:* densidad informativa alta y ordenada, controles alcanzables en 1 clic, cero bloques decorativos que empujen los datos reales hacia abajo.
  * *Enfoque / Examen / Checkout:* eliminar navegación o ruido secundario mientras dura la tarea crítica.
* **Ritmo y proximidad:** usa una escala espacial disciplinada (ej. base `4px/8px`) asegurando siempre que el espacio **dentro** de un grupo relacionado sea menor que el espacio **entre** grupos distintos.

---

## 2. Tipografía y microtipografía
* **Jerarquía clara sin gritar:** combina **tamaño + peso + tono** para separar display, encabezados, cuerpo y metadatos.
* **Ajustes finos que separan lo amateur de lo profesional:**
  * Interlineado por rol: `1.05–1.2` en titulares grandes (con *tracking* ligeramente negativo `-0.02em`), `1.5–1.65` en cuerpo.
  * `text-wrap: balance` en titulares y `text-wrap: pretty` en párrafos.
  * `font-variant-numeric: tabular-nums` en tablas, precios, cronómetros, KPIs y columnas numéricas.
  * Preferir fuentes *self-hosted* o con fallback métrico limpio para evitar saltos de layout (CLS) o bloqueos CSP.

---

## 3. Color, superficies y alineación óptica
* **Jerarquía de superficies:** distingue fondo base, superficie de trabajo y superficie elevada mediante cambio sutil de luminosidad y **bordes finos de baja opacidad (`1px`)** antes que recurrir a sombras difusas pesadas.
* **Color con intención:** reserva el color de acento para la acción primaria, estado activo y foco; cumple contraste **WCAG 2.2 AA** (`4.5:1` texto normal, `3:1` texto grande y controles) tanto en modo claro como oscuro.
* **Alineación óptica:** verifica visualmente que iconos y texto compartan centro óptico, que los radios anidados respeten relación geométrica (`radio externo = radio interno + padding`) y que un solo set de iconos mantenga grosor de trazo uniforme.

---

## 4. Integridad de layout en distintos tamaños de pantalla
* **Páginas cortas con pie de página:** cuando el diseño incluya un `<footer>` tradicional, evita que quede flotando en vistas cortas (`/login`, `/cookies`, `/404`) aplicando `min-height: 100dvh; display: flex; flex-direction: column;` y `main { flex: 1; }` (omitir en interfaces *full-screen* tipo editor, mapa o canvas sin pie de página).
* **Responsive real (no solo cero overflow):** diseña proporciones conscientes en `390px`, `768px`, `1440px` y `1920px`; apoya los componentes adaptables en unidades `dvh`/`svh`, Container Queries y `:has()` cuando el layout lo necesite. *(Las decisiones de rendimiento técnico como *code splitting* o caché viven en `swe-data-apis`.)*
