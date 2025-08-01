import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      // /api로 시작하는 모든 요청(예: /api/v1, /api/ai)을
      // EC2에서 실행 중인 Nginx(포트 80)로 전달합니다.
      '/api': {
        target: 'http://3.38.218.18', // 여기에 EC2의 Public IP 주소를 입력하세요.
        changeOrigin: true,
        secure: false,
      },
      // WebSocket 연결을 위한 프록시 설정
      '/ws': {
        target: 'ws://3.38.218.18', // 여기에 EC2의 Public IP 주소를 입력하세요.
        ws: true,
        changeOrigin: true,
      },
    }
  }
})