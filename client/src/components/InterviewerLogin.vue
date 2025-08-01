<!-- src/components/InterviewerLogin.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex justify-center items-center relative overflow-hidden">
    <!-- 배경 장식 요소들 -->
    <div class="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-blue-200/30 to-purple-200/30 rounded-full blur-3xl -translate-x-48 -translate-y-48"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-gradient-to-br from-red-200/30 to-orange-200/30 rounded-full blur-3xl translate-x-48 translate-y-48"></div>
    <div class="absolute top-1/4 right-1/4 w-32 h-32 bg-gradient-to-br from-green-200/40 to-blue-200/40 rounded-full blur-2xl"></div>
    
    <!-- 관리자 로그인 버튼 -->
    <button 
      @click="showAdminLogin = true"
      class="absolute top-6 right-6 w-12 h-12 bg-white/80 backdrop-blur-sm hover:bg-white text-gray-600 hover:text-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group border border-gray-200/50"
    >
      <i class="fas fa-cog text-lg group-hover:rotate-90 transition-transform duration-300"></i>
    </button>
    
    <!-- 메인 로그인 카드 -->
    <div class="w-full max-w-2xl bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 relative overflow-hidden">
      <!-- 카드 내부 장식 -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-red-400/10 to-orange-400/10 rounded-full -translate-y-16 translate-x-16"></div>
      
      <div class="relative p-8 md:p-10">
        <!-- 로고 섹션 -->
        <div class="text-center mb-8">
          <img src="@/assets/sk.png" alt="SK Logo" class="mx-auto w-28 h-auto mb-6" />
          <h1 class="text-4xl font-bold mb-2">
            <span class="bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">SK</span><span class="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">AXIS</span>
          </h1>
          <div class="space-y-1">
            <h2 class="text-2xl font-bold text-gray-800">AI 면접 시스템</h2>
            <p class="text-gray-600 font-medium">{{ showRegistration ? '새로운 계정을 만들어보세요' : '안전하고 스마트한 면접을 시작하세요' }}</p>
          </div>
        </div>
        
        <!-- 로그인 폼 -->
        <form v-if="!showRegistration" @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-5">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-user text-blue-500"></i>
                아이디
              </label>
              <input
                type="text"
                v-model="loginForm.username"
                class="w-full px-4 py-4 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200 text-gray-800 placeholder-gray-400"
                placeholder="아이디를 입력하세요"
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
                v-model="loginForm.password"
                class="w-full px-4 py-4 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200 text-gray-800 placeholder-gray-400"
                placeholder="비밀번호를 입력하세요"
                required
              />
            </div>
          </div>
          
          <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <i class="fas fa-exclamation-triangle text-red-500"></i>
              <span class="text-red-700 text-sm font-medium">{{ loginError }}</span>
            </div>
          </div>
          
          <button
            type="submit"
            class="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white py-4 rounded-xl font-semibold shadow-lg shadow-red-500/25 hover:shadow-red-500/40 transition-all duration-300 transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
          >
            <i class="fas fa-sign-in-alt"></i>
            로그인
          </button>
          
          <div class="text-center">
            <button
              @click.prevent="showRegistration = true"
              class="text-gray-600 hover:text-gray-800 text-sm font-medium transition-colors duration-200 flex items-center gap-2 mx-auto group"
            >
              <span>계정이 없으신가요?</span>
              <span class="text-blue-600 group-hover:text-blue-700 font-semibold">회원가입</span>
              <i class="fas fa-arrow-right text-xs group-hover:translate-x-1 transition-transform"></i>
            </button>
          </div>
        </form>

        <!-- 회원가입 폼 -->
        <form v-else @submit.prevent="handleRegistration" class="space-y-6">
          <!-- 뒤로가기 버튼 -->
          <div class="mb-6">
            <button 
              @click.prevent="showRegistration = false" 
              class="text-gray-600 hover:text-gray-800 flex items-center gap-2 group transition-colors duration-200"
            >
              <i class="fas fa-arrow-left text-sm group-hover:-translate-x-1 transition-transform"></i>
              <span class="text-sm font-medium">로그인으로 돌아가기</span>
            </button>
          </div>
          
          <!-- 2열 그리드 레이아웃 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
            <!-- 이름 -->
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-id-badge text-purple-500"></i>
                이름
              </label>
              <input
                type="text"
                v-model="registrationForm.name"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
                placeholder="실명을 입력하세요"
                required
              />
            </div>
            
            <!-- 아이디 -->
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-user text-blue-500"></i>
                아이디
              </label>
              <input
                type="text"
                v-model="registrationForm.username"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
                placeholder="3자 이상의 아이디"
                required
              />
            </div>
            
            <!-- 이메일 -->
            <div class="space-y-2 md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-envelope text-green-500"></i>
                이메일
              </label>
              <input
                type="email"
                v-model="registrationForm.email"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
                placeholder="example@company.com"
                required
              />
            </div>
            
            <!-- 비밀번호 -->
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-lock text-red-500"></i>
                비밀번호
              </label>
              <input
                type="password"
                v-model="registrationForm.password"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
                placeholder="6자 이상의 비밀번호"
                required
              />
            </div>
            
            <!-- 비밀번호 확인 -->
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-shield-alt text-orange-500"></i>
                비밀번호 확인
              </label>
              <input
                type="password"
                v-model="registrationForm.confirmPassword"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
                placeholder="비밀번호를 다시 입력하세요"
                required
              />
            </div>
          </div>
          
          <div v-if="registrationError" class="bg-red-50 border border-red-200 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <i class="fas fa-exclamation-triangle text-red-500"></i>
              <span class="text-red-700 text-sm font-medium">{{ registrationError }}</span>
            </div>
          </div>
          
          <button
            type="submit"
            class="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white py-4 rounded-xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all duration-300 transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
          >
            <i class="fas fa-user-plus"></i>
            회원가입
          </button>
        </form>
        
        <!-- 푸터 -->
        <div class="mt-8 pt-6 border-t border-gray-200/50 text-center space-y-1">
          <p class="text-xs text-gray-500 font-medium">© 2025 SK AXIS. All rights reserved.</p>
          <p class="text-xs text-gray-400">Secure · Smart · Simple</p>
        </div>
      </div>
    </div>
    
    <!-- Admin Login Modal -->
    <AdminLoginModal 
      v-if="showAdminLogin"
      @close="showAdminLogin = false"
      @login="handleAdminLogin"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminLoginModal from './AdminLoginModal.vue'

