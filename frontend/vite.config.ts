import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, './src'),
    },
  },
  server: {
    host: true,
    port: 5180,
    strictPort: true,
    proxy: {
      // 8000 is used by another project on this machine — LOOP-MIND's own
      // backend runs on 8011 (moved from 8010 after 8010 became a
      // permanently stuck OS-level socket on this dev machine that no
      // process kill could free).
      '/api': 'http://localhost:8011',
    },
  },
})
