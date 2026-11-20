import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const apiTarget = process.env.LEGO_API_URL ?? 'http://127.0.0.1:8787';

export default defineConfig({
  plugins: [react()],
  server: {
    port: Number(process.env.LEGO_WEB_PORT ?? 5173),
    strictPort: true,
    proxy: {
      '/api': { target: apiTarget, changeOrigin: false },
      '/health': { target: apiTarget, changeOrigin: false },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    target: 'es2022',
  },
});
