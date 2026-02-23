import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    allowedHosts: ["minitwo"],
    proxy: {
      "/money": {
        target: "http://localhost:58000",
        changeOrigin: true,
        cookieDomainRewrite: "",
      },
      "/auth-token": {
        target: "http://localhost:58000",
        changeOrigin: true,
        cookieDomainRewrite: "",
      },
      "/accounts": {
        target: "http://localhost:58000",
        changeOrigin: true,
        cookieDomainRewrite: "",
      },
    },
  },
});
