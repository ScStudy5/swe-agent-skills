# Plantilla base Dockerfile multi-stage y no-root
# Adapta la imagen base y comandos al lenguaje del proyecto (Node, Python, .NET, Go, etc.).

# --- Etapa 1: Build ---
FROM node:22-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- Etapa 2: Runtime mínimo ---
FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Usuario no-root para reducir superficie de ataque
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder --chown=appuser:appgroup /app/package.json /app/package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force && chown -R appuser:appgroup /app/node_modules

COPY --from=builder --chown=appuser:appgroup /app/dist ./dist

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1

CMD ["node", "dist/main.js"]
