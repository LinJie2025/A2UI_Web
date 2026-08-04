FROM node:22-alpine AS build

WORKDIR /app

ARG VITE_API_BASE_URL=http://localhost/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY package.json ./
RUN npm install

COPY . .
RUN npx vite build

FROM alpine:3.20
COPY --from=build /app/dist /app/dist
