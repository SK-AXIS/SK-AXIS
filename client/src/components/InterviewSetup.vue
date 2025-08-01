<!-- InterviewSetup.vue -->
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

    <div class="w-full max-w-2xl bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 relative overflow-hidden">
      <!-- 카드 내부 장식 -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-red-400/10 to-orange-400/10 rounded-full -translate-y-16 translate-x-16"></div>
      
      <div class="relative p-8 md:p-10">
        <!-- 헤더 섹션 -->
        <div class="text-center mb-10">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-red-500 to-orange-500 rounded-2xl mb-6 shadow-xl shadow-red-500/25">
            <i class="fas fa-chart-line text-white text-2xl"></i>
          </div>
          <h1 class="text-4xl font-bold mb-2">
            <span class="bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">SK</span><span class="bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">AXIS</span>
          </h1>
          <h2 class="text-2xl font-bold text-gray-800 mb-6">AI 면접 시스템</h2>
          
          <!-- 면접관 환영 메시지 -->
          <div class="inline-flex items-center gap-3 px-6 py-3 bg-white/60 backdrop-blur-sm rounded-full shadow-lg border border-gray-200/50">
            <div class="w-8 h-8 bg-gradient-to-br from-red-500 to-orange-500 rounded-full flex items-center justify-center">
              <i class="fas fa-user text-white text-sm"></i>
            </div>
            <span class="text-gray-700 font-medium">
              안녕하세요, <span class="font-bold bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">{{ userDisplayName }}</span>님!
            </span>
          </div>
        </div>

        <!-- 면접 설정 폼 -->
        <div class="space-y-8">
          <!-- 날짜 및 호실 선택 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- 면접 날짜 -->
            <div class="space-y-3">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-calendar-alt text-blue-500"></i>
                면접 날짜
              </label>
              <input
                type="date"
                v-model="selectedDate"
                class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <!-- 면접 호실 -->
            <div class="space-y-3">
              <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                <i class="fas fa-door-open text-purple-500"></i>
                면접 호실
              </label>
              <div class="relative">
                <div
                  @click="toggleRoomDropdown"
                  class="w-full px-4 py-3 bg-gray-50/80 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-200 cursor-pointer text-gray-700 flex justify-between items-center hover:bg-gray-100/80"
                >
                  <span v-if="selectedRoom" class="font-medium">{{ rooms.find(r => r.id === selectedRoom)?.name }}</span>
                  <span v-else class="text-gray-500">면접 호실을 선택해주세요</span>
                  <i class="fas fa-chevron-down text-gray-600 transition-transform duration-200" :class="{ 'rotate-180': showRoomDropdown }"></i>
                </div>
                <div v-if="showRoomDropdown" class="absolute z-10 mt-2 w-full bg-white/95 backdrop-blur-sm border border-gray-200 rounded-xl shadow-xl max-h-60 overflow-y-auto">
                  <div
                    v-for="room in rooms"
                    :key="room.id"
                    @click="selectRoom(room.id)"
                    class="px-4 py-3 hover:bg-red-50 cursor-pointer transition-colors duration-200 border-b border-gray-100 last:border-b-0 font-medium"
                  >
                    {{ room.name }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 면접 일정 테이블 -->
          <div v-if="selectedRoom" class="space-y-4">
            <div class="flex items-center gap-2 mb-4">
              <i class="fas fa-clock text-green-500"></i>
              <h3 class="text-lg font-semibold text-gray-800">면접 일정</h3>
            </div>

            <div v-if="loading" class="text-center py-12 bg-gray-50/50 rounded-2xl">
              <i class="fas fa-spinner fa-spin text-3xl text-gray-400 mb-4"></i>
              <p class="text-gray-600 font-medium">일정을 불러오는 중...</p>
            </div>

            <div v-else-if="error" class="text-center py-12 bg-red-50/50 rounded-2xl">
              <i class="fas fa-exclamation-triangle text-3xl text-red-400 mb-4"></i>
              <p class="text-red-600 font-medium">{{ error }}</p>
            </div>

            <div v-else class="bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200/50 overflow-hidden">
              <div class="overflow-x-auto">
                <table class="w-full">
                  <thead>
                    <tr class="bg-gradient-to-r from-gray-50 to-gray-100">
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                        <i class="fas fa-clock mr-2 text-blue-500"></i>시간
                      </th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                        <i class="fas fa-user-tie mr-2 text-green-500"></i>면접관
                      </th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                        <i class="fas fa-user mr-2 text-purple-500"></i>지원자
                      </th>
                      <th class="px-6 py-4 text-center text-sm font-semibold text-gray-700 w-32">
                        <i class="fas fa-hand-pointer mr-2 text-orange-500"></i>선택
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="schedule in filteredSchedules" :key="schedule.timeRange" 
                        class="hover:bg-red-50/30 transition-colors duration-200"
                        :class="{ 'bg-red-50/20': selectedSchedule && selectedSchedule.roomName === schedule.roomName && selectedSchedule.timeRange === schedule.timeRange }">
                      <td class="px-6 py-4 text-sm font-medium text-gray-800 border-t border-gray-200/50">
                        {{ schedule.timeRange }}
                      </td>
                      <td class="px-6 py-4 text-sm text-gray-700 border-t border-gray-200/50">
                        <div class="space-y-1">
                          <div v-for="interviewer in schedule.interviewers" :key="interviewer" class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                            {{ interviewer }}
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 text-sm text-gray-700 border-t border-gray-200/50">
                        <div class="space-y-1">
                          <div v-for="name in getIntervieweeNames(schedule.interviewees).split('\n').filter(n => n)" :key="name" class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-purple-400 rounded-full"></div>
                            {{ name }}
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 text-center border-t border-gray-200/50">
                        <button
                          @click="selectTimeSlot(schedule)"
                          class="px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg"
                          :class="{
                            'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-green-500/25 hover:from-green-600 hover:to-green-700': selectedSchedule && 
                              selectedSchedule.roomName === schedule.roomName && 
                              selectedSchedule.timeRange === schedule.timeRange,
                            'bg-gradient-to-r from-red-500 to-red-600 text-white shadow-red-500/25 hover:from-red-600 hover:to-red-700': !selectedSchedule || 
                              selectedSchedule.roomName !== schedule.roomName || 
                              selectedSchedule.timeRange !== schedule.timeRange
                          }"
                        >
                          <i class="fas" :class="{
                            'fa-check': selectedSchedule && selectedSchedule.roomName === schedule.roomName && selectedSchedule.timeRange === schedule.timeRange,
                            'fa-hand-pointer': !selectedSchedule || selectedSchedule.roomName !== schedule.roomName || selectedSchedule.timeRange !== schedule.timeRange
                          }"></i>
                          {{ selectedSchedule && 
                             selectedSchedule.roomName === schedule.roomName && 
                             selectedSchedule.timeRange === schedule.timeRange ? '선택됨' : '선택' }}
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- 버튼 영역 -->
          <div class="flex flex-col sm:flex-row gap-4 pt-6">
            <button 
              @click="logout"
              class="px-6 py-3 text-gray-600 hover:text-gray-800 transition-all duration-300 flex items-center justify-center gap-2 border border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 font-medium"
            >
              <i class="fas fa-sign-out-alt"></i>
              로그아웃
            </button>
            
            <button
              class="flex-1 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg flex items-center justify-center gap-2"
              :disabled="!canProceed"
              :class="{
                'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white shadow-red-500/25 hover:shadow-red-500/40': canProceed && isToday,
                'bg-gray-400 text-white cursor-not-allowed shadow-gray-400/25': !canProceed || !isToday
              }"
              @click="onStartInterview"
            >
              <i class="fas" :class="{
                'fa-play': isToday,
                'fa-calendar-times': !isToday
              }"></i>
              {{ isToday ? '면접 시작하기' : '오늘 날짜의 면접만 시작할 수 있습니다' }}
            </button>
          </div>
        </div>

        <!-- 푸터 -->
        <div class="mt-12 pt-8 border-t border-gray-200/50 text-center space-y-2">
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

