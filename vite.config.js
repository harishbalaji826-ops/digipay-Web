import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  // Base path for GitHub Pages — matches repo name exactly (case-sensitive)
  // Repo: harishbalaji826-ops/digipay-Web  →  /digipay-Web/
  base: '/digipay-Web/',

  // Build output to docs/ so GitHub Pages can serve from
  // Settings → Pages → Branch: main → Folder: /docs
  build: {
    outDir: 'docs',
    emptyOutDir: true,
  },

  plugins: [react(), tailwindcss()],
  server: {
    port: 3000
  }
})
