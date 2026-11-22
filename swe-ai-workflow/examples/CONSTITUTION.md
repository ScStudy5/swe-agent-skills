# CONSTITUTION — Reglas Innegociables de [Nombre del Proyecto]

> Archivo corto de reglas permanentes para humanos y agentes de IA. **Mantener ≤ 80 líneas.**

## 1. Stack exacto y versión objetivo
- **Lenguaje / Runtime:** `[Ej. TypeScript 5.x / Node 22 | Python 3.12]`
- **Framework / UI:** `[Ej. Next.js 15 / React 19 | FastAPI]`
- **Base de datos / ORM:** `[Ej. PostgreSQL 16 + Prisma / SQLAlchemy]`
- **Nivel del proyecto:** `[Nivel 1: MVP | Nivel 2: Profesional | Nivel 3: Empresarial]`

## 2. Arquitectura permitida (límites duros)
- Separación estricta: lógica de negocio en dominio/servicios; nunca mezclar SQL o reglas críticas dentro de vistas UI o controladores HTTP.
- Toda entrada externa se valida en el servidor (nunca confiar en validaciones solo de cliente).
- Errores de API siguen formato estándar (RFC 9457) sin filtrar *stack traces* ni mensajes de BD.

## 3. Zonas protegidas (la IA NO modifica sin permiso explícito humano)
- Cálculo de **precios, totales, descuentos, impuestos, saldos y cobros** (siempre en servidor).
- **Autenticación, autorización (RBAC/tenant), sesiones, cookies y CORS/headers de seguridad**.
- **Migraciones destructivas** de base de datos o cambios en archivos `.env` / secretos / CI de despliegue.
- **Dependencias nuevas:** prohibido instalar paquetes sin verificar existencia oficial, necesidad real y licencia.
- **Tests y linters:** prohibido saltar tests (`skip`), relajar aserciones o desactivar reglas de lint para "hacer pasar" un cambio.

## 4. Protocolo de trabajo obligatorio para la IA
1. Si la petición es ambigua o afecta >2 archivos: presentar primero un **plan de 3–5 líneas** y esperar confirmación.
2. Trabajar en **lotes pequeños** (<250 líneas de diff) y verificar cada lote con `lint` + `typecheck` + `test`.
3. **Regla de 2 intentos:** si un bug no se resuelve en 2 intentos, frenar el parcheo ciego, analizar causa raíz y registrar lo que falló en `.ai/MEMORY.md`.
4. **Lectura selectiva:** buscar con `rg`/grep y leer solo rangos de líneas relevantes; nunca volcar archivos o logs masivos innecesariamente.
5. **Cero secretos ni PII real** en código, logs, tests, prompts o archivos `.ai/`.
