<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white/95 backdrop-blur-xl rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl border border-white/20 animate-fadeIn">
      <!-- 닫기 버튼 -->
      <button @click="emitClose" class="absolute top-4 right-4 w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center justify-center transition-all duration-200 group">
        <i class="fas fa-times text-gray-600 group-hover:text-gray-800 text-sm"></i>
      </button>
      
      <!-- 헤더 -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-red-500/25">
          <i class="fas fa-cog text-white text-xl"></i>
        </div>
        <h2 class="text-xl font-bold mb-2">
          <span class="text-red-600">SK</span><span class="text-orange-500">AXIS</span>
          <span class="text-gray-900 ml-2">관리자</span>
        </h2>
        <p class="text-gray-600 text-sm">시스템 관리자 전용 로그인</p>
      </div>
      
      <!-- 로그인 폼 -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
            <i class="fas fa-user text-blue-500"></i>
            아이디
          </label>
          <input
            type="text"
            v-model="username"
            class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
            placeholder="관리자 아이디를 입력하세요"
            required
          />
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
            <i class="fas fa-lock text-green-500"></i>
            비밀번호
          </label>
          <input
            type="password"
            v-model="password"
            class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>
        
        <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-3">
          <div class="flex items-center gap-2">
            <i class="fas fa-exclamation-triangle text-red-500"></i>
            <span class="text-red-700 text-sm font-medium">{{ error }}</span>
          </div>
        </div>
        
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white py-3 rounded-xl font-semibold shadow-lg shadow-red-500/25 hover:shadow-red-500/40 transition-all duration-300 transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
        >
          <i class="fas fa-sign-in-alt"></i>
          관리자 로그인
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const emit = defineEmits(['close', 'login']);
const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
try {
  fetch('http://3.38.218.18:8080/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userName: username.value,
      password: password.value
    })
  })
  router.push('/admin');
  emit('login');
} catch (err) {
  console.error('로그인 중 오류 발생:', err);
  error.value = '로그인에 실패했습니다. 다시 시도해주세요.';
  return;
}
}

function emitClose() {
  emit('close');
  username.value = '';
  password.value = '';
  error.value = '';
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

/* 폼 요소 애니메이션 */
input:focus {
  transform: translateY(-1px);
}
</style>