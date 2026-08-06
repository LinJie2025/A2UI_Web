import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        // Docker 开发环境使用 nginx 服务名；本地开发使用 localhost
        target: process.env.VITE_PROXY_TARGET || "http://localhost",
        changeOrigin: true,
      },
    },
  },
});
