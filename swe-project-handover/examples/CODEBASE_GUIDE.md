# Guía del Código Fuente para Sucesores (`CODEBASE_GUIDE.md`)

- **Última actualización:** `[YYYY-MM-DD]`
- **Commit de referencia:** `[<git-sha>]`
- **Responsable:** `[Rol / Equipo]`

---

## 1. Mapa de directorios del repositorio
```text
.
├── src/                # [Descripción real de la estructura del proyecto]
│   ├── api/            # [Rutas HTTP / controladores]
│   ├── domain/         # [Reglas de negocio puras]
│   ├── infrastructure/ # [BD, colas, clientes externos]
│   └── ui/             # [Componentes y vistas]
├── tests/              # [Unit, integration, E2E]
├── docs/adr/           # [Registros de decisiones arquitectónicas]
└── PROJECT-HANDOVER/   # [Este paquete de transferencia]
```

## 2. Puntos de entrada y ciclo de vida de una solicitud
* **Bootstrap / arranque:** `[Ej. src/main.ts -> inicializa config, logger, BD y servidor HTTP]`
* **Jobs / Workers / Cron:** `[Ej. src/workers/billing-sync.ts — corre cada 15 min]`
* **Flujo típico de una petición:**
  1. Middleware de `Correlation-ID`, CORS, Rate Limiting y Autenticación (`[ruta-archivo]`).
  2. Validación de DTO / esquema (`[ruta-archivo]`).
  3. Caso de uso / servicio de dominio (`[ruta-archivo]`).
  4. Repositorio / transacción de BD (`[ruta-archivo]`).
  5. Serialización de respuesta o error estándar RFC 9457 (`[ruta-archivo]`).

## 3. Mapa de módulos (`MODULES.md` resumen)
| Módulo | Ruta | Responsabilidad | Dependencias críticas | Nivel de fragilidad |
| :--- | :--- | :--- | :--- | :--- |
| `[Auth]` | `[src/auth/]` | `[Login, JWT/sesiones, RBAC]` | `[Proveedor OIDC / BD]` | `[Alto — cambios afectan todo]` |
| `[Billing]` | `[src/billing/]` | `[Webhooks, suscripciones, idempotencia]` | `[Pasarela de pagos]` | `[Alto — revisar tests antes de tocar]` |

## 4. Referencia de configuración (`CONFIGURATION_REFERENCE.md` resumen)
> **Nunca escribas valores reales aquí.** Referencia únicamente nombres y ubicación en bóveda.

| Variable | Obligatoria | Ejemplo no sensible / Default | Ambientes | Qué controla | Ubicación del secreto |
| :--- | :-: | :--- | :--- | :--- | :--- |
| `DATABASE_URL` | Sí | `postgresql://app:local@127.0.0.1:5432/db` | Todos | Conexión principal a BD | `[Vault/Prod/DB]` |
| `LOG_LEVEL` | No | `info` | Todos | Verbosidad de logs | No es secreto |

## 5. Catálogo de errores frecuentes (`ERROR_CATALOG.md` resumen)
| Código interno | HTTP | Causa habitual | Diagnóstico / Acción rápida |
| :--- | :-: | :--- | :--- |
| `ERR_AUTH_TOKEN_EXPIRED` | `401` | Token expirado o reloj desincronizado | Verificar renovación de sesión y reloj NTP |
| `ERR_IDEMPOTENCY_CONFLICT` | `409` | Reintento duplicado con misma clave | Inspeccionar payload original por `correlationId` |

## 6. Trampas conocidas y consejos para el día 1
* `[Ej. No modificar el orden de los middlewares en src/app.ts porque el webhook de pagos requiere raw body antes del parser JSON.]`
* `[Ej. Ejecutar siempre migraciones con el script npm run db:migrate, nunca editando tablas manualmente.]`
