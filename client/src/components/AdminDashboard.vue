<!--AdminDashboard.vue -->
<template>
  <div class="bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
    <div class="flex min-h-screen">
      <!-- 사이드바: 개선된 디자인 -->
      <div class="w-72 bg-white border-r border-gray-200 h-screen shadow-xl flex flex-col justify-between fixed left-0 top-0 z-40 backdrop-blur-sm">
        <div>
          <div class="p-8 border-b border-gray-100">
            <div class="flex items-center gap-3 mb-8">
              <div class="w-10 h-10 bg-gradient-to-br from-red-500 to-orange-500 rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-chart-line text-white text-lg"></i>
              </div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">
                SK<span class="text-orange-500">AXIS</span>
              </h1>
            </div>
            <nav class="space-y-2">
              <a href="#" @click.prevent="setActiveView('dashboard')" 
                 :class="activeView === 'dashboard' ? 'text-white bg-gradient-to-r from-red-500 to-red-600 shadow-lg shadow-red-500/25' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
                 class="flex items-center px-4 py-3.5 rounded-xl transition-all duration-200 group">
                <div :class="activeView === 'dashboard' ? 'bg-white/20' : 'bg-gray-100 group-hover:bg-gray-200'" 
                     class="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200">
                  <i class="fas fa-tachometer-alt" :class="activeView === 'dashboard' ? 'text-white' : 'text-gray-500 group-hover:text-gray-700'"></i>
                </div>
                <span class="ml-4 font-medium">대시보드</span>
                <div v-if="activeView === 'dashboard'" class="ml-auto w-2 h-2 bg-white rounded-full"></div>
              </a>
              
              <a href="#" @click.prevent="setActiveView('candidates')"
                 :class="activeView === 'candidates' ? 'text-white bg-gradient-to-r from-red-500 to-red-600 shadow-lg shadow-red-500/25' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
                 class="flex items-center px-4 py-3.5 rounded-xl transition-all duration-200 group">
                <div :class="activeView === 'candidates' ? 'bg-white/20' : 'bg-gray-100 group-hover:bg-gray-200'" 
                     class="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200">
                  <i class="fas fa-users" :class="activeView === 'candidates' ? 'text-white' : 'text-gray-500 group-hover:text-gray-700'"></i>
                </div>
                <span class="ml-4 font-medium">지원자 관리</span>
                <div v-if="activeView === 'candidates'" class="ml-auto w-2 h-2 bg-white rounded-full"></div>
              </a>
              
              <a href="#" @click.prevent="showCalendarView = true" 
                 class="flex items-center px-4 py-3.5 text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-xl transition-all duration-200 group">
                <div class="w-10 h-10 bg-gray-100 group-hover:bg-gray-200 rounded-lg flex items-center justify-center transition-all duration-200">
                  <i class="fas fa-calendar-alt text-gray-500 group-hover:text-gray-700"></i>
                </div>
                <span class="ml-4 font-medium">면접 일정</span>
              </a>
              
              <a href="#" @click.prevent="showStatistics" 
                 class="flex items-center px-4 py-3.5 text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-xl transition-all duration-200 group">
                <div class="w-10 h-10 bg-gray-100 group-hover:bg-gray-200 rounded-lg flex items-center justify-center transition-all duration-200">
                  <i class="fas fa-chart-bar text-gray-500 group-hover:text-gray-700"></i>
                </div>
                <span class="ml-4 font-medium">통계 분석</span>
              </a>
              
              <a href="#" @click.prevent="setActiveView('system-settings')"
                 :class="activeView === 'system-settings' ? 'text-white bg-gradient-to-r from-red-500 to-red-600 shadow-lg shadow-red-500/25' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
                 class="flex items-center px-4 py-3.5 rounded-xl transition-all duration-200 group">
                <div :class="activeView === 'system-settings' ? 'bg-white/20' : 'bg-gray-100 group-hover:bg-gray-200'" 
                     class="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200">
                  <i class="fas fa-cog" :class="activeView === 'system-settings' ? 'text-white' : 'text-gray-500 group-hover:text-gray-700'"></i>
                </div>
                <span class="ml-4 font-medium">시스템 설정</span>
                <div v-if="activeView === 'system-settings'" class="ml-auto w-2 h-2 bg-white rounded-full"></div>
              </a>
            </nav>
          </div>
        </div>
        
        <!-- 사용자 정보 개선 -->
        <div class="p-8 border-t border-gray-100">
          <div class="flex items-center gap-4 p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-lg">
              <i class="fas fa-user text-white text-lg"></i>
            </div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-gray-900">관리자</p>
              <p class="text-xs text-gray-500">admin@skaxis.com</p>
            </div>
            <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          </div>
        </div>
      </div>
      
      <!-- 메인 콘텐츠: 사이드바 오른쪽에 위치, 스크롤 가능 -->
      <div class="flex-1 ml-72">
        <DashboardMain
          v-if="activeView === 'dashboard'"
          :candidateList="candidateList"
          :filters="filters"
          :tableColumns="tableColumns"
          :sortedInterviews="sortedInterviews"
          @updateFilters="updateFilters"
          @close="emitClose"
        />
        <CandidateManage
          v-if="activeView === 'candidates'"
        />
        <InterviewCalendar
          v-if="showCalendarView"
          :calendarDays="calendarDays"
          :currentMonthYear="currentMonthYear"
          @close="showCalendarView = false"
          @prevMonth="prevMonth"
          @nextMonth="nextMonth"
        />
        <StatisticsModal
          v-if="showStatisticsView"
          :statisticsFilter="statisticsFilter"
          @close="showStatisticsView = false"
        />
        <SystemSettings
          v-if="activeView === 'system-settings'"
          @close="setActiveView('dashboard')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import DashboardMain from './DashboardMain.vue';
