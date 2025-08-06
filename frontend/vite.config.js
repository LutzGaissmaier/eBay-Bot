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
  server: {
    port: 5174,
    host: '0.0.0.0',
    allowedHosts: [
      'pr-verification-app-tunnel-b9zmaf09.devinapps.com',
      'localhost',
      '127.0.0.1',
      '172.16.19.2'
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:5003',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
