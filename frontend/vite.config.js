// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/PDFToolbox/',
  server: {
    host: true,
    allowedHosts: [
      'node100.webte.fei.stuba.sk',
      'node98.webte.fei.stuba.sk',
      'node85.webte.fei.stuba.sk',
      'node63.webte.fei.stuba.sk',
    ],
  },
})
