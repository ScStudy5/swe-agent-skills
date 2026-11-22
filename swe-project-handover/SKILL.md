---
name: swe-project-handover
description: >-
  Orquestador integral de Software Project Handover, Transferencia de
  Conocimiento y Documentación Viva: genera, audita y cierra un paquete unificado
  PROJECT-HANDOVER/ (00-START-HERE a 17-APPENDICES + política de documentación viva)
  cubriendo contexto ejecutivo, guía de código, memoria histórica/deuda técnica,
  licencias/PI, manuales diferenciados, inventario de activos, transferencia y
  revocación de accesos, sesiones supervisadas y acta de aceptación formal. Usar al
  preparar la entrega formal de un proyecto, onboarding completo de sucesores o
  auditar la completitud documental (para plantillas sueltas en desarrollo diario
  usar swe-methodology).
---

# Project Handover, Transferencia de Conocimiento y Documentación Viva

Aplica esta skill cuando necesites generar, completar, auditar o cerrar un paquete formal de entrega de software (`PROJECT-HANDOVER/`) para que un equipo o desarrollador sucesor pueda operar, mantener y evolucionar el sistema **sin depender del autor original**.

## Reglas fundamentales
1. **Cero secretos ni PII en el paquete documental:** nunca incluyas contraseñas, API keys, certificados privados, archivos `.env` reales ni datos personales de producción dentro de `PROJECT-HANDOVER/`. Documenta exclusivamente la **ubicación en el gestor de secretos** (bóveda/servicio) y el procedimiento de rotación y revocación.
2. **Transparencia radical (cero documentación cosmética):** documenta lo que el sistema **realmente es hoy** —incluyendo bugs conocidos, deuda técnica, riesgos y preguntas abiertas— basándote en el código y configuración reales del repositorio, nunca inventando arquitectura o métricas inexistentes.
3. **Aplicación proporcional por nivel:** antes de generar o auditar el paquete, confirma el nivel del proyecto (`1. MVP` / `2. Profesional` / `3. Empresarial`) si el usuario no lo indicó:
   * **Nivel 1 — MVP:** paquete compacto enfocado en continuidad técnica inmediata (índice, setup local, arquitectura básica, configuración, issues conocidos, inventario de cuentas y acta ligera).
   * **Nivel 2 — Profesional (SaaS / Producción):** paquete completo de operación y soporte (guía de código, BD/backups, APIs, seguridad/privacidad, QA, CI/CD/FinOps, licencias, manuales diferenciados, transferencia de accesos y sesiones supervisadas).
   * **Nivel 3 — Empresarial / Regulado:** las 18 dimensiones completas (`00-START-HERE` a `17-APPENDICES`), evidencia formal de cumplimiento, matriz de PI/cesión, simulacros de incidentes, firma formal de aceptación y política estricta de documentación viva.

## Flujo de trabajo

### Modo A — Crear o completar el paquete `PROJECT-HANDOVER/`
1. **Descubrimiento previo del repositorio:** si existe código fuente, inspecciona el repo (idealmente ejecutando primero `repo_audit_scan.py` de `swe-methodology` o leyendo manifiestos, rutas, CI, BD y docs existentes) para poblar el handover con hechos verificados y evitar duplicar docs que ya existen (enlázalos o consolídalos).
2. **Consultar el plano de 18 puntos y calibrar por nivel:** revisa la matriz completa de carpetas, documentos y obligatoriedad por nivel en [handover-blueprint-18.md](./references/handover-blueprint-18.md).
3. **Generar el andamiaje con el script (opcional y seguro):** usa [handover_scaffold.py](./scripts/handover_scaffold.py) desde la ruta resuelta de esta skill (previsualiza primero con `--dry-run`):
   ```bash
   # Previsualizar qué archivos se crearán (sin escribir en disco)
   python3 <ruta-de-la-skill>/scripts/handover_scaffold.py init <ruta-del-repo>/PROJECT-HANDOVER --level 2 --dry-run

   # Crear la estructura base sin sobrescribir documentos existentes
   python3 <ruta-de-la-skill>/scripts/handover_scaffold.py init <ruta-del-repo>/PROJECT-HANDOVER --level 2
   ```
   *(En Windows usa `python` en lugar de `python3`.)*
