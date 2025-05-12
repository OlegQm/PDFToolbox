import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const BASE_URL = mode === 'production' ? '/PDFToolbox/' : '/'
  return {
    plugins: [react()],
    base: BASE_URL,
    define: {
      'import.meta.env.VITE_BASE_URL': JSON.stringify(BASE_URL)
    },
    server: {
      host: true,
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