const router = useRouter()

// 로그인 폼 데이터
const loginForm = ref({
  username: '',
  password: ''
})

// 회원가입 폼 데이터
const registrationForm = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 상태 관리
const loginError = ref('')
const registrationError = ref('')
const showAdminLogin = ref(false)
const showRegistration = ref(false)

// 로그인 처리
const handleLogin = async () => {
  try {
    loginError.value = '';
    
    const response = await fetch('http://3.38.218.18:8080/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        userName: loginForm.value.username,
        password: loginForm.value.password
      })
    });

    if (response.ok) {
      // JWT 토큰을 헤더에서 추출
      const authHeader = response.headers.get('Authorization');
      if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.substring(7);
        // 토큰을 localStorage에 저장
        localStorage.setItem('accessToken', token);
        console.log('로그인 성공, 토큰 저장됨');
      }
      
      // 응답 본문에서 사용자 정보 파싱
      try {
        const userData = await response.json();
        // 사용자 정보를 localStorage에 저장
        localStorage.setItem('userName', userData.username || '');
        localStorage.setItem('userDisplayName', userData.name || '');
        localStorage.setItem('userType', userData.userType || '');
        console.log('사용자 정보 저장됨:', userData);
      } catch (parseError) {
        console.warn('사용자 정보 파싱 실패:', parseError);
      }
      
      // 로그인 성공 시 면접 설정 페이지로 이동
      router.push('/setup');
    } else {
      let errorMessage = '로그인에 실패했습니다.';
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      } catch (e) {
        // JSON 파싱 실패 시 기본 메시지 사용
      }
      loginError.value = errorMessage;
    }
  } catch (error) {
    console.error('로그인 중 오류:', error);
    loginError.value = '네트워크 오류가 발생했습니다. 서버 연결을 확인해주세요.';
  }
}

