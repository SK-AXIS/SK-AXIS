<!-- DashboardMain.vue -->
<template>
  <!-- 대시보드 뷰 -->
  <div class="container mx-auto px-8 py-8 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
    <!-- 헤더 개선 -->
    <div class="flex justify-between items-center mb-8">
      <div class="flex items-center gap-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">관리자 대시보드</h1>
          <p class="text-gray-600 mt-1">면접 진행 상황을 한눈에 확인하세요</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button class="px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-white/80 rounded-xl transition-all duration-200 backdrop-blur-sm border border-gray-200/50 flex items-center gap-2 shadow-sm hover:shadow-md">
          <i class="fas fa-info-circle text-blue-500"></i> 
          <span class="font-medium">About</span>
        </button>
        <button class="px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-white/80 rounded-xl transition-all duration-200 backdrop-blur-sm border border-gray-200/50 flex items-center gap-2 shadow-sm hover:shadow-md">
          <i class="fas fa-headset text-green-500"></i> 
          <span class="font-medium">개발자 문의</span>
        </button>
        <button @click="$emit('close')" class="w-10 h-10 rounded-xl bg-red-50 hover:bg-red-100 text-red-500 hover:text-red-600 transition-all duration-200 flex items-center justify-center border border-red-200/50">
          <i class="fas fa-times text-lg"></i>
        </button>
      </div>
    </div>
    
    <!-- 통계 카드 개선 -->
    <div class="grid grid-cols-4 gap-8 mb-10">
      <!-- 전체 지원자 -->
      <div class="group">
        <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-400/10 to-blue-600/10 rounded-full -translate-y-16 translate-x-16"></div>
          <div class="relative">
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/25">
                <i class="fas fa-users text-white text-2xl"></i>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-blue-600 uppercase tracking-wide">Total</p>
                <p class="text-4xl font-bold text-gray-900">{{ candidateList.length }}</p>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">전체 지원자</h3>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">취소된 면접자 수:</span>
              <div class="flex items-center gap-1 px-2 py-1 bg-red-50 rounded-lg">
                <i class="fas fa-times text-red-500 text-xs"></i>
                <span class="text-red-600 font-semibold">{{ cancelledInterviewsCount }}명</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 오늘의 면접 -->
      <div class="group">
        <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-green-400/10 to-green-600/10 rounded-full -translate-y-16 translate-x-16"></div>
          <div class="relative">
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg shadow-green-500/25">
                <i class="fas fa-calendar-day text-white text-2xl"></i>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-green-600 uppercase tracking-wide">Today</p>
                <p class="text-4xl font-bold text-gray-900">{{ todayInterviewsCount }}</p>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">오늘의 면접</h3>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">전일 대비</span>
              <div class="flex items-center gap-1 px-2 py-1 bg-green-50 rounded-lg">
                <i class="fas fa-caret-up text-green-500 text-xs"></i>
                <span class="text-green-600 font-semibold">{{ todayInterviewsCount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 완료된 면접 -->
      <div class="group">
        <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-400/10 to-purple-600/10 rounded-full -translate-y-16 translate-x-16"></div>
          <div class="relative">
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/25">
                <i class="fas fa-check-circle text-white text-2xl"></i>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-purple-600 uppercase tracking-wide">Completed</p>
                <p class="text-4xl font-bold text-gray-900">{{ completedInterviewsCount }}</p>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">완료된 면접</h3>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">전체 면접 대비</span>
              <div class="px-2 py-1 bg-purple-50 rounded-lg">
                <span class="text-purple-600 font-semibold">{{ completedPercentage }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 대기중 -->
      <div class="group">
        <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-orange-400/10 to-orange-600/10 rounded-full -translate-y-16 translate-x-16"></div>
          <div class="relative">
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl flex items-center justify-center shadow-lg shadow-orange-500/25">
                <i class="fas fa-clock text-white text-2xl"></i>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-orange-600 uppercase tracking-wide">Pending</p>
                <p class="text-4xl font-bold text-gray-900">{{ scheduledInterviewsCount }}</p>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">대기중</h3>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">전체 면접 대비</span>
              <div class="px-2 py-1 bg-orange-50 rounded-lg">
                <span class="text-orange-600 font-semibold">{{ scheduledPercentage }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 필터 섹션 개선 -->
    <div class="bg-white rounded-2xl p-8 mb-8 border border-gray-100 shadow-lg">
      <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-2">
        <i class="fas fa-filter text-blue-500"></i>
        필터 옵션
      </h2>
      <div class="grid grid-cols-4 gap-8">
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">면접 기간</label>
          <select :value="filters.period" @change="updateFilter('period', ($event.target as HTMLSelectElement).value)" 
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <option value="all">전체 기간</option>
            <option value="today">오늘</option>
            <option value="week">이번 주</option>
            <option value="month">이번 달</option>
          </select>
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">면접실</label>
          <select :value="filters.room" @change="updateFilter('room', ($event.target as HTMLSelectElement).value)" 
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <option value="all">전체</option>
            <option value="회의실A">회의실A</option>
            <option value="회의실B">회의실B</option>
            <option value="회의실C">회의실C</option>
            <option value="회의실D">회의실D</option>
          </select>
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">평가 상태</label>
          <select :value="filters.status" @change="updateFilter('status', ($event.target as HTMLSelectElement).value)" 
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <option value="all">전체</option>
            <option value="COMPLETED">평가 완료</option>
            <option value="SCHEDULED">대기중</option>
            <option value="IN_PROGRESS">진행중</option>
            <option value="CANCELLED">취소</option>
            <option value="UNDECIDED">미정</option>
          </select>
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">검색</label>
          <div class="relative">
            <input type="text" :value="filters.search" @input="updateFilter('search', ($event.target as HTMLInputElement).value)" 
                   placeholder="이름, 부서, 면접실, 면접관 검색" 
                   class="w-full px-4 py-3 pr-12 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <i class="fas fa-search text-gray-400"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 테이블 섹션 개선 -->
    <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-lg mb-8">
      <div class="p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-gray-100">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <i class="fas fa-table text-blue-500"></i>
              면접자 목록
            </h2>
            <p class="text-sm text-gray-600 mt-1">총 {{ sortedInterviews.length }}건의 면접 일정</p>
          </div>
          <div class="flex items-center gap-4">
            <button @click="showDeleteConfirm = true" 
                    class="group px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg shadow-red-500/25 hover:shadow-red-500/40 transform hover:-translate-y-0.5 flex items-center gap-2">
              <i class="fas fa-trash-alt group-hover:scale-110 transition-transform"></i> 
              <span class="font-medium">전체 삭제</span>
            </button>
            <label class="group px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:from-gray-600 hover:to-gray-700 transition-all duration-200 shadow-lg shadow-gray-500/25 hover:shadow-gray-500/40 transform hover:-translate-y-0.5 cursor-pointer flex items-center gap-2">
              <i class="fas fa-file-upload group-hover:scale-110 transition-transform"></i> 
              <span class="font-medium">엑셀 업로드</span>
              <input type="file" accept=".xlsx,.xls" class="hidden" @change="handleExcelUpload">
            </label>
            <button @click="$emit('downloadExcel')" 
                    class="group px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transform hover:-translate-y-0.5 flex items-center gap-2">
              <i class="fas fa-file-download group-hover:scale-110 transition-transform"></i> 
              <span class="font-medium">엑셀 다운로드</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
            <tr>
              <th v-for="column in visibleTableColumns" :key="column.key"
                  @click="$emit('sortBy', column.key)"
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  {{ column.label }} 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-if="pagedInterviews.length === 0">
              <td :colspan="visibleTableColumns.length" class="px-6 py-12 text-center text-gray-500">
                <div class="flex flex-col items-center">
                  <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <i class="fas fa-search text-3xl text-gray-300"></i>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">데이터가 없습니다</h3>
                  <span class="text-gray-500">조건에 맞는 면접자가 없습니다.</span>
                </div>
              </td>
            </tr>
            <tr v-for="interview in pagedInterviews" :key="interview.id" 
                class="hover:bg-blue-50/50 transition-colors duration-200 group">
              <td v-for="column in visibleTableColumns" :key="column.key" class="px-6 py-4 whitespace-nowrap">
                <template v-if="column.key === 'date'">
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
                    <span class="text-sm font-medium">{{ interview.date }}</span>
                  </div>
                </template>
                <template v-else-if="column.key === 'time'">
                  <span class="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-lg">{{ interview.time }}</span>
                </template>
                <template v-else-if="column.key === 'room'">
                  <span class="text-sm font-medium text-purple-600 bg-purple-100 px-3 py-1 rounded-lg">{{ interview.room || '-' }}</span>
                </template>
                <template v-else-if="column.key === 'candidate'">
                  <div>
                    <div class="text-sm font-semibold text-gray-900">{{ interview.candidate }}</div>
                    <div v-if="interview.position && interview.position.trim()" class="text-xs text-gray-500 mt-1">{{ interview.position }}</div>
                  </div>
                </template>
                <template v-else-if="column.key === 'interviewers'">
                  <div class="max-w-32 truncate text-sm text-gray-600" :title="interview.interviewers.join(', ')">
                    {{ interview.interviewers.join(', ') || '-' }}
                  </div>
                </template>
                <template v-else-if="column.key === 'status'">
                  <span :class="{
                    'px-3 py-1 text-xs font-medium rounded-full border': true,
                    'bg-green-50 text-green-700 border-green-200': interview.status === 'COMPLETED',
                    'bg-yellow-50 text-yellow-700 border-yellow-200': interview.status === 'SCHEDULED' || interview.status === 'UNDECIDED',
                    'bg-blue-50 text-blue-700 border-blue-200': interview.status === 'IN_PROGRESS',
                    'bg-gray-50 text-gray-700 border-gray-200': interview.status === 'CANCELLED'
                  }">
                    {{ getStatusText(interview.status) }}
                  </span>
                </template>
                <template v-else-if="column.key === 'score'">
                  <span v-if="interview.score !== null" :class="{
                    'font-bold text-sm px-3 py-1 rounded-lg': true,
                    'text-green-700 bg-green-100': interview.score >= 90,
                    'text-blue-700 bg-blue-100': interview.score >= 80 && interview.score < 90,
                    'text-yellow-700 bg-yellow-100': interview.score >= 70 && interview.score < 80,
                    'text-red-700 bg-red-100': interview.score < 70
                  }">
                    {{ interview.score }}점
                  </span>
                  <span v-else class="text-gray-400 text-sm">-</span>
                </template>
                <template v-else-if="column.key === 'actions'">
                  <button @click="$emit('viewDetails', interview.id)" 
                          class="w-8 h-8 rounded-lg bg-blue-100 hover:bg-blue-200 text-blue-600 hover:text-blue-700 transition-all duration-200 flex items-center justify-center group-hover:scale-110" 
                          title="상세보기">
                    <i class="fas fa-eye text-sm"></i>
                  </button>
                </template>
                <template v-else>
                  <span class="text-sm">{{ (interview as any)[column.key] }}</span>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 페이지네이션 개선 -->
    <div class="flex justify-between items-center mt-8">
      <div class="flex items-center gap-4">
        <label for="itemsPerPageDashboard" class="text-sm font-medium text-gray-700">페이지당 표시:</label>
        <select id="itemsPerPageDashboard" v-model.number="itemsPerPage" 
                class="px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 shadow-sm">
          <option :value="5">5개</option>
          <option :value="10">10개</option>
          <option :value="15">15개</option>
        </select>
      </div>
      
      <div class="flex items-center gap-2">
        <button @click="goToPage(1)" :disabled="currentPage === 1" 
                class="w-10 h-10 rounded-xl transition-all duration-200 flex items-center justify-center" 
                :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-blue-50 shadow-sm hover:shadow-md border border-gray-200'">
          <i class="fas fa-angle-double-left"></i>
        </button>
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" 
                class="w-10 h-10 rounded-xl transition-all duration-200 flex items-center justify-center" 
                :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-blue-50 shadow-sm hover:shadow-md border border-gray-200'">
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <div class="flex items-center gap-1">
          <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" 
                  :class="page === currentPage ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg shadow-blue-500/25' : 'bg-white text-gray-700 hover:bg-blue-50 shadow-sm hover:shadow-md border border-gray-200'" 
                  class="w-10 h-10 rounded-xl transition-all duration-200 flex items-center justify-center font-medium">
            {{ page }}
          </button>
        </div>
        
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0" 
                class="w-10 h-10 rounded-xl transition-all duration-200 flex items-center justify-center" 
                :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-blue-50 shadow-sm hover:shadow-md border border-gray-200'">
          <i class="fas fa-chevron-right"></i>
        </button>
        <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages || totalPages === 0" 
                class="w-10 h-10 rounded-xl transition-all duration-200 flex items-center justify-center" 
                :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-blue-50 shadow-sm hover:shadow-md border border-gray-200'">
          <i class="fas fa-angle-double-right"></i>
        </button>
      </div>
      
      <div class="text-sm text-gray-600">
        총 {{ sortedInterviews.length }}개 중 {{ Math.min((currentPage - 1) * itemsPerPage + 1, sortedInterviews.length) }}-{{ Math.min(currentPage * itemsPerPage, sortedInterviews.length) }}개 표시
      </div>
    </div>
    
    <!-- 전체 삭제 확인 모달 개선 -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl transform transition-all duration-300">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-exclamation-triangle text-red-600 text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">전체 삭제 확인</h3>
          <p class="text-gray-600 mb-8">모든 면접자 데이터를 삭제하시겠습니까?<br>이 작업은 되돌릴 수 없습니다.</p>
          <div class="flex gap-4">
            <button @click="showDeleteConfirm = false" 
                    class="flex-1 px-6 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl transition-all duration-200 font-medium">
              취소
            </button>
            <button @click="deleteAllInterviews" 
                    class="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 font-medium shadow-lg shadow-red-500/25">
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, computed, watch } from 'vue';

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

interface TableColumn {
  key: string;
  label: string;
}

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

const props = defineProps<{
  candidateList: Candidate[];
  filters: Record<string, string>;
  tableColumns: TableColumn[];
  sortedInterviews: Interview[];
}>();

const emits = defineEmits([
  'close',
  'showDeleteConfirm',
  'handleExcelUpload',
  'downloadExcel',
  'sortBy',
  'viewDetails',
  'updateFilters'
]);

// 페이징 관련 상태
const itemsPerPage = ref(5);
const currentPage = ref(1);

const pagedInterviews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return props.sortedInterviews.slice(start, start + itemsPerPage.value);
});

