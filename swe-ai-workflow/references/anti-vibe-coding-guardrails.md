# Protocolo Anti-Vibe Coding Desordenado

El *vibe coding* (pedir funciones grandes con prompts vagos y aceptar cambios sin verificar) produce rapidez aparente el día 1 y colapso de mantenimiento el día 10. Este protocolo transforma el flujo asistido por IA en ingeniería repetible sin perder velocidad.

---

## 1. Convertir prompts vagos en mini-contratos (`TASK_SPEC.md`)

Antes de escribir código frente a una instrucción abierta, tradúcela a 4 campos verificables:

| Prompt vago (vibe coding) | Mini-contrato estructurado (`TASK_SPEC.md`) |
| :--- | :--- |
| *"Haz el login"* | **Objetivo:** Endpoint `POST /api/v1/auth/login` + formulario `/login` con cookie `HttpOnly`. **Archivos:** `src/auth/login.ts`, `src/ui/LoginForm.tsx`. **Restricciones:** Sin tocar esquema de usuarios ni librerías nuevas; validar con Zod en servidor; respuestas RFC 9457. **Verificación:** `npm run typecheck && npm test -- auth.login`. |
| *"Arregla el carrito que falla"* | **Objetivo:** Corregir cálculo de subtotal con cupones en servidor (reproducido en test `cart.spec.ts`). **Archivos:** `src/cart/pricing.ts`. **Restricciones:** Recalcular siempre desde precios en BD, nunca confiar en total del cliente. **Verificación:** `npm test -- cart.spec.ts`. |
| *"Mejora el rendimiento"* | **Objetivo:** Eliminar consulta N+1 en `GET /api/v1/orders` (hoy 42 queries -> objetivo ≤ 3). **Archivos:** `src/orders/repo.ts`. **Restricciones:** Mantener contrato OpenAPI sin cambios breaking. **Verificación:** `pytest tests/test_orders_perf.py`. |

---

## 2. Regla de "Lote pequeño + Verificación obligatoria"

1. **Un lote = un cambio revisable** (idealmente 1–5 archivos, <250 líneas de diff). Nunca pidas *"construye todo el módulo completo con admin, pagos, correos y reportes de golpe"*.
2. **Puerta de salida de cada lote (sin excepciones):**
   * `lint` / formatter pasando.
   * `typecheck` / compilación sin errores ni `@ts-ignore` / `any` gratuitos.
   * Pruebas automatizadas existentes + prueba nueva del cambio pasando.
   * Revisión rápida del `git diff`: confirmar que la IA no borró validaciones, no debilitó permisos, no agregó paquetes inventados (*slopsquatting*) ni dejó secretos o `console.log` con PII.
3. **Commit atómico:** solo cuando el lote pasa verificación se hace commit (o checkpoint) y se pasa a la siguiente tarea.

---

## 3. Detección de deriva — La Regla de los 2 Intentos

El mayor quemador de tokens del *vibe coding* es el **bucle de parcheo ciego** (intento 1 falla → IA parcha síntoma → intento 2 rompe otra cosa → intento 3 inventa un workaround frágil).

**Protocolo obligatorio cuando un bug falla en 2 intentos consecutivos:**
1. **FRENAR:** no apliques un tercer parche adivinado.
2. **REVERTIR ruido:** descarta ediciones especulativas que no resolvieron el problema (`git diff` limpio sobre el estado previo).
3. **DIAGNOSTICAR causa raíz con evidencia:**
   * Reproducir con el caso mínimo posible (test aislado o comando exacto).
   * Leer el mensaje de error completo y la línea real del stack trace.
   * Verificar versiones reales en `package.json`/`pyproject.toml` y consultar documentación oficial vigente (p. ej. `Context7` si está disponible) para descartar APIs obsoletas.
4. **DOCUMENTAR en `.ai/MEMORY.md`:** anotar en la sección *"Intentos fallidos / Trampas conocidas"* qué se probó, por qué falló y cuál fue la causa raíz real. Así ningún chat futuro vuelve a caer en el mismo error.

---

## 4. Zonas protegidas que la IA nunca debe alterar sin confirmación explícita
Declaradas siempre en `CONSTITUTION.md`:
* Lógica de **precios, descuentos, totales, impuestos, cobros o saldos**.
* **Autenticación, autorización (RBAC/tenant), tokens, cookies y reglas de firewall/CORS**.
* **Migraciones destructivas** (`DROP`, borrado de columnas/tablas) o cambios de esquema en producción.
* **Instalación de dependencias nuevas** (verificar siempre que el paquete existe, está mantenido y tiene licencia compatible).
* **Borrado o relajación de tests/linters** (`skip`, desactivar reglas ESLint/Ruff) para "hacer pasar" un cambio.
