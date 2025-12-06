import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    hmr: true,
    // 在 WSL/网络挂载盘上监听文件变化可能不可靠，开启轮询提高热更新稳定性
    watch: {
      usePolling: true,
      interval: 200,
    },
  },
})
