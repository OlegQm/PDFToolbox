import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const BASE_URL = mode === 'production' ? '/PDFToolbox/' : '/'
  const API_URL  = mode === 'production'
    ? BASE_URL
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
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, ''),
        },
      },
      allowedHosts: [
        'node100.webte.fei.stuba.sk',
        'node98.webte.fei.stuba.sk',
        'node85.webte.fei.stuba.sk',
        'node63.webte.fei.stuba.sk',
      ],
    },
    assetsInclude: ['**/*.riv'],
  }
})
