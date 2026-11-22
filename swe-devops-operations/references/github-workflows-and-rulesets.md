# Guía Completa de Flujo GitHub, Actions Hardening y Rulesets

Complemento práctico de [git-cicd-infra-observability.md](./git-cicd-infra-observability.md) para configurar repositorios GitHub de punta a punta con seguridad en cadena de suministro.

---

## 1. Elección del flujo de ramas (GitHub Flow vs. Trunk-Based vs. Git Flow)

| Estrategia | Cómo funciona | Cuándo elegirla | Estrategia de merge recomendada |
| :--- | :--- | :--- | :--- |
| **GitHub Flow *(Recomendado por defecto en Web / SaaS)*** | `main` siempre estable y desplegable. Cada cambio nace en `feat/*` o `fix/*`, abre Pull Request con CI en verde + revisión y al fusionar despliega a staging/prod. | **90 % de los proyectos web, APIs, SaaS y MVPs** con despliegue continuo y una sola versión en producción. | **Squash and merge** (título del PR en Conventional Commits = historial limpio y revertible en 1 commit). |
| **Trunk-Based Development** | Ramas muy cortas (<24–48 h) o integración diaria en `main` protegida por **feature flags** y pruebas automatizadas fuertes. | Equipos maduros con CI/CD muy rápido, pruebas robustas y necesidad de entregas diarias frecuentes. | **Squash and merge** o **Rebase and merge** (nunca commits gigantes sin dividir). |
| **Git Flow** | `main` (producción) + `develop` (integración) + `feature/*`, `release/*` y `hotfix/*`. | Productos con **múltiples versiones soportadas en paralelo**, apps móviles con ventana de revisión en tiendas o software empresarial con cortes formales por versión. | **Squash and merge** en `feature/* -> develop`; **Merge commit** en `release/* -> main` para preservar el corte y tag exacto. |

---

## 2. Hardening obligatorio en GitHub Actions

1. **Mínimo privilegio en `GITHUB_TOKEN`:** declarar siempre `permissions: contents: read` en la raíz del workflow y otorgar permisos adicionales únicamente en el `job` que los necesite (p. ej. `id-token: write` solo en el job de despliegue OIDC; `security-events: write` solo en CodeQL).
2. **Fijar acciones por commit SHA completo (40 caracteres):** nunca usar `@main`/`@master` ni depender solo de tags mutables (`@v4`) en proyectos Nivel 2–3. Escribe `uses: owner/action@<sha-40-chars> # vX.Y.Z` y activa [dependabot.yml](../examples/dependabot.yml) con `github-actions` para mantenerlos actualizados automáticamente.
   * Consultar SHA exacto de un tag oficial antes de fijarlo:
     ```bash
     gh api repos/actions/checkout/commits/v4.2.2 --jq .sha
     ```
3. **OIDC en lugar de llaves cloud estáticas:** autentica AWS, Azure, GCP o Cloudflare desde GitHub Actions usando **OpenID Connect (`id-token: write`)** con roles restringidos al repositorio y ambiente (`environment: production`), evitando `AWS_SECRET_ACCESS_KEY` o *Service Account JSON* permanentes en Secrets.
4. **Control de concurrencia (`concurrency`):**
   * En **CI (PRs):** `cancel-in-progress: true` para ahorrar minutos cuando llegan nuevos pushes al mismo PR.
   * En **CD (Staging/Producción):** `cancel-in-progress: false` para **jamás cancelar un despliegue a la mitad**.
5. **Prevención de *Script Injection*:** nunca interpoles expresiones no confiables (`${{ github.event.pull_request.title }}`, `${{ github.event.issue.body }}`) directamente dentro de `run:`. Pásalas siempre a través de variables `env:` y cítalas con comillas dobles (`"$PR_TITLE"`).

---

## 3. Configuración de GitHub Rulesets / Branch Protection (por nivel)

| Regla sobre rama `main` | Nivel 1 (MVP) | Nivel 2 (Profesional) | Nivel 3 (Empresarial) |
| :--- | :---: | :---: | :---: |
| Bloquear `push` directo a `main` y bloquear `force-push` / borrado | **Sí** | **Sí** | **Sí** |
| Exigir Pull Request + status checks en verde (`CI`, `PR Validation`) | **Sí** | **Sí** | **Sí** |
| Exigir rama actualizada antes de merge (*strict status checks*) | Opcional | **Sí** | **Sí** |
| Revisión aprobada obligatoria (`required_approving_review_count`) | 0 (solo dev) / 1 (equipo) | **≥ 1** | **≥ 2 + CODEOWNERS** |
| Descartar aprobaciones antiguas al recibir nuevos commits | Opcional | **Sí** | **Sí** |
| Exigir todas las conversaciones resueltas antes de fusionar | **Sí** | **Sí** | **Sí** |
| Eliminar rama automáticamente al fusionar (`delete_branch_on_merge`) | **Sí** | **Sí** | **Sí** |
| Exigir commits firmados (GPG / SSH) | Opcional | Recomendado | **Sí** |
| GitHub Environment `production` con aprobador manual + restricción a rama `main` | Opcional | **Sí** | **Sí** |

### Comandos reproducibles con GitHub CLI (`gh`)

Reemplaza `<OWNER>/<REPO>` y revisa los nombres exactos de tus checks antes de ejecutar:

```bash
# 1. Configurar estrategia de merge (Squash recomendado en GitHub Flow) y borrado automático de ramas
gh repo edit <OWNER>/<REPO> \
  --enable-squash-merge \
  --disable-merge-commit \
  --disable-rebase-merge \
  --delete-branch-on-merge

# 2. Aplicar Branch Protection en main (Nivel 2: PR + checks + 1 revisión + conversaciones resueltas)
#    (Para solo dev en Nivel 1, cambia required_approving_review_count a 0 y require_code_owner_reviews a false)
gh api --method PUT "repos/<OWNER>/<REPO>/branches/main/protection" \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Lint, Tests & Build",
      "Secret & Dependency Scan",
      "PR Title & Size Check"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

> **Tip para organizaciones (GitHub Rulesets):** en repositorios con múltiples ramas protegidas (`main`, `release/*`, tags `v*.*.*`), prefiere **Repository Rulesets** (`Settings -> Rules -> Rulesets`) para proteger simultáneamente ramas y tags inmutables de release (`v*.*.*`).