4. **Redactar cada bloque con las plantillas base y skills especializadas:**
   * Índice maestro de orientación por rol (`00-START-HERE/INDEX.md`) -> [00-INDEX.md](./examples/00-INDEX.md)
   * Guía de código para sucesores (`04-CODEBASE-GUIDE/`) -> [CODEBASE_GUIDE.md](./examples/CODEBASE_GUIDE.md)
   * Memoria histórica, bugs, deuda y riesgos (`11-HISTORY-AND-KNOWN-ISSUES/`) -> [KNOWN_ISSUES_AND_DEBT.md](./examples/KNOWN_ISSUES_AND_DEBT.md)
   * Inventario, transferencia de propiedad y revocación de accesos (`14` y `15`) -> [ACCESS_TRANSFER_AND_REVOCATION.md](./examples/ACCESS_TRANSFER_AND_REVOCATION.md)
   * Checklist y acta de aceptación formal (`16-HANDOVER-ACCEPTANCE/`) -> [HANDOVER_ACCEPTANCE_ACTA.md](./examples/HANDOVER_ACCEPTANCE_ACTA.md)
   * Reutiliza o invoca las skills especializadas `swe-*` cuando falte contenido técnico profundo de dominio (`domain-discovery`), arquitectura (`architecture-design`), datos/APIs (`data-apis`), seguridad (`security-privacy`), QA (`qa-testing`), UX (`ux-accessibility`), DevOps (`devops-operations`) o IA (`ai-engineering`).
5. **Integrar la Regla 18 (Documentación Viva):** incluye `17-APPENDICES/LIVING_DOCUMENTATION_POLICY.md` y enlaza las reglas de actualización obligatoria en PRs y releases siguiendo [living-documentation-standard.md](./references/living-documentation-standard.md).

### Modo B — Auditar un paquete de Handover existente
1. Ejecuta el escaneo de solo lectura con [handover_scaffold.py](./scripts/handover_scaffold.py):
   ```bash
   python3 <ruta-de-la-skill>/scripts/handover_scaffold.py audit <ruta-del-repo>/PROJECT-HANDOVER --level 2
   ```
   *(Agrega `--format json` para salida estructurada. Códigos de salida: `0` sin bloqueadores de seguridad, `1` error de argumentos, `2` **bloqueador crítico**: se detectó un archivo `.env` o posible secreto dentro del handover).*
2. Revisa completitud por sección, placeholders pendientes (`[TODO]`, `[PENDIENTE]`, `[...]`), desactualización respecto al código real y ausencias críticas para el sucesor.
3. Entrega un informe priorizado en **Crítico (bloqueante para entrega)**, **Importante (antes del cierre)** y **Recomendado (mejora continua)**.

### Modo C — Ejecutar la transferencia formal y cierre (Puntos 14, 15 y 16)
Sigue el protocolo operativo paso a paso de [transfer-and-acceptance-protocol.md](./references/transfer-and-acceptance-protocol.md):
1. Completar el **Inventario de activos entregables** (repos, cloud, dominios, DNS, certificados, SaaS, diseño, tableros).
2. Ejecutar la **Transferencia de propiedad y accesos** + rotación de secretos + **revocación verificada** del equipo saliente.
3. Realizar y registrar las **Sesiones supervisadas** (instalación desde cero por el sucesor, despliegue controlado en staging/prod y simulación de incidente + rollback).
4. Completar el **Checklist de Aceptación** y generar el **Acta de Entrega (`HANDOVER_SIGN_OFF_ACTA.md`)** con firmas, fechas y pendientes acordados.

## Criterios de verificación
* El paquete `PROJECT-HANDOVER/` contiene todas las secciones obligatorias para el nivel elegido y ningún documento crítico queda con placeholders sin resolver.
* El escaneo `handover_scaffold.py audit` confirma **0 archivos `.env`** y **0 secretos hardcodeados** dentro de la documentación.
* Toda información técnica escrita en el handover coincide con archivos, rutas, scripts y configuración reales del repositorio (sin datos inventados).
* Existe una regla explícita de **Documentación Viva** (Regla 18) vinculada al flujo de PRs/releases para evitar obsolescencia posterior.
