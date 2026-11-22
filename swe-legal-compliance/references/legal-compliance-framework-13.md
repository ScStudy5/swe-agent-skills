# Marco de Cumplimiento Legal y Regulatorio — 13 Pilares (LCS)

> **Advertencia legal obligatoria:** Este marco es una guía técnico-operativa de cumplimiento para equipos de software. **No constituye asesoría legal ni contable oficial.** Toda redacción final, registro o estrategia fiscal debe ser revisada por un abogado habilitado y un contador público en la jurisdicción aplicable.

---

## Matriz de los 13 pilares por nivel de proyecto

Leyenda: **O** = Obligatorio · **R** = Recomendado / Condicional (según modelo de negocio) · **—** = Opcional en este nivel.

| # | Pilar LCS | Alcance principal | N1 (MVP) | N2 (Prof.) | N3 (Empr.) |
| :-: | :--- | :--- | :-: | :-: | :-: |
| `01` | **Jurisdicción, titularidad y riesgo** | Definir entidad responsable (persona física/moral/coautores), país de operación, mercados destino y si hay regulación vertical (`swe-domain-discovery`). | **O** | **O** | **O** |
| `02` | **Privacidad y Protección de Datos** | Aviso de Privacidad Integral y Simplificado conforme a **LFPDPPP vigente** en México (y GDPR/CCPA si hay usuarios en UE/EE. UU.), finalidades primarias vs. secundarias, transferencias y derechos **ARCO**. | **O** | **O** | **O** |
| `03` | **Términos y Condiciones + AUP** | Reglas de uso del servicio, Política de Uso Aceptable (*Acceptable Use Policy*), suspensión de cuentas, contenido generado por usuarios, propiedad intelectual y jurisdicción. | **O** | **O** | **O** |
| `04` | **Política de Cookies y Rastreo** | Clasificación de cookies (estrictamente necesarias, analíticas, preferencias, marketing), consentimiento granular previo y mecanismo de revocación. | **O** | **O** | **O** |
| `05` | **Comercio Electrónico y Consumidor (PROFECO / LFPC)** | Cumplimiento de **LFPC arts. 76 Bis y 76 Bis 1** en México: precios totales con impuestos, información veraz, políticas claras de cancelación/devolución/reembolso, transparencia y cancelación sencilla en renovaciones automáticas y prevención de cláusulas abusivas. | R *(si cobra)* | **O** | **O** |
| `06` | **Soporte, SLA y Atención a Quejas** | Canales de soporte visibles, tiempos de respuesta realistas, gestión de aclaraciones/reclamaciones y acuerdos de nivel de servicio (**SLA**) coherentes con la operación real. | R | **O** | **O** |
| `07` | **Propiedad Intelectual y Marca (INDAUTOR / IMPI)** | Registro de programa de cómputo ante **INDAUTOR**, búsqueda fonética y registro de marca/signo distintivo ante **IMPI**, titularidad de dominios y verificación de licencias OSS/activos. | R *(verificar marca)* | **O** | **O** |
| `08` | **Acuerdos de Equipo y Coautores** | Acuerdo de colaboración, gobierno y **cesión de derechos patrimoniales** entre coautores/socios (crítico en equipos de 2+ fundadores), empleados y freelancers + **NDA**. | **O** *(si hay >1 autor)* | **O** | **O** |
| `09` | **Contratos B2B y Licenciamiento** | **EULA**, **SaaS Agreement / MSA**, **DPA** (*Data Processing Agreement* / contrato con encargados del tratamiento), **SLA** comercial y revisión de términos de APIs/proveedores de IA. | — | R *(si es B2B)* | **O** |
| `10` | **Controles Técnico-Legales en Software** | Centro de Privacidad, flujo ARCO trazable, exportación y eliminación/anonimización de cuenta, consentimiento granular sin casillas premarcadas y control de edad (ver [tech-legal-controls-in-software.md](./tech-legal-controls-in-software.md)). | **O** *(básico)* | **O** | **O** |
| `11` | **Evidencia Electrónica (NOM-151)** | Registro inmutable de aceptación de términos y privacidad (`versión`, `SHA-256`, `timestamp UTC`, evidencia técnica) y constancia de conservación **NOM-151-SCFI-2016** mediante PSC autorizado cuando se requiera valor probatorio reforzado. | **O** *(log básico)* | **O** *(log + hash)* | **O** *(NOM-151 PSC)* |
| `12` | **Obligaciones Fiscales (SAT / CFDI / IVA)** | Alta en **RFC** y régimen fiscal adecuado, facturación electrónica **CFDI 4.0**, cálculo y entero de **IVA** / impuestos digitales, retenciones e integración con pasarelas reguladas (validar con contador público). | R *(antes de cobrar)* | **O** | **O** |
| `13` | **Lanzamiento y Mantenimiento Legal (0/36)** | Auditoría formal `Legal Launch Readiness (0/36)`, versionado semántico de documentos legales, notificación de cambios sustanciales y re-aceptación registrada. | **O** *(subconjunto N1)* | **O** | **O** |

