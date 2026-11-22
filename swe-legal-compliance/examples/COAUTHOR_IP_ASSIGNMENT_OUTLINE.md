# Esquema de Acuerdo de Coautores / Cesión de PI y Guía de Contratos B2B

> **BORRADOR DE ESTRUCTURA — REQUIERE REDACCIÓN/VALIDACIÓN DE ABOGADO:** Este documento sirve para alinear las decisiones técnicas, comerciales y de titularidad antes de formalizar contratos ante abogado o notario (especialmente crítico cuando participan varios coautores/fundadores, empleados o freelancers).

---

## Parte 1 — Acuerdo de Colaboración y Titularidad entre Coautores / Equipo

### 1. Partes participantes
| Nombre completo | Rol técnico / negocio | Participación acordada (%) | Estado de firma |
| :--- | :--- | :-: | :--- |
| `[Coautor 1]` | `[Ej. Arquitectura / Backend]` | `[%]` | `[Pendiente / Firmado]` |
| `[Coautor 2]` | `[Ej. Frontend / UX]` | `[%]` | `[Pendiente / Firmado]` |
| `[Coautor 3]` | `[Ej. Seguridad / QA]` | `[%]` | `[Pendiente / Firmado]` |
| `[Coautor 4]` | `[Ej. Datos / DevOps]` | `[%]` | `[Pendiente / Firmado]` |
| `[Coautor 5]` | `[Ej. Producto / Negocio]` | `[%]` | `[Pendiente / Firmado]` |

### 2. Cláusulas clave que debe formalizar el abogado
1. **Titularidad centralizada de la Propiedad Intelectual:** definir si los derechos patrimoniales del código, diseños, documentación, marca y dominios se ceden a una **persona moral** constituida (o por constituirse) o bajo qué esquema de copropiedad se explotan, evitando bloqueos futuros si un integrante sale del proyecto.
2. **Aportaciones previas (*Background IP*):** listar librerías o herramientas creadas por cada integrante **antes** del proyecto que quedan excluidas o licenciadas al proyecto.
3. **Vesting y salida de integrantes (*Good Leaver / Bad Leaver*):** reglas claras si un coautor abandona el proyecto antes de un plazo o hito acordado (devolución de accesos, no bloqueo del repositorio, conservación de su reconocimiento moral donde proceda).
4. **Confidencialidad (NDA):** obligación de no divulgar código propietario, secretos comerciales, arquitectura interna ni datos de usuarios.
5. **Toma de decisiones y administración de activos:** quién administra cuentas de GitHub, cloud, dominios, IMPI, INDAUTOR y cuentas bancarias (preferiblemente con control dual / MFA corporativo, nunca dependiente de un correo personal único).
6. **Empleados y contratistas externos:** todo tercero que escriba código, diseño o contenido debe firmar antes de iniciar un contrato con cláusula expresa de **obra por encargo / cesión patrimonial de derechos** y NDA.

---

## Parte 2 — Registro de Propiedad Intelectual y Marca (México)
* **INDAUTOR (Derechos de autor — Programa de cómputo):** preparar código fuente representativo (primeras/últimas páginas o paquete según lineamientos vigentes), documentación descriptiva, datos de coautores y contrato de cesión/titularidad para registro de obra.
* **IMPI (Marca y aviso comercial):**
  1. Ejecutar búsqueda fonética y figurativa previa en las clases de Niza aplicables (p. ej. **Clase 9** software descargable/apps, **Clase 42** SaaS/servicios tecnológicos).
  2. Verificar disponibilidad simultánea del dominio web y usuarios en redes antes de registrar.

---

## Parte 3 — Mapa de Contratos B2B y Licenciamiento (Nivel 2–3)

| Contrato | Cuándo es obligatorio | Puntos mínimos que debe validar el abogado |
| :--- | :--- | :--- |
| **EULA** (*End User License Agreement*) | Software descargable, apps de escritorio o licencias por asiento/dispositivo | Alcance de licencia, restricciones de copia/ingeniería inversa, actualizaciones, garantías y terminación. |
| **SaaS Agreement / MSA** | Venta B2B a empresas con facturación recurrente o planes corporativos | Alcance del servicio, propiedad de datos del cliente, facturación, suspensión, limitación de responsabilidad, salida/exportación de datos (*exit clause*). |
| **NDA** (*Non-Disclosure Agreement*) | Pilotos comerciales, inversionistas, proveedores o demos con arquitectura privada | Definición de información confidencial, exclusiones, plazo de vigencia y devolución/destrucción de información. |
| **DPA** (*Data Processing Agreement*) | Cuando tratas datos personales **por cuenta de un cliente B2B** (rol de Encargado) | Instrucciones del responsable, lista de subencargados, medidas de seguridad técnicas, notificación de brechas (p. ej. 24–72 h) y devolución/borrado al terminar. |
| **SLA** (*Service Level Agreement*) | Clientes empresariales que exigen garantía de disponibilidad | Porcentaje de uptime realista (alineado a tu arquitectura real), ventanas de mantenimiento excluidas, tiempos de respuesta por severidad y créditos acotados (no penalizaciones ilimitadas). |
