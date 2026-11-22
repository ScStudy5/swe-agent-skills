# Checklist Formal de Preparación Legal de Lanzamiento (`Legal Launch Readiness 0/36`)

> **Instrucciones de uso:** Marca `[x]` únicamente cuando exista evidencia verificable (documento revisado sin placeholders pendientes, control probado en staging o trámite concluido). En Nivel 1 (MVP) exige el 100 % de los ítems marcados **`N1`**; en Nivel 2 exige **`N1` + `N2`**; en Nivel 3 exige los **36/36** completos.
> **Advertencia:** Este checklist no sustituye la aprobación formal de un abogado habilitado ni de un contador público certificado.

---

## Bloque 1 — Privacidad y Datos Personales (`L-01` a `L-06`)
- [ ] **L-01 (`N1`):** Aviso de Privacidad Integral redactado conforme a LFPDPPP vigente (y GDPR/CCPA si aplica), sin placeholders y publicado en URL permanente.
- [ ] **L-02 (`N1`):** Aviso de Privacidad Simplificado visible en cada formulario de registro/captura con enlace directo al Integral.
- [ ] **L-03 (`N1`):** Separación clara entre finalidades primarias (necesarias) y secundarias (marketing/analítica/listas de espera), con consentimiento registrado, identificación del remitente, baja (*unsubscribe*) operativa y cumplimiento de reglas de canal (email/SMS/WhatsApp).
- [ ] **L-04 (`N2`):** Canal y procedimiento operativo de derechos ARCO definido (correo/formulario dedicado, verificación de identidad, folios y plazos legales).
- [ ] **L-05 (`N1`):** Política de Cookies publicada y banner de consentimiento que bloquea rastreadores no esenciales antes de aceptar.
- [ ] **L-06 (`N2`):** Inventario de terceros receptores/encargados de datos (hosting, auth, pagos, IA, analítica) documentado y consistente con el Aviso de Privacidad.

## Bloque 2 — Términos, Consumidor y E-Commerce (`L-07` a `L-12`)
- [ ] **L-07 (`N1`):** Términos y Condiciones publicados y accesibles sin requerir inicio de sesión.
- [ ] **L-08 (`N1`):** Política de Uso Aceptable (AUP) y causales claras de suspensión/terminación de cuenta incluidas.
- [ ] **L-09 (`N2`):** Transparencia total de precios finales, impuestos, moneda y restricciones antes de confirmar pago (LFPC art. 76 Bis).
- [ ] **L-10 (`N2`):** Política clara y visible de cancelaciones, devoluciones y reembolsos publicada antes de la compra.
- [ ] **L-11 (`N2`):** En suscripciones/renovaciones automáticas: aviso transparente de periodicidad/cargo y cancelación digital sencilla sin trabas (LFPC art. 76 Bis 1).
- [ ] **L-12 (`N2`):** Revisión anti-cláusulas abusivas completada y canal visible de soporte, aclaraciones y quejas con horario/tiempo de respuesta.

## Bloque 3 — Propiedad Intelectual, Marca y Equipo (`L-13` a `L-18`)
- [ ] **L-13 (`N1`):** Acuerdo de colaboración, gobierno y titularidad firmado entre todos los coautores/socios (crítico si participan 2+ integrantes).
- [ ] **L-14 (`N2`):** Contratos con cláusula escrita de cesión patrimonial de obra/software firmados por empleados y contratistas/freelancers.
- [ ] **L-15 (`N2`):** Búsqueda fonética/figurativa de marca realizada y estrategia/solicitud de registro ante IMPI (o autoridad local) iniciada.
- [ ] **L-16 (`N2`):** Expediente preparado o registro de programa de cómputo gestionado ante INDAUTOR (o autoridad equivalente).
- [ ] **L-17 (`N1`):** Auditoría de licencias OSS ejecutada confirmando compatibilidad comercial (sin copyleft incompatible sin cumplir obligaciones).
- [ ] **L-18 (`N2`):** Licencias verificadas de fuentes tipográficas, iconos, imágenes, datasets y términos comerciales de modelos de IA.

## Bloque 4 — Contratos B2B y Terceros (`L-19` a `L-24`)
- [ ] **L-19 (`N2`):** EULA o SaaS Agreement / MSA base preparado (si comercializa software licenciado o B2B).
- [ ] **L-20 (`N2`):** Acuerdo de Confidencialidad (NDA) estándar disponible para socios, clientes piloto o proveedores.
- [ ] **L-21 (`N3`):** Data Processing Agreement (DPA) disponible para clientes B2B y revisado con proveedores subencargados críticos.
- [ ] **L-22 (`N3`):** SLA comercial alineado a métricas reales de disponibilidad, RTO/RPO y capacidad de soporte del equipo.
- [ ] **L-23 (`N2`):** Términos comerciales y políticas de no-entrenamiento/retención verificados en APIs externas y proveedores LLM/IA.
- [ ] **L-24 (`N3`):** Cláusulas de limitación de responsabilidad, indemnización y seguros revisadas por abogado corporativo.

## Bloque 5 — Controles Técnico-Legales y Evidencia en Software (`L-25` a `L-30`)
- [ ] **L-25 (`N1`):** Casillas de aceptación y consentimiento granular sin preselección (`checked=false` por defecto) en toda la interfaz.
- [ ] **L-26 (`N1`):** Registro inmutable en servidor de aceptación legal (usuario, versión del documento, hash `SHA-256`, timestamp UTC y canal).
- [ ] **L-27 (`N3`):** Conservación de mensajes de datos con constancia **NOM-151-SCFI-2016** (PSC acreditado) integrada donde se requiera valor probatorio reforzado.
- [ ] **L-28 (`N2`):** Centro de Privacidad funcional en la aplicación (gestión de preferencias y solicitud de derechos ARCO).
- [ ] **L-29 (`N2`):** Flujo funcional y probado de exportación de datos y eliminación/anonimización de cuenta respetando retenciones legales.
- [ ] **L-30 (`N2`):** Control de edad (y consentimiento parental verificable + privacidad máxima si admite menores) implementado y validado.

## Bloque 6 — Fiscal, Operativo y Gobernanza Legal (`L-31` a `L-36`)
- [ ] **L-31 (`N2`):** Entidad fiscal definida (alta en RFC y régimen tributario correcto en SAT o autoridad local) antes de emitir cobros reales.
- [ ] **L-32 (`N2`):** Flujo de facturación electrónica (CFDI 4.0) y cálculo de IVA/impuestos digitales validado por contador público.
- [ ] **L-33 (`N2`):** Procesamiento de pagos delegado a pasarela regulada/certificada PCI-DSS (sin almacenar datos crudos de tarjetas).
- [ ] **L-34 (`N2`):** Sistema de versionado de documentos legales, historial público y procedimiento de notificación/re-aceptación ante cambios sustanciales.
- [ ] **L-35 (`N2`):** Revisión de brechas regulatorias sectoriales completada (`swe-domain-discovery`) confirmando ausencia de licencias obligatorias pendientes.
- [ ] **L-36 (`N2`):** Visto bueno final de abogado habilitado sobre el paquete legal completo antes del lanzamiento comercial en producción.
