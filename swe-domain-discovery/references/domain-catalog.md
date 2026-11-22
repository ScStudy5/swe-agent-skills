# Mapa Base de Dominios e Industrias

Referencia inicial para detectar brechas que las skills generales no cubren. **Siempre complementa esta tabla investigando la legislación vigente del país donde operará el proyecto.**

---

## 1. Fintech, Banca pequeña, Wallets y Pagos
* **Qué cubrir en código/arquitectura:**
  * **Contabilidad de partida doble (*Double-Entry Ledger*):** nunca actualizar saldos con un simple `balance = balance - x`; registrar asientos inmutables (débito/crédito), trazabilidad completa y procesos de **conciliación** automática.
  * **Idempotencia y bloqueo transaccional:** claves de idempotencia en transferencias/pagos, transacciones ACID y prevención estricta de condiciones de carrera (doble gasto).
  * **Flujos de KYC / KYB y prevención de fraude:** captura verificable de identidad, límites por nivel de cuenta, detección de anomalías, listas de control/bloqueo y auditoría inmutable de operaciones.
  * **Integración con infraestructura regulada:** delegar tarjetas a pasarelas certificadas (**PCI-DSS** como Stripe/Adyen/Openpay) o usar **BaaS** (*Banking-as-a-Service*) / agregadores autorizados para reducir el alcance regulatorio.
* **Qué investigar según país y gestión externa:**
  * Licencias/autorizaciones financieras locales (ej. México: CNBV, Ley Fintech, Banxico/SPEI, PLD/FT; EE. UU./UE: licencias de transmisor de dinero, PSD2, etc.).
  * Nivel de cumplimiento **PCI-DSS**, auditorías de cumplimiento y pruebas de penetración periódicas por terceros independientes.

---

## 2. Sector Salud (Telemedicina, Expediente Clínico, Wellness/Diagnóstico)
* **Qué cubrir en código/arquitectura:**
  * **Historial clínico con integridad e inmutabilidad:** notas firmadas/selladas con fecha y autor; las correcciones se agregan como enmiendas (*append-only*), sin sobrescribir ni borrar registros clínicos históricos.
  * **Control de acceso basado en relación clínica:** además de RBAC, verificar relación médico-paciente y consentimiento explícito, con registro de cada lectura (*audit trail* de accesos a PII/PHI).
  * **Interoperabilidad clínica:** estándares **HL7 / FHIR**, **DICOM** (imágenes) y catálogos médicos estándar (CIE-10/CIE-11) cuando intercambie datos con clínicas/laboratorios.
  * **Si usa IA:** *Human-in-the-loop* obligatorio; nunca presentar salidas automatizadas como diagnóstico médico definitivo sin validación clínica.
* **Qué investigar según país y gestión externa:**
  * Regulación sanitaria y de expediente clínico (ej. México: **NOM-024-SSA3**, datos sensibles en LFPDPPP; EE. UU.: **HIPAA/HITECH** y BAA con proveedores cloud; UE: GDPR Art. 9).
  * Clasificación como **Software como Dispositivo Médico (SaMD)** si realiza triaje, diagnóstico o dosificación (COFEPRIS, FDA, MDR).
  * Tiempos mínimos legales de retención de expedientes clínicos.

---

## 3. Sector Gubernamental y Trámites Públicos
* **Qué cubrir en código/arquitectura:**
  * **Accesibilidad obligatoria:** cumplimiento estricto y auditable de **WCAG 2.2 AA** (o estándar oficial local).
  * **Validez documental y trazabilidad:** soporte para **firma electrónica avanzada**, sellado de tiempo, foliado único, bitácoras inmutables de funcionarios/ciudadanos y preservación digital a largo plazo.
  * **Portabilidad y estándares abiertos:** evitar *Vendor Lock-in* y exponer datos/formatos abiertos e interoperables.
* **Qué investigar según país y gestión externa:**
  * Firma electrónica oficial y conservación documental (ej. México: **e.firma / FIEL**, **NOM-151**; UE: **eIDAS**).
  * Requisitos de **soberanía y residencia de datos** (ubicación física de servidores y respaldos).
  * Marcos normativos públicos de seguridad de la información, licitaciones y auditorías certificadas.

---

## 4. Videojuegos y Plataformas Tiempo Real
* **Qué cubrir en código/arquitectura:**
  * **Arquitectura autoritativa en servidor (*Anti-cheat*):** nunca confiar en el cliente para física, daño, inventario o moneda virtual; validar reglas críticas en servidor.
  * **Sincronización y red:** manejo de latencia, interpolación/predicción, protección contra desconexiones y límites contra DDoS / spam de paquetes.
  * **Economía virtual e integridad:** transacciones atómicas en compras/intercambios de inventario para evitar duplicación de ítems (*duping*).
  * **Seguridad comunitaria y menores:** moderación/reporte de abuso, filtros, privacidad en chat/voz y control parental si aplica.
* **Qué investigar según plataforma y región:**
  * Clasificación por edad (**ESRB**, **PEGI**, etc.), reglas sobre *loot boxes* / compras dentro de la app y políticas técnicas de publicación (Steam, Play Store, App Store, consolas).

---

## 5. E-commerce, Marketplaces y Suscripciones
* **Qué cubrir en código/arquitectura:**
  * **Separación de inventario, órdenes y pagos:** manejo atómico de stock (reservas temporales, prevención de sobreventa), máquina de estados de órdenes e idempotencia en webhooks de pago.
  * **Facturación, impuestos y devoluciones:** cálculo preciso en centavos/enteros (nunca `float` para dinero), notas de crédito/reembolsos e historial de precios al momento de compra.
* **Qué investigar según país:**
  * Normativa fiscal/facturación electrónica local (ej. CFDI en México), derechos del consumidor, cancelaciones/reembolsos y prevención de contracargos.

---

## 6. EdTech / Plataformas con Menores de Edad
* **Qué cubrir en código/arquitectura:**
  * **Consentimiento parental verificable**, privacidad máxima por defecto (perfiles privados, cero seguimiento publicitario invasivo) y moderación estricta en interacciones entre usuarios.
* **Qué investigar según país:**
  * Leyes de protección infantil en línea (**COPPA** en EE. UU., **GDPR-K** en UE, normativa local de protección de datos de menores).

---

## 7. IoT y Dispositivos Conectados
* **Qué cubrir en código/arquitectura:**
  * **Identidad criptográfica por dispositivo**, comunicación mutua cifrada (mTLS), colas/telemetría tolerante a reconexiones y mecanismo de actualizaciones **OTA firmadas con rollback** automático si falla el arranque.
* **Qué investigar:**
  * Certificaciones de radiofrecuencia/seguridad física y normativas de ciberseguridad IoT del mercado destino.
