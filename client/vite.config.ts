import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  // 상위 디렉토리의 .env 파일 로드
  const env = loadEnv(mode, path.resolve(__dirname, '../'), '')
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 3000,
      open: true
    },
    // 환경변수를 클라이언트에서 사용할 수 있도록 정의
    define: {
      __SPRING_API_URL__: JSON.stringify(env.SPRING_API_URL || 'http://3.38.218.18:8080/api/v1'),
      // __FASTAPI_URL__: JSON.stringify(env.FASTAPI_URL || 'http://localhost:8000/api/v1'),
      // __REDIS_HOST__: JSON.stringify(env.REDIS_HOST || 'localhost'),
      // __REDIS_PORT__: JSON.stringify(env.REDIS_PORT || '6379')
    }
  }
})