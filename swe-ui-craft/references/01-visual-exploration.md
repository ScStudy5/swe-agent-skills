# 01 — Exploración Visual y Decisión de Dirección (Antes de Codificar)

El diseño genérico ocurre cuando se salta directamente del requisito al CSS usando el primer estilo que viene a la mente. Ejecuta este proceso breve antes de crear el primer componente visual.

---

## 1. Escribir la Tesis Visual (2–3 líneas)
Responde con precisión para **este** producto específico:
* **Quién lo usa y en qué estado mental:** (ej. estudiante con presión de tiempo, operador contable revisando 80 filas, comprador comparando precios en móvil).
* **Qué contenido manda en pantalla:** (texto largo, números/tablas, fotografía, formularios, canvas interactivo).
* **Qué debe sentir el usuario en 3 segundos:** (calma y claridad, velocidad quirúrgica, calidez editorial, confianza institucional).

*Ejemplo bueno:* «Herramienta operativa diaria para soporte; prioridad a escanear tablas densas, detectar urgencias por contraste limpio y corregir registros con teclado sin decoración que robe espacio».
*Ejemplo malo (vago):* «Diseño moderno, limpio, premium y minimalista».

---

## 2. Proponer 3 direcciones visuales realmente distintas
Presenta **3 opciones contrastantes** antes de implementar. Deben diferir en **estructura y ritmo**, no solo en cambiar azul por verde:

| Dimensión | Dirección A | Dirección B | Dirección C |
| :--- | :--- | :--- | :--- |
| **Metáfora / Carácter** | Ej. Cuaderno editorial estructurado | Ej. Instrumento técnico de alta densidad | Ej. Estudio enfocado de una sola columna |
| **Composición dominante** | Asimétrica con aire y líneas divisorias | Sidebar fija + tabla/panel operativo | Flujo central sin cromado extra |
| **Tipografía y ritmo** | Display con carácter + cuerpo legible | Sans geométrica compacta + mono tabular | Sistema tipográfico sobrio de alto contraste |
| **Superficies** | Papel cálido + bordes `1px` sin tarjetas anidadas | Fondo neutro frío + elevación mínima | Alto contraste monocromo + 1 acento táctico |
| **Referencia razonada** | Qué principio concreto se adopta **y cuál se descarta** | Qué principio se adopta **y cuál se descarta** | Qué principio se adopta **y cuál se descarta** |

### Regla para analizar referencias (evitar imitación superficial)
Nunca escribas solo *"inspirado en Stripe / Linear / Apple"*. Para cada referencia explica en 2 líneas:
1. **Qué principio se extrae:** (ej. jerarquía por peso y bordes finos sin sombras pesadas; encabezados de sección alineados a la izquierda).
2. **Qué se descarta intencionalmente:** (ej. se descarta el fondo oscuro con brillos decorativos porque nuestro producto se lee en salones iluminados durante sesiones de 40 minutos).

---

## 3. Cerrar el contrato compacto (`DESIGN_DIRECTION.md`, máx. 40 líneas)
Una vez elegida la dirección con el usuario, documenta:
* **Tesis visual elegida** y motivo de descarte de las otras dos.
* **Tokens base** (tipografía, escala espacial, colores semánticos y de superficie en claro/oscuro).
* **Patrones que SÍ definen este producto** (3–5 decisiones concretas).
* **Patrones PROHIBIDOS en este proyecto** (ej. *"sin cuadrículas de 3 tarjetas con icono circular"*, *"sin gradientes neón"*, *"sin animaciones >250ms en navegación"*).
