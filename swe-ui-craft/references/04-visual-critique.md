# 04 — Protocolo de Crítica Visual de Identidad y Oficio

Pasar `axe-core` y tener `overflow: false` confirma corrección técnica, **no** confirma buen diseño. Esta guía evalúa las capturas reales de Playwright con ojos de diseño.

---

## 1. Capturar evidencia completa con `swe-browser-audit`
Antes de evaluar, genera capturas reales en los 4 tamaños y ambos temas (si la app soporta modo oscuro), incluyendo al menos **una ruta principal** y **una ruta corta** (`/login`, `/cookies` o `/404`):

```bash
node <ruta-de-swe-browser-audit>/scripts/playwright_security_audit.mjs http://localhost:4173 \
  --routes /,/login,/cookies --screenshots-dir .audit-screenshots --color-scheme both --out audit-report.json
```

Inspecciona visualmente las imágenes PNG en `wide` (`1920×1080`), `desktop` (`1440×900`), `tablet` (`768×1024`) y `mobile` (`390×844`) — tanto *above the fold* como `fullPage`.

---

## 2. Preguntas de juicio estético y de identidad (obligatorias)
1. **Adecuación al producto:** si tapas el logotipo, ¿esta pantalla parece diseñada para **este** producto específico o parece una plantilla genérica que serviría para cualquier SaaS?
2. **Test de los 3 segundos (*above the fold*):** en el primer pantallazo (tanto en `1440px` como en `390px`), ¿se distingue al instante el propósito, el contenido protagonista y la acción principal sin competir entre sí?
3. **Intención en cada sección:** ¿cada bloque aporta información o interacción útil, o hay secciones de relleno con tarjetas repetitivas que no dicen nada nuevo?
4. **Ritmo y jerarquía:** ¿hay variación visual sana entre secciones y contraste claro entre títulos, cuerpo y metadatos, o todo pesa igual?
5. **Páginas cortas y pantallas amplias (`1920×1080`):** ¿el `<footer>` descansa abajo (`100dvh`) sin huecos negros/blancos muertos? ¿El ancho máximo se siente equilibrado en monitores grandes?
6. **Acabado en móvil (`390×844`):** ¿el encabezado respira sin apelmazarse ni cortar texto? ¿Los botones clave tienen tamaño táctil cómodo (`>=44px`)? ¿Algún banner flotante (cookies, chat, toast) tapa controles o contenido clave?
7. **Consistencia en modo oscuro:** ¿las superficies se distinguen entre sí sin verse "lavadas" ni con bordes chillones, y el texto secundario sigue siendo cómodo de leer?

---

## 3. Señales de alarma ("síntomas de diseño genérico" -> rehacer)
* Más de dos secciones seguidas con la misma cuadrícula simétrica de 3 tarjetas centradas con icono en círculo.
* Gradientes decorativos sin relación con la identidad del producto o *glassmorphism* que reduce contraste.
* Textos de párrafo estirados a más de `75ch` o líneas sueltas desalineadas.
* Un *footer* flotando en páginas cortas o enlaces dentro de formularios que navegan en la misma pestaña borrando lo escrito.

---

## 4. Ciclo obligatorio de cierre
**Capturar -> Listar fallos concretos de identidad/layout/acabado -> Corregir -> Re-capturar y confirmar visualmente** antes de declarar la interfaz terminada.
