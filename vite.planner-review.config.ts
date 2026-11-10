import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { realpathSync } from "node:fs";
import path from "node:path";
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": process.cwd() } },
  optimizeDeps: { entries: ["study-planner-local.html"] },
  server: {
    host: "127.0.0.1",
    port: 5188,
    strictPort: true,
    fs: { allow: [process.cwd(), realpathSync(path.resolve("node_modules"))] },
  },
});
