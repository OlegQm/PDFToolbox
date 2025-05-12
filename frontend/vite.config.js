import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const BASE_URL = mode === 'production' ? '/PDFToolbox/' : '/'
  const API_URL  = mode === 'production'
    ? BASE_URL        // если nginx на сервере проксирует /PDFToolbox/ на API
    : 'http://localhost:8000/'

  return {
    plugins: [react()],
    base: BASE_URL,
    define: {
      'import.meta.env.VITE_BASE_URL': JSON.stringify(BASE_URL),
      'import.meta.env.VITE_API_URL':  JSON.stringify(API_URL),
    },
    server: {
      host: true,
      proxy: {
        // при dev-запуске все запросы /api/* будут идти на localhost:8000
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, ''),
        },
      },
      allowedHosts: [ /* …ваши хосты… */ ],
    },
    assetsInclude: ['**/*.riv'],
  }
})