const totalPages = computed(() => Math.ceil(props.sortedInterviews.length / itemsPerPage.value));

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

watch(itemsPerPage, () => {
  currentPage.value = 1;
});

// 필터가 변경될 때마다 첫 페이지로 이동
watch(() => props.sortedInterviews, () => {
  currentPage.value = 1;
});

// 최대 5개만 보이는 페이지네이션 계산
const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }
  if (current <= 3) {
    return [1, 2, 3, 4, 5];
  }
  if (current >= total - 2) {
    return [total - 4, total - 3, total - 2, total - 1, total].filter(p => p > 0);
  }
  return [current - 2, current - 1, current, current + 1, current + 2];
});

// '지원 부서' 컬럼을 제외한 컬럼만 사용 (필요하다면 포함)
const visibleTableColumns = computed(() => props.tableColumns);

// 통계 계산을 위한 computed 속성들
const todayInterviewsCount = computed(() => {
  const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD 형식
  return props.candidateList.filter(candidate => candidate.interviewDate === today).length;
});

const completedInterviewsCount = computed(() => {
  return props.candidateList.filter(candidate => candidate.status === 'COMPLETED').length;
});

const scheduledInterviewsCount = computed(() => {
  return props.candidateList.filter(candidate => candidate.status === 'SCHEDULED').length;
});

