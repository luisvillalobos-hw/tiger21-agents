import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // Environment variables are automatically available as import.meta.env.VITE_*
  server: {
    // No proxy needed - frontend calls Agent Engine directly
  },
  preview: {
    port: 8080,
  },
})
