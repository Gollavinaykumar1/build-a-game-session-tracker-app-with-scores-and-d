import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/build-a-game-session-tracker-app-with-scores-and-d/",
  build: { outDir: "dist", assetsDir: "assets" },
  server: { port: 3000 },
});