import CandidateManage from './CandidateManage.vue';
import InterviewCalendar from './InterviewCalendar.vue';
import StatisticsModal from './StatisticsModal.vue';
import SystemSettings from './SystemSettings.vue';

const router = useRouter();

// 활성 뷰 상태
const activeView = ref('dashboard');

// 필터 상태
const filters = ref({
  period: 'all',
  room: 'all',
  status: 'all',
  search: ''
});

// 정렬 설정
const sortConfig = ref({
  key: 'date',
  direction: 'asc' as 'asc' | 'desc'
});

// 테이블 컬럼 정의
const tableColumns = [
  { key: 'date', label: '날짜' },
  { key: 'time', label: '시간' },
  { key: 'room', label: '면접실' },
  { key: 'candidate', label: '지원자' },
  { key: 'interviewers', label: '면접관' },
  { key: 'status', label: '상태' },
  { key: 'score', label: '점수' },
  { key: 'actions', label: '상세보기' }
];

// 면접 데이터
interface Interview {
  id: number;
  date: string;
  time: string;
  room: string;
  candidate: string;
  position: string;
  department: string;
  interviewers: string[];
  status: string;
  score: number | null;
}
const interviews = ref<Interview[]>([]);

// 지원자 목록 데이터
interface Candidate {
  id: number;
  name: string;
  position: string;
  department?: string;
  interviewers: string[];
  status: string;
  interviewDate: string;
  score: number | null;
  interviewTime: string;
  room: string;
}
const candidateList = ref<Candidate[]>([]);

// 모달 상태
const showCalendarView = ref(false);
const currentDate = ref(new Date());
const showStatisticsView = ref(false);
const statisticsFilter = ref({
  period: 'all'
});

// 뷰 변경 함수
const setActiveView = (view: string) => {
  activeView.value = view;
};

// 필터 업데이트 함수 수정
const updateFilters = (newFilters: typeof filters.value) => {
  filters.value = { ...newFilters };
};

// 정렬된 면접 목록 - 필터링 로직 개선
const sortedInterviews = computed(() => {
  let filtered = [...interviews.value];

  // 기간 필터
  if (filters.value.period !== 'all') {
    const today = new Date();
    const pad = (n: number) => n.toString().padStart(2, '0');
    if (filters.value.period === 'today') {
      const todayStr = `${today.getFullYear()}-${pad(today.getMonth() + 1)}-${pad(today.getDate())}`;
      filtered = filtered.filter(i => i.date === todayStr);
    } else if (filters.value.period === 'week') {
      const startOfWeek = new Date(today);
      startOfWeek.setHours(0,0,0,0);
      startOfWeek.setDate(today.getDate() - today.getDay());
      const endOfWeek = new Date(startOfWeek);
      endOfWeek.setDate(startOfWeek.getDate() + 6);
      endOfWeek.setHours(23,59,59,999);
      filtered = filtered.filter(i => {
        const [y, m, d] = i.date.split('-').map(Number);
        const dateObj = new Date(y, m - 1, d);
        return dateObj >= startOfWeek && dateObj <= endOfWeek;
      });
    } else if (filters.value.period === 'month') {
      const year = today.getFullYear();
      const month = today.getMonth() + 1;
      filtered = filtered.filter(i => {
        const [y, m] = i.date.split('-').map(Number);
        return y === year && m === month;
      });
    }
  }

  // 면접실 필터
  if (filters.value.room !== 'all') {
    filtered = filtered.filter(i => i.room === filters.value.room);
  }

  // 상태 필터
  if (filters.value.status !== 'all') {
    filtered = filtered.filter(i => i.status === filters.value.status);
  }

  // 검색 필터 - 개선된 로직
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase();
    filtered = filtered.filter(i =>
      i.candidate.toLowerCase().includes(search) ||
      (i.department && i.department.toLowerCase().includes(search)) ||
      (i.position && i.position.toLowerCase().includes(search)) ||
      i.room.toLowerCase().includes(search) ||
      i.interviewers.some((interviewer: string) => interviewer.toLowerCase().includes(search))
    );
  }

  // 정렬
  return filtered.sort((a, b) => {
    const key = sortConfig.value.key as keyof Interview;
    const aVal = a[key] ?? '';
    const bVal = b[key] ?? '';
    if (aVal < bVal) return sortConfig.value.direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortConfig.value.direction === 'asc' ? 1 : -1;
    return 0;
  });
});

