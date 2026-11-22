# Guía de Contribución (`CONTRIBUTING.md`)

¡Gracias por contribuir al proyecto! Sigue estas normas para mantener la calidad y consistencia del código.

## 1. Flujo de trabajo en Git
1. Crea una rama desde `main` (o `develop` si el proyecto usa Git Flow) con nombre descriptivo:
   - `feat/<descripcion-corta>`
   - `fix/<descripcion-corta>`
   - `docs/<descripcion-corta>`
2. Usa **Conventional Commits** en tus mensajes:
   - `feat: agrega paginación en listado de usuarios`
   - `fix: corrige validación de zona horaria en reportes`
   - `refactor: extrae servicio de autenticación`
   - `test: añade pruebas de contrato para /orders`
   - `docs: actualiza guía de despliegue`

## 2. Estándares antes de abrir un Pull Request
- [ ] El código cumple las reglas del linter y formatter configurados.
- [ ] No hay secretos, contraseñas, API keys ni datos personales reales en el diff.
- [ ] Existen pruebas unitarias/integración nuevas o actualizadas para los cambios.
- [ ] Toda la suite de pruebas y análisis estático pasan localmente.
- [ ] La documentación (`README.md`, OpenAPI, ADR si aplica) fue actualizada.

## 3. Revisión de código
- Los Pull Requests deben mantenerse pequeños y enfocados en un solo objetivo.
- Toda corrección de bug debe incluir una prueba que evite regresión.