import AdminLoginModal from './AdminLoginModal.vue';
import { getInterviewSchedules } from '../services/interviewService';

const router = useRouter();

const selectedRoom = ref<string>('');
const selectedTimeSlot = ref<string>('');
const showRoomDropdown = ref(false);
const selectedDate = ref<string>(new Date().toISOString().split('T')[0]);
const schedules = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const showAdminLogin = ref(false);
const selectedSchedule = ref<any>(null);

// 로그인한 사용자 이름을 가져오는 computed 속성
const userDisplayName = computed(() => {
  return localStorage.getItem('userDisplayName') || '면접관';
});

// API 데이터에서 동적으로 rooms 생성
const rooms = computed(() => {
  if (!schedules.value || !Array.isArray(schedules.value)) {
    return [];
  }
  const uniqueRooms = new Set(schedules.value.map(schedule => schedule.roomName));
  return Array.from(uniqueRooms).map((roomName, index) => ({
    id: `room${index + 1}`,
    name: roomName
  }));
});

// 오늘 날짜와 선택된 날짜가 일치하는지 확인하는 computed 속성
const isToday = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return selectedDate.value === today;
});

// selectedRoom, selectedTimeSlot, isToday가 모두 true일 때만 canProceed가 true가 되도록 변경
const canProceed = computed(() => {
  return selectedRoom.value && 
         selectedTimeSlot.value && 
         isToday.value && 
         selectedSchedule.value;
});