---

## Notas clave de jurisdicción (México — verificar vigencia antes de publicar)

1. **Protección de Datos Personales (LFPDPPP):**
   * En México aplica la **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)**. *Nota de verificación:* debido a las reformas constitucionales y legales recientes sobre la autoridad garante federal (transición de funciones del extinto INAI hacia la Secretaría Anticorrupción y Buen Gobierno), **verifica siempre la autoridad vigente y los plazos exactos** antes de publicar el Aviso de Privacidad definitivo.
   * Diferencia obligatoriamente entre **Aviso de Privacidad Integral** (documento completo disponible permanentemente) y **Aviso de Privacidad Simplificado** (resumen en cada formulario/pantalla de captura con enlace directo al integral).
   * Separa siempre **finalidades primarias** (necesarias para el servicio) de **finalidades secundarias** (mercadotecnia, publicidad, perfilamiento) ofreciendo un mecanismo sencillo de negativa sin condicionar el servicio.
2. **Protección al Consumidor en Comercio Electrónico (PROFECO / LFPC):**
   * **Art. 76 Bis LFPC:** exige confidencialidad, seguridad técnica en transacciones, domicilio físico/teléfono/medios de aclaración claros, precios totales con impuestos y restricciones transparentes antes de concretar el pago.
   * **Art. 76 Bis 1 LFPC (cobros recurrentes y suscripciones):** informar de forma clara y destacada la periodicidad, monto y fecha de cobro, notificar antes de renovaciones automáticas cuando corresponda y habilitar un mecanismo de **cancelación inmediato y sin trabas** por el mismo medio de contratación.
   * Evitar **cláusulas abusivas** (renuncia total a garantías legales, modificaciones unilaterales retroactivas de precio sin aviso ni salida, arbitraje forzoso desproporcionado contra consumidores).
3. **Propiedad Intelectual (INDAUTOR e IMPI):**
   * **INDAUTOR:** el registro de programa de cómputo otorga presunción de autoría y fecha cierta (no sustituye los contratos escritos de cesión patrimonial cuando participan varios coautores o contratistas).
   * **IMPI:** realizar búsqueda fonética y figurativa previa en la clase de Niza correspondiente (p. ej. clase 9 software descargable, clase 42 SaaS/tecnología) antes de invertir en dominio y marca comercial.
4. **Evidencia Electrónica (NOM-151-SCFI-2016):**
   * Para contratos electrónicos, pagarés, aceptación de contratos B2B o pruebas ante disputas, considerar la emisión de constancias de conservación de mensajes de datos con un **Prestador de Servicios de Certificación (PSC)** acreditado bajo **NOM-151-SCFI-2016**.
5. **Alcance Internacional (si el producto atiende usuarios fuera de México):**
   * **Unión Europea / EEE:** **GDPR** (base jurídica explícita Art. 6, derecho al olvido y portabilidad, representante/DPO si aplica, cláusulas contractuales tipo para transferencias internacionales).
   * **California / EE. UU.:** **CCPA/CPRA** (*Do Not Sell or Share My Personal Information*, avisos en punto de recolección).
   * **Menores de edad:** **COPPA** (EE. UU., <13 años), **GDPR-K** (UE, 13–16 años) y protección reforzada del interés superior de la niñez en México.
