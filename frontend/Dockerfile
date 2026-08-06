# ========================================
#  Production — 构建静态文件到 alpine 镜像
# ========================================
FROM node:22-alpine AS build

WORKDIR /app

ARG VITE_API_BASE_URL=http://localhost/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npx vite build

FROM alpine:3.20 AS production
COPY --from=build /app/dist /app/dist


# ========================================
#  Development — Vite dev server + HMR
# ========================================
FROM node:22-alpine AS development

WORKDIR /app

ARG VITE_API_BASE_URL=http://localhost/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 安装依赖（不 COPY 源码 — compose 用 volume 挂载）
COPY package.json package-lock.json ./
# 删除 lockfile 避免 npm optional dependency 跨平台 bug
RUN rm -f package-lock.json && npm install

EXPOSE 5173

# Vite dev server，HMR 通过 WebSocket 自动推送
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "5173"]