const completedPercentage = computed(() => {
  if (props.candidateList.length === 0) return 0;
  return Math.round((completedInterviewsCount.value / props.candidateList.length) * 100);
});

const scheduledPercentage = computed(() => {
  if (props.candidateList.length === 0) return 0;
  return Math.round((scheduledInterviewsCount.value / props.candidateList.length) * 100);
});

const cancelledInterviewsCount = computed(() => {
  return props.candidateList.filter(candidate => candidate.status === 'CANCELLED').length;
});

// 엑셀 업로드 처리 함수
function handleExcelUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  fetch('http://3.38.218.18:8080/api/v1/uploads/interview-schedule', {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        alert('엑셀 업로드 실패: ' + response.statusText);
        return;
      }
      alert('엑셀 업로드 성공!');
    })
    .catch(error => {
      alert('엑셀 업로드 중 오류 발생: ' + (error as Error).message);
    })
    .finally(() => {
      (event.target as HTMLInputElement).value = '';
    });
}

function getStatusText(status: string) {
  switch ((status || '').toUpperCase()) {
    case 'COMPLETED': return '평가 완료';
    case 'SCHEDULED': return '대기중';
    case 'IN_PROGRESS': return '진행중';
    case 'CANCELLED': return '취소';
    case 'UNDECIDED': return '미정';
    default: return status;
  }
}

// 모달 상태 추가
const showDeleteConfirm = ref(false);

// 필터 업데이트 함수 - 수정된 버전
function updateFilter(key: string, value: string) {
  const newFilters = { ...props.filters, [key]: value };
  console.log('Filter updated:', key, '=', value); // 디버깅용
  console.log('New filters:', newFilters); // 디버깅용
  emits('updateFilters', newFilters);
}

function deleteAllInterviews() {
  fetch('http://3.38.218.18:8080/api/v1/interviews?deleteFiles=true', {
    method: 'DELETE',
    headers: { 'Accept': '*/*' }
  })
    .then(response => {
      if (!response.ok) {
        alert('전체 삭제 실패: ' + response.statusText);
        return;
      }
      alert('전체 삭제가 완료되었습니다.');
      showDeleteConfirm.value = false;
      // 필요하다면 데이터 새로고침 emit 등 추가
    })
    .catch(error => {
      alert('전체 삭제 중 오류 발생: ' + (error as Error).message);
      showDeleteConfirm.value = false;
    });
}
</script>

<style scoped>
/* 필요한 스타일 */
</style>