// props.rooms 대신 rooms.value 사용
const filteredSchedules = computed(() => {
  if (!schedules.value || !Array.isArray(schedules.value)) {
    return [];
  }
  return schedules.value.filter(schedule => 
    schedule.roomName === rooms.value.find(r => r.id === selectedRoom.value)?.name
  );
});

const toggleRoomDropdown = () => { showRoomDropdown.value = !showRoomDropdown.value; };
const selectRoom = (roomId: string) => {
  selectedRoom.value = roomId;
  selectedTimeSlot.value = '';
  selectedSchedule.value = null;
  showRoomDropdown.value = false;
};

const fetchSchedules = async () => {
  if (!selectedDate.value) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    const response = await getInterviewSchedules(selectedDate.value);
    console.log('API Response:', response);
    schedules.value = response.schedules || [];
  } catch (err) {
    error.value = '면접 일정을 불러오는데 실패했습니다.';
    console.error(err);
    schedules.value = []; // 에러 시 빈 배열로 초기화
  } finally {
    loading.value = false;
  }
};

const selectTimeSlot = (schedule: any) => {
  selectedSchedule.value = schedule;
  selectedTimeSlot.value = schedule.timeRange;
};

// 날짜가 변경될 때마다 일정을 다시 불러옵니다
watch(selectedDate, () => {
  selectedRoom.value = '';
  selectedTimeSlot.value = '';
  selectedSchedule.value = null;
  fetchSchedules();
});

const onStartInterview = () => {
  if (!canProceed.value || !selectedSchedule.value) return;
  
  console.log('선택된 스케줄:', selectedSchedule.value);
  console.log('전체 스케줄:', schedules.value);
  
  // 면접 일정에서 지원자 정보 추출
  const candidateIds: number[] = [];
  const candidateNames: string[] = [];
  
  // API 응답에서 해당 스케줄의 지원자 정보 찾기
  const scheduleData = schedules.value.find(schedule => 
    schedule.roomName === selectedSchedule.value.roomName &&
    schedule.timeRange === selectedSchedule.value.timeRange
  );
  
  console.log('찾은 스케줄 데이터:', scheduleData);
  
  if (scheduleData && scheduleData.interviewees) {
    scheduleData.interviewees.forEach((interviewee: { name: string; id: number }) => {
      candidateNames.push(interviewee.name);
      candidateIds.push(interviewee.id);
    });
  }
  
  console.log('추출된 지원자 ID:', candidateIds);
  console.log('추출된 지원자 이름:', candidateNames);
  
  // candidateIds가 비어있지 않은지 확인
  if (candidateIds.length === 0) {
    console.error('지원자 정보를 찾을 수 없습니다.');
    alert('지원자 정보를 불러오는 중 오류가 발생했습니다. 다시 시도해주세요.');
    return;
  }
  
  router.push({
    name: 'interview',
    query: {
      roomName: selectedSchedule.value.roomName,
      date: selectedDate.value,
      timeRange: selectedSchedule.value.timeRange,
      interviewers: selectedSchedule.value.interviewers.join(', '),
      interviewerIds: JSON.stringify(selectedSchedule.value.interviewerIds || []),
      candidates: JSON.stringify(candidateNames),
      candidateIds: JSON.stringify(candidateIds),
      interview_id: selectedSchedule.value.interviewId
    }
  });
};

const handleAdminLogin = () => {
  // 로그인 성공 시 관리자 대시보드로 이동
  router.push('/admin');
};

// 로그아웃 함수 추가
const logout = () => {
  // localStorage 클리어
  localStorage.clear();
  // 메인 로그인 페이지로 이동
  router.push('/');
};

// 지원자 이름을 추출하는 함수
const getIntervieweeNames = (interviewees: any[]): string => {
  if (!interviewees || !Array.isArray(interviewees)) {
    return '';
  }
  return interviewees.map((interviewee: any) => interviewee.name || '').join('\n');
};

onMounted(() => {
  fetchSchedules();
  document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement;
    if (!target.closest('.relative') && showRoomDropdown.value) {
      showRoomDropdown.value = false;
    }
  });
});
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

/* 테이블 행 호버 효과 */
tbody tr:hover {
  transform: translateY(-1px);
}
</style>