// 회원가입 처리
const handleRegistration = async () => {
  // 에러 메시지 초기화
  registrationError.value = '';
  
  // 폼 검증
  if (!registrationForm.value.name.trim()) {
    registrationError.value = '이름을 입력해주세요.';
    return;
  }
  
  if (!registrationForm.value.username.trim()) {
    registrationError.value = '아이디를 입력해주세요.';
    return;
  }
  
  if (registrationForm.value.username.length < 3) {
    registrationError.value = '아이디는 3자 이상이어야 합니다.';
    return;
  }
  
  if (!registrationForm.value.email.trim()) {
    registrationError.value = '이메일을 입력해주세요.';
    return;
  }
  
  // 이메일 형식 검증
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(registrationForm.value.email)) {
    registrationError.value = '올바른 이메일 형식을 입력해주세요.';
    return;
  }
  
  if (!registrationForm.value.password) {
    registrationError.value = '비밀번호를 입력해주세요.';
    return;
  }
  
  if (registrationForm.value.password.length < 6) {
    registrationError.value = '비밀번호는 6자 이상이어야 합니다.';
    return;
  }
  
  if (registrationForm.value.password !== registrationForm.value.confirmPassword) {
    registrationError.value = '비밀번호가 일치하지 않습니다.';
    return;
  }
  
  // 회원가입 API 호출
  try {
    const response = await fetch('http://3.38.218.18:8080/api/v1/auth/signup/interviewer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        userName: registrationForm.value.username,
        name: registrationForm.value.name,
        password: registrationForm.value.password
      })
    });

    if (response.ok) {
      // 회원가입 성공 처리
      showSuccessModal();
    } else {
      let errorMessage = '회원가입에 실패했습니다.';
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      } catch (e) {
        // JSON 파싱 실패 시 기본 메시지 사용
      }
      registrationError.value = errorMessage;
    }
  } catch (error) {
    console.error('회원가입 중 오류:', error);
    registrationError.value = '네트워크 오류가 발생했습니다. 서버 연결을 확인해주세요.';
  }
}

// 성공 모달 표시
const showSuccessModal = () => {
  const successModal = document.createElement('div')
  successModal.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50'
  successModal.innerHTML = `
    <div class="bg-white/90 backdrop-blur-xl rounded-2xl p-8 max-w-md w-full mx-4 text-center shadow-2xl border border-white/20 animate-fadeIn">
      <div class="mb-6">
        <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center shadow-lg shadow-green-500/25">
          <i class="fas fa-check text-white text-3xl"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-3">회원가입 완료!</h3>
        <p class="text-gray-600 leading-relaxed">회원가입이 성공적으로 완료되었습니다.<br>이제 로그인하여 AI 면접 시스템을 이용하실 수 있습니다.</p>
      </div>
      <button class="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white py-3 rounded-xl font-semibold shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all duration-300 transform hover:-translate-y-0.5 cursor-pointer flex items-center justify-center gap-2">
        <i class="fas fa-arrow-right"></i>
        로그인으로 이동
      </button>
    </div>
  `
  
  // 애니메이션을 위한 스타일 추가
  const style = document.createElement('style')
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.9) translateY(20px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .animate-fadeIn {
      animation: fadeIn 0.4s ease-out;
    }
  `
  document.head.appendChild(style)
  document.body.appendChild(successModal)
  
  // 확인 버튼 클릭 이벤트
  const closeButton = successModal.querySelector('button')
  if (closeButton) {
    closeButton.addEventListener('click', () => {
      document.body.removeChild(successModal)
      document.head.removeChild(style)
      
      // 폼 초기화 및 로그인 화면으로 전환
      registrationForm.value = {
        name: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
      showRegistration.value = false
      registrationError.value = ''
      loginError.value = ''
      
      // 로그인 폼도 초기화
      loginForm.value = {
        username: '',
        password: ''
      }
    })
  }
}

// 관리자 로그인 처리
const handleAdminLogin = () => {
  router.push('/admin')
}
</script>

<style scoped>
/* 그라데이션 텍스트 */
.bg-clip-text {
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 커스텀 스크롤바 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #ef4444, #f97316);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #dc2626, #ea580c);
}

/* 폼 요소 애니메이션 */
input:focus, select:focus {
  transform: translateY(-1px);
}

/* 버튼 호버 효과 */
button {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>