// 현재 월/년 표시
const currentMonthYear = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth() + 1;
  return `${year}년 ${month}월`;
});

// 캘린더 날짜 배열
interface CalendarDay {
  date: number;
  isCurrentMonth: boolean;
  interviews: Interview[];
}
const calendarDays = computed<CalendarDay[]>(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days: CalendarDay[] = [];

  // 이전 달 날짜 추가
  const prevMonthDays = firstDay.getDay();
  const prevMonth = new Date(year, month, 0);
  for (let i = prevMonthDays - 1; i >= 0; i--) {
    days.push({
      date: prevMonth.getDate() - i,
      isCurrentMonth: false,
      interviews: []
    });
  }

  // 현재 달 날짜 추가
  for (let date = 1; date <= lastDay.getDate(); date++) {
    const dayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
    const dayInterviews = interviews.value.filter((interview: Interview) => interview.date === dayStr);
    days.push({
      date,
      isCurrentMonth: true,
      interviews: dayInterviews
    });
  }

  // 다음 달 날짜 추가
  const remainingDays = 42 - days.length; // 6행 × 7일
  for (let i = 1; i <= remainingDays; i++) {
    days.push({
      date: i,
      isCurrentMonth: false,
      interviews: []
    });
  }

  return days;
});

// 함수들
const emitClose = () => {
  router.push('/');
};

const prevMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1);
};

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1);
};

// 사이드바 통계 분석 링크 클릭 이벤트 핸들러
const showStatistics = () => {
  showStatisticsView.value = true;
};

onMounted(async () => {
  try {
    const response = await fetch('http://3.38.218.18:8080/api/v1/interviewees/simple');
    if (!response.ok) throw new Error('서버 오류');
    const result = await response.json();
    interviews.value = result.data.map((item: Record<string, any>): Interview => {
      let date = '';
      let time = '';
      if (item.startAt) {
        const startAtStr = item.startAt.replace(/Z$/, '');
        const dateObj = new Date(startAtStr);
        date = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
        time = `${String(dateObj.getHours()).padStart(2, '0')}:${String(dateObj.getMinutes()).padStart(2, '0')}`;
      }
      return {
        id: item.intervieweeId,
        date,
        time,
        room: item.roomNo || '',
        candidate: item.name || '',
        position: item.position || '',
        department: item.department || '개발팀',
        interviewers: item.interviewers ? String(item.interviewers).split(',').map((s: string) => s.trim()) : [],
        status: item.status || 'UNDECIDED',
        score: item.score ?? null
      };
    });
    candidateList.value = result.data.map((item: Record<string, any>): Candidate => {
      let interviewDate = '';
      let interviewTime = '';
      if (item.startAt) {
        const startAtStr = item.startAt.replace(/Z$/, '');
        const dateObj = new Date(startAtStr);
        interviewDate = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
        interviewTime = `${String(dateObj.getHours()).padStart(2, '0')}:${String(dateObj.getMinutes()).padStart(2, '0')}`;
      }
      return {
        id: item.intervieweeId,
        name: item.name,
        position: item.position || '',
        department: item.department || '개발팀',
        interviewers: item.interviewers ? String(item.interviewers).split(',').map((s: string) => s.trim()) : [],
        status: item.status,
        interviewDate,
        score: item.score ?? null,
        interviewTime,
        room: item.roomNo || ''
      };
    });
  } catch (e) {
    alert('면접자 목록을 불러오지 못했습니다.');
  }
});
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateX(-20px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

.animate-slideIn {
  animation: slideIn 0.3s ease-out;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

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
</style>