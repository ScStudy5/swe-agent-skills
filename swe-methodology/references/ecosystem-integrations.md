# Integración del Ecosistema y Extensiones Opcionales

Las 13 skills `swe-*` forman una base completa y autocontenida. Cuando el entorno tenga herramientas o skills adicionales instaladas, sigue estas reglas para potenciar la calidad **sin generar conflictos ni sobrecargar el contexto**.

---

## 1. Documentación viva y diseño moderno (Prioritarios si están disponibles)

| Herramienta / Skill | Cuándo usarla | Qué aporta | Si NO está instalada |
| :--- | :--- | :--- | :--- |
| **`modern-web-guidance`** | **Antes** de diseñar o modificar UI web (HTML, CSS, formularios, modales, animaciones, CWV, sanitización) | Patrones web modernos actuales y evita diseños genéricos o CSS/APIs obsoletas | Aplicar las reglas de `swe-ux-accessibility` |
| **`Context7` (`context7-mcp`)** | **Antes** de generar código que dependa de frameworks o librerías (React, Next.js, Tailwind, Prisma, Supabase, FastAPI, etc.) | Consulta documentación oficial exacta de la versión actual del proyecto | Verificar versiones en `package.json`/`pyproject.toml` y documentación oficial |

---

## 2. Packs y skills externas opcionales (Solo bajo demanda)

**Regla anti-conflicto:** nunca actives múltiples packs generales al mismo tiempo para tareas básicas (por ejemplo, mezclar reglas de planificación/PRs de varios repos distintos genera instrucciones contradictorias). Úsalos solo de forma puntual:

| Recurso externo | Cuándo conviene activarlo | Precaución |
| :--- | :--- | :--- |
| **Matt Pocock’s Skills** | Proyectos complejos en **TypeScript / JavaScript** que requieran planificación, TDD estricto o refactoring avanzado | Usar únicamente la parte de diseño/TDD puntual; no duplicar la metodología general |
| **Cloudflare Security Audit Skill** | Proyectos desplegados en **Cloudflare** (Workers, Pages, Turnstile, WAF) durante una auditoría profunda | No activar en cambios pequeños; usar solo para auditoría o configuración de Cloudflare |
| **ECC (Everything Claude Code)** | Solo si el usuario eligió explícitamente un perfil puntual compatible | Revisar siempre permisos, *hooks* y MCPs; evitar instalarlo por múltiples métodos a la vez |
| **Playbooks externos de OWASP / OWASP ZAP** | Auditorías **Nivel 2–3** o pruebas DAST exhaustivas en `staging` | Complementar con `swe-browser-audit` y `swe-security-privacy` sin duplicar checklists |

---

## 3. Regla de respaldo (Portabilidad entre Codex, Antigravity, Claude Code y OpenCode)
* Verifica primero si la herramienta/skill externa existe en el entorno actual antes de delegar en ella.
* Si no existe, continúa de forma autónoma usando las skills `swe-*` sin interrumpir el trabajo.
