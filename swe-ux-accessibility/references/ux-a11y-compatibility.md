# Diseño UX/UI, Responsive, Accesibilidad y Compatibilidad

## 1. Diseño responsive (Mobile First)

* **Mobile First:** diseñar primero para pantallas pequeñas y escalar progresivamente.
* Adaptabilidad a **móviles, tablets, laptops y monitores** grandes.
* **Breakpoints definidos** y consistentes en el Design System.
* Diseño flexible con **CSS Grid y Flexbox**.
* **Imágenes responsivas** (`srcset`, formatos **WebP / AVIF**, tamaños adaptables, relación de aspecto controlada).
* **Tipografía adaptable y fuentes propias (*self-hosted*)** para evitar bloqueos de red externos.
* **Probar en dispositivos móviles reales y redes lentas** (simulación 3G/4G), cuidando velocidad percibida.
* **Menús y navegación adaptables** a pantallas táctiles y escritorio.
* Compatibilidad con **orientación horizontal y vertical**.
* **Evitar desplazamiento horizontal no deseado.**
* **Áreas táctiles adecuadas** y espaciado suficiente entre controles.
* **Formularios adaptados a dispositivos móviles** (tipos de teclado adecuados, autocompletado).

---

## 2. UX/UI

* **Design System** y **componentes reutilizables**.
* **Consistencia visual** y **jerarquía visual** clara.
* **Estados de carga (Loading):** usar **esqueletos de carga (*skeletons*)** o indicadores claros para evitar sensación de bloqueo.
* **Listas grandes y búsquedas:** aplicar **virtualización de listas** y **retardo en búsqueda (*debounce*)** sin llamadas duplicadas.
* **Estados vacíos (Empty States)** informativos con siguiente paso claro.
* **Mensajes de error comprensibles** que indiquen qué ocurrió y cómo resolverlo.
* **Confirmaciones de acciones importantes** y **prevención de acciones destructivas accidentales**.
* **Navegación intuitiva** y **feedback visual** inmediato ante las acciones del usuario.
* **Formularios con validaciones claras** (en línea, comprensibles, sin borrar lo escrito).
* **Diseño centrado en el usuario.**
* **Observación de experiencia real (RUM y analítica ética):** medir rendimiento real en dispositivos de usuarios, detectar fricciones/abandono y recoger feedback respetando consentimiento y minimización de datos.

---

## 3. Accesibilidad (A11y)

* Cumplir **WCAG 2.2 nivel AA** como objetivo recomendado (el W3C recomienda trabajar con la versión vigente de WCAG).
* **Navegación completa por teclado** (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, flechas donde corresponda) con **orden lógico de tabulación** y sin trampas de teclado.
* **Menús desplegables y modales accesibles:** menús operables 100 % con teclado; modales con **gestión correcta de foco** (atrapar foco dentro mientras permanecen abiertos, cierre con `Escape` y restauración del foco al elemento disparador).
* **Compatibilidad con lectores de pantalla** (roles, estados y propiedades correctas).
* **Contraste adecuado** entre texto/controles y fondo.
* **Etiquetas accesibles** asociadas a cada campo (`<label>`) y botón.
* **Textos alternativos (`alt`)** significativos para imágenes informativas (y `alt=""` en decorativas).
* **No depender exclusivamente del color** para comunicar errores, estados o gráficos (acompañar con texto o icono).
* **Subtítulos / transcripciones** para contenido audiovisual.
* **Foco visible** en todo elemento interactivo.
* **Estructura semántica HTML e idioma:** usar landmarks (`header`, `nav`, `main`, `button`), jerarquía ordenada de encabezados (`h1`–`h6`) y especificar explícitamente el **idioma del documento** (`<html lang="es">` o el idioma correspondiente).
* Respeto por **`prefers-reduced-motion`** para usuarios sensibles a animaciones.
* **Tamaños de texto ajustables** (zoom hasta 200 % sin pérdida de contenido o funcionalidad).

### Referencias y herramientas de UX/A11y
* **WCAG 2.2:** https://www.w3.org/TR/wcag/
* **WAI-ARIA**
* **ISO/IEC 40500** (WCAG 2.0 como estándar ISO)
* **ISO 9241-210** (diseño centrado en las personas) e **ISO 9241-110** (principios de interacción)
* **Herramientas:** axe-core, Lighthouse.

---

## 4. Compatibilidad y estándares tecnológicos

* Compatibilidad entre **navegadores**, **dispositivos móviles**, **resoluciones** y **sistemas operativos** definidos como soportados.
* Uso de protocolos y formatos estándar (**UTF-8**, JSON, HTTP, ISO 8601).
* **Fechas y zonas horarias normalizadas** (almacenar en UTC / ISO 8601 y mostrar en zona local según corresponda).
* **Internacionalización (i18n)** y **Localización (l10n)**.
* **Gestión de idiomas** y **formatos monetarios / numéricos** locales.
* Compatibilidad con lectores de pantalla.
* Control de **versiones soportadas de frameworks** y **compatibilidad entre dependencias**.
* **Evitar tecnologías obsoletas** sin justificación documentada.

---

## 5. SEO, indexación y publicación web pública

Aplicable a sitios públicos, landing pages, SaaS con páginas de marketing y e-commerce:

* **Metadatos base:** configurar `<title>` y `<meta name="description">` únicos por página, `favicon` e iconos de plataforma, **Open Graph** (`og:title`, `og:description`, `og:image`, `og:url`) y **URLs canónicas** (`<link rel="canonical">`).
* **Control de indexación:** publicar `robots.txt` y `sitemap.xml` cuando corresponda; definir explícitamente qué páginas deben indexarse y **bloquear la indexación (`noindex` + autenticación) de paneles administrativos, rutas internas y vistas con información sensible**.
* **Privacidad en metadatos:** comprobar que títulos, descripciones, URLs y etiquetas Open Graph nunca revelen datos privados o internos.
* **Páginas de error, resiliencia y enlaces:** configurar **`ErrorBoundary` global** (o manejador equivalente para evitar pantallas en blanco ante crashes de UI), vistas dedicadas y limpias para **`400` / `403` (acceso denegado)**, **`404` (no encontrado)**, **`500` (error interno)** y **`503` (mantenimiento / servicio no disponible)** sin filtrar trazas técnicas, estado claro de **sin conexión (*offline*)** y verificación de ausencia de **enlaces rotos** antes de publicar.
* **Operación cara al usuario:** asegurar página de contacto funcional, correo/canal de soporte operativo, preguntas frecuentes (**FAQ**) cuando corresponda, información clara sobre limitaciones/precios del servicio y páginas de mantenimiento o estado del servicio cuando aplique.
