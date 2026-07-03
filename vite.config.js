import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // 相对路径，适配 GitHub Pages
  server: {
    port: 3000,
    open: true,
  },
})
