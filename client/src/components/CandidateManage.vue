<!-- CandidateManage.vue -->
<template>
  <!-- 지원자 관리 뷰 -->
  <div class="p-8 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
    <!-- 지원자 관리 헤더 개선 -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
            <i class="fas fa-users text-white"></i>
          </div>
          지원자 관리
        </h1>
        <p class="text-gray-600 mt-2">면접 지원자들을 효율적으로 관리하세요</p>
      </div>
      <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
        <div class="grid grid-cols-2 gap-6 text-center">
          <div>
            <p class="text-2xl font-bold text-blue-600">{{ candidateList.length }}</p>
            <p class="text-sm text-gray-600">총 지원자</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-green-600">{{ filteredCandidates.length }}</p>
            <p class="text-sm text-gray-600">필터 결과</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 필터 및 검색 개선 -->
    <div class="bg-white rounded-2xl p-8 mb-8 border border-gray-200 shadow-lg">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-800 flex items-center gap-2">
          <i class="fas fa-filter text-blue-500"></i>
          필터 & 검색
        </h2>
        <button 
          v-if="hasActiveFilters"
          @click="resetFilters" 
          class="px-4 py-2 text-sm text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 border border-red-200 rounded-xl transition-all duration-200 flex items-center gap-2">
          <i class="fas fa-times"></i>
          필터 초기화
        </button>
      </div>
      
      <div class="grid grid-cols-4 gap-6 mb-6">
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">상태</label>
          <select v-model="filters.status" @change="onFilterChange" 
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <option value="all">전체</option>
            <option value="SCHEDULED">예정</option>
            <option value="IN_PROGRESS">진행중</option>
            <option value="COMPLETED">완료</option>
            <option value="CANCELLED">취소</option>
            <option value="UNDECIDED">미정</option>
          </select>
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">면접 일정</label>
          <input 
            type="date" 
            v-model="filters.interviewDate" 
            @change="onFilterChange"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">면접실</label>
          <select v-model="filters.room" @change="onFilterChange" 
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <option value="all">전체</option>
            <option v-for="room in uniqueRooms" :key="room" :value="room">{{ room }}</option>
          </select>
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">검색</label>
          <div class="relative">
            <input 
              type="text" 
              v-model="filters.search" 
              @input="onFilterChange"
              placeholder="이름, 직무, 면접관 검색" 
              class="w-full px-4 py-3 pr-12 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:bg-gray-100">
            <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <i class="fas fa-search text-gray-400"></i>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 활성 필터 표시 개선 -->
      <div class="flex items-center gap-3 flex-wrap" v-if="hasActiveFilters">
        <span class="text-sm font-medium text-gray-600">활성 필터:</span>
        <span v-if="filters.status !== 'all'" class="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full border border-blue-200">
          <i class="fas fa-tag"></i>
          상태: {{ getStatusText(filters.status) }}
        </span>
        <span v-if="filters.interviewDate" class="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full border border-green-200">
          <i class="fas fa-calendar"></i>
          날짜: {{ filters.interviewDate }}
        </span>
        <span v-if="filters.room !== 'all'" class="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full border border-purple-200">
          <i class="fas fa-door-open"></i>
          면접실: {{ filters.room }}
        </span>
        <span v-if="filters.search" class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-800 text-xs font-medium rounded-full border border-gray-200">
          <i class="fas fa-search"></i>
          검색: "{{ filters.search }}"
        </span>
      </div>
      <div v-else class="text-sm text-gray-500 flex items-center gap-2">
        <i class="fas fa-info-circle"></i>
        현재 활성화된 필터가 없습니다
      </div>
    </div>
    
    <!-- 지원자 목록 테이블 개선 -->
    <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-lg">
      <div class="p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-gray-100">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <i class="fas fa-table text-blue-500"></i>
              지원자 목록
            </h2>
            <p class="text-sm text-gray-600 mt-1">
              {{ filteredCandidates.length }}명 / 전체 {{ candidateList.length }}명
            </p>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3 bg-white rounded-xl px-4 py-2 border border-gray-200">
              <label for="itemsPerPage" class="text-sm font-medium text-gray-700">페이지당</label>
              <select id="itemsPerPage" v-model.number="itemsPerPage" 
                      class="px-3 py-1 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200">
                <option :value="8">8</option>
                <option :value="10">10</option>
                <option :value="15">15</option>
                <option :value="20">20</option>
              </select>
              <span class="text-sm text-gray-700">개 보기</span>
            </div>
            <button @click="openAddModal" 
                    class="group px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transform hover:-translate-y-0.5 flex items-center gap-2">
              <i class="fas fa-plus group-hover:scale-110 transition-transform"></i>
              <span class="font-medium">지원자 추가</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
            <tr>
              <th @click="sortBy('interviewDate')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  날짜 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th @click="sortBy('interviewTime')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  시간 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th @click="sortBy('room')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  면접실 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th @click="sortBy('name')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  지원자 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">면접관</th>
              <th @click="sortBy('status')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  상태 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th @click="sortBy('score')" 
                  class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition-colors duration-200 group">
                <div class="flex items-center gap-2">
                  점수 
                  <i class="fas fa-sort text-gray-400 group-hover:text-gray-600 transition-colors"></i>
                </div>
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">관리</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-if="pagedCandidates.length === 0">
              <td colspan="8" class="px-6 py-12 text-center text-gray-500">
                <div class="flex flex-col items-center">
                  <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <i class="fas fa-search text-3xl text-gray-300"></i>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">데이터가 없습니다</h3>
                  <span class="text-gray-500 mb-4">조건에 맞는 지원자가 없습니다.</span>
                  <button @click="resetFilters" 
                          class="px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors text-sm">
                    필터 초기화
                  </button>
                </div>
              </td>
            </tr>
            <tr v-for="candidate in pagedCandidates" :key="candidate.id" 
                class="hover:bg-blue-50/50 transition-colors duration-200 group">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span class="text-sm font-medium">{{ formatDate(candidate.interviewDate) }}</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-lg">{{ candidate.interviewTime || '-' }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm font-medium text-purple-600 bg-purple-100 px-3 py-1 rounded-lg border border-purple-200">
                  {{ candidate.room || '-' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="text-sm font-semibold text-gray-900">{{ candidate.name }}</div>
                  <div v-if="candidate.position && candidate.position.trim()" class="text-xs text-gray-500 mt-1">{{ candidate.position }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="max-w-32 truncate text-sm text-gray-600" :title="candidate.interviewers ? candidate.interviewers.join(', ') : '-'">
                  {{ candidate.interviewers ? candidate.interviewers.join(', ') : '-' }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'px-3 py-1 text-xs font-medium rounded-full border': true,
                  'bg-green-50 text-green-700 border-green-200': candidate.status === 'COMPLETED',
                  'bg-yellow-50 text-yellow-700 border-yellow-200': candidate.status === 'SCHEDULED' || candidate.status === 'UNDECIDED',
                  'bg-blue-50 text-blue-700 border-blue-200': candidate.status === 'IN_PROGRESS',
                  'bg-gray-50 text-gray-700 border-gray-200': candidate.status === 'CANCELLED'
                }">{{ getStatusText(candidate.status) }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="candidate.score !== null" :class="{
                  'font-bold text-sm px-3 py-1 rounded-lg': true,
                  'text-green-700 bg-green-100': candidate.score >= 90,
                  'text-blue-700 bg-blue-100': candidate.score >= 80 && candidate.score < 90,
                  'text-yellow-700 bg-yellow-100': candidate.score >= 70 && candidate.score < 80,
                  'text-red-700 bg-red-100': candidate.score < 70
                }">
                  {{ candidate.score }}점
                </span>
                <span v-else class="text-gray-400 text-sm">-</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-2">
                  <button class="w-8 h-8 rounded-lg bg-blue-100 hover:bg-blue-200 text-blue-600 hover:text-blue-700 transition-all duration-200 flex items-center justify-center group-hover:scale-110" 
                          @click="openEditModal(candidate)" title="수정">
                    <i class="fas fa-edit text-sm"></i>
                  </button>
                  <button class="w-8 h-8 rounded-lg bg-red-100 hover:bg-red-200 text-red-600 hover:text-red-700 transition-all duration-200 flex items-center justify-center group-hover:scale-110" 
                          @click="openDeleteModal(candidate)" title="삭제">
                    <i class="fas fa-trash-alt text-sm"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 페이지네이션 개선 -->
    <div class="flex justify-center items-center gap-2 mt-8" v-if="totalPages > 1">
      <button @click="goToPage(1)" :disabled="currentPage === 1" 
              class="w-10 h-10 rounded-xl border transition-all duration-200 flex items-center justify-center" 
              :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200' : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300 hover:border-blue-300 shadow-sm hover:shadow-md'">
        <i class="fas fa-angle-double-left"></i>
      </button>
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" 
              class="w-10 h-10 rounded-xl border transition-all duration-200 flex items-center justify-center" 
              :class="currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200' : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300 hover:border-blue-300 shadow-sm hover:shadow-md'">
        <i class="fas fa-chevron-left"></i>
      </button>
      
      <div class="flex items-center gap-1">
        <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" 
                :class="page === currentPage ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg shadow-blue-500/25' : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300 hover:border-blue-300 shadow-sm hover:shadow-md'" 
                class="w-10 h-10 rounded-xl border transition-all duration-200 flex items-center justify-center font-medium">
          {{ page }}
        </button>
      </div>
      
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0" 
              class="w-10 h-10 rounded-xl border transition-all duration-200 flex items-center justify-center" 
              :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200' : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300 hover:border-blue-300 shadow-sm hover:shadow-md'">
        <i class="fas fa-chevron-right"></i>
      </button>
      <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages || totalPages === 0" 
              class="w-10 h-10 rounded-xl border transition-all duration-200 flex items-center justify-center" 
              :class="currentPage === totalPages || totalPages === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200' : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300 hover:border-blue-300 shadow-sm hover:shadow-md'">
        <i class="fas fa-angle-double-right"></i>
      </button>
    </div>

    <!-- 지원자 추가/수정 모달 개선 -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-8 max-w-2xl w-full mx-4 shadow-2xl transform transition-all duration-300 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <i class="fas fa-user-plus text-white text-xl"></i>
            </div>
            <div>
              <h3 class="text-2xl font-bold text-gray-900">
                {{ isEditing ? '지원자 정보 수정' : '새 지원자 추가' }}
              </h3>
              <p class="text-gray-600 text-sm">지원자 정보를 입력해주세요</p>
            </div>
          </div>
          <button @click="closeModal" 
                  class="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-500 hover:text-gray-700 transition-all duration-200 flex items-center justify-center">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-calendar text-blue-500"></i>
              날짜
            </label>
            <input type="date" v-model="form.interviewDate" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-clock text-green-500"></i>
              시간
            </label>
            <input type="time" v-model="form.interviewTime" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-door-open text-purple-500"></i>
              면접실
            </label>
            <input type="text" v-model="form.room" placeholder="예: 회의실A" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-user text-red-500"></i>
              지원자 이름
            </label>
            <input type="text" v-model="form.name" placeholder="이름을 입력하세요" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
          <div class="col-span-2 space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-users text-orange-500"></i>
              면접관 (쉼표로 구분)
            </label>
            <input type="text" v-model="form.interviewersString" placeholder="예: 김민수, 이지원" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-flag text-indigo-500"></i>
              상태
            </label>
            <select v-model="form.status" 
                    class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
              <option value="SCHEDULED">예정</option>
              <option value="IN_PROGRESS">진행중</option>
              <option value="COMPLETED">완료</option>
              <option value="CANCELLED">취소</option>
              <option value="UNDECIDED">미정</option>
            </select>
            <div v-if="form.status" class="mt-2">
              <span :class="{
                'px-3 py-1 text-xs font-medium rounded-full border': true,
                'bg-yellow-50 text-yellow-700 border-yellow-200': form.status === 'SCHEDULED' || form.status === 'UNDECIDED',
                'bg-blue-50 text-blue-700 border-blue-200': form.status === 'IN_PROGRESS',
                'bg-green-50 text-green-700 border-green-200': form.status === 'COMPLETED',
                'bg-gray-50 text-gray-700 border-gray-200': form.status === 'CANCELLED'
              }">{{ getStatusText(form.status) }}</span>
            </div>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700 flex items-center gap-2">
              <i class="fas fa-star text-yellow-500"></i>
              점수 (0-100)
            </label>
            <input type="number" v-model="form.score" min="0" max="100" placeholder="점수를 입력하세요" 
                   class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200">
          </div>
        </div>
        
        <div class="flex justify-end gap-4 mt-8 pt-6 border-t border-gray-100">
          <button @click="closeModal"
                  class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200 font-medium">
            취소
          </button>
          <button @click="isEditing ? updateCandidate() : addCandidate()"
                  class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-200 font-medium shadow-lg shadow-blue-500/25">
            {{ isEditing ? '수정 완료' : '추가하기' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 삭제 모달 개선 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl transform transition-all duration-300">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-exclamation-triangle text-red-600 text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">지원자 삭제</h3>
          <p class="text-gray-600 mb-8">
            정말로 <span class="font-semibold text-gray-900">{{ deletingCandidate?.name }}</span> 지원자를 삭제하시겠습니까?<br>
            이 작업은 되돌릴 수 없습니다.
          </p>
          <div class="flex gap-4">
            <button @click="showDeleteModal = false; deletingCandidate = null"
                    class="flex-1 px-6 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl transition-all duration-200 font-medium">
              취소
            </button>
            <button @click="confirmDeleteCandidate"
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
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';

interface Candidate {
  id: number;
  interviewId: number;
  name: string;
  position: string;
  interviewers: string[];
  status: string;
  interviewDate: string;
  score: number | null;
  interviewTime: string;
  room: string;
}

// 내부 상태로 관리
const candidateList = ref<Candidate[]>([]);

// 개선된 필터 상태
const filters = ref({ 
  status: 'all', 
  interviewDate: '', 
  search: '',
  room: 'all'
});

// 정렬 상태
const sortConfig = ref({
  key: 'interviewDate',
  direction: 'asc' as 'asc' | 'desc'
});

// 모달 상태 및 폼
const showModal = ref(false);
const isEditing = ref(false);
const form = ref<Partial<Candidate & { interviewersString?: string }>>({});

// 삭제 모달 상태
const showDeleteModal = ref(false);
const deletingCandidate = ref<Candidate | null>(null);

// 고유 면접실 목록
const uniqueRooms = computed(() => {
  const rooms = candidateList.value
    .map(c => c.room)
    .filter(room => room && room.trim())
    .filter((room, index, arr) => arr.indexOf(room) === index)
    .sort();
  return rooms;
});

// 활성 필터 여부 확인
const hasActiveFilters = computed(() => {
  return filters.value.status !== 'all' ||
         filters.value.interviewDate !== '' ||
         filters.value.search !== '' ||
         filters.value.room !== 'all';
});

// 목록 fetch 함수
async function fetchCandidates() {
  try {
    const response = await fetch('http://3.38.218.18:8080/api/v1/interviewees/simple');
    if (response.ok) {
      const result = await response.json();
      console.log('서버에서 받아온 최신 목록:', result.data);
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
          interviewId: item.interviewId,
          name: item.name,
          position: item.job,
          interviewers: item.interviewers ? String(item.interviewers).split(',').map((s: string) => s.trim()) : [],
          status: item.status,
          interviewDate,
          score: item.score,
          interviewTime,
          room: item.roomNo
        };
      });
    }
  } catch (error) {
    console.error('데이터 로딩 실패:', error);
    alert('데이터를 불러오는데 실패했습니다.');
  }
}

onMounted(fetchCandidates);

// 개선된 필터링 로직
const filteredCandidates = computed(() => {
  let filtered = [...candidateList.value];
  
  // 상태 필터
  if (filters.value.status !== 'all') {
    filtered = filtered.filter(c => c.status === filters.value.status);
  }
  
  // 날짜 필터
  if (filters.value.interviewDate) {
    filtered = filtered.filter(c => c.interviewDate === filters.value.interviewDate);
  }
  
  // 면접실 필터
  if (filters.value.room !== 'all') {
    filtered = filtered.filter(c => c.room === filters.value.room);
  }
  
  // 검색 필터 - 확장된 검색 범위
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase();
    filtered = filtered.filter(c =>
      c.name.toLowerCase().includes(search) ||
      (c.position && c.position.toLowerCase().includes(search)) ||
      (c.room && c.room.toLowerCase().includes(search)) ||
      c.interviewers.some(interviewer => interviewer.toLowerCase().includes(search))
    );
  }
  
  // 정렬 적용
  return filtered.sort((a, b) => {
    const key = sortConfig.value.key as keyof Candidate;
    const aVal = a[key] ?? '';
    const bVal = b[key] ?? '';
    if (aVal < bVal) return sortConfig.value.direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortConfig.value.direction === 'asc' ? 1 : -1;
    return 0;
  });
});

// 페이징
const itemsPerPage = ref(8);
const currentPage = ref(1);

const pagedCandidates = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return filteredCandidates.value.slice(start, start + itemsPerPage.value);
});

const totalPages = computed(() => Math.ceil(filteredCandidates.value.length / itemsPerPage.value));

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

// 페이지 관련 watcher
watch(itemsPerPage, () => { 
  currentPage.value = 1; 
});

watch(filteredCandidates, () => {
  currentPage.value = 1;
});

const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  if (total <= 5) return Array.from({ length: total }, (_, i) => i + 1);
  if (current <= 3) return [1, 2, 3, 4, 5];
  if (current >= total - 2) return [total - 4, total - 3, total - 2, total - 1, total].filter(p => p > 0);
  return [current - 2, current - 1, current, current + 1, current + 2];
});

// 필터 변경 핸들러
function onFilterChange() {
  currentPage.value = 1;
  console.log('필터 변경됨:', filters.value);
}

// 필터 초기화
function resetFilters() {
  filters.value = {
    status: 'all',
    interviewDate: '',
    search: '',
    room: 'all'
  };
  currentPage.value = 1;
}

// 정렬 함수
function sortBy(key: string) {
  if (sortConfig.value.key === key) {
    sortConfig.value.direction = sortConfig.value.direction === 'asc' ? 'desc' : 'asc';
  } else {
    sortConfig.value.key = key;
    sortConfig.value.direction = 'asc';
  }
}

// 모달 열기/닫기
function openAddModal() {
  isEditing.value = false;
  form.value = {
    status: 'SCHEDULED',
    score: null
  };
  showModal.value = true;
}

function openEditModal(candidate: Candidate) {
  isEditing.value = true;
  form.value = { 
    ...candidate, 
    interviewersString: candidate.interviewers?.join(', ') || ''
  };
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  form.value = {};
}

// 공통 폼 검증 함수
function validateCandidateForm() {
  if (!form.value.name || !form.value.room) {
    alert('지원자 이름과 면접실을 모두 입력해 주세요.');
    return false;
  }
  
  if (!form.value.interviewDate || !form.value.interviewTime) {
    alert('면접 일자와 시간을 모두 입력해 주세요.');
    return false;
  }
  
  return true;
}

// 지원자 추가 함수 (POST)
async function addCandidate() {
  if (!validateCandidateForm()) return;
  
  const interviewersArr = form.value.interviewersString
    ? form.value.interviewersString.split(',').map(s => s.trim()).filter(Boolean)
    : [];
  
  // 날짜와 시간 조합
  const date = form.value.interviewDate || '';
  const time = form.value.interviewTime || '00:00';
  
  // 로컬 시간으로 Date 객체 생성
  const [year, month, day] = date.split('-').map(Number);
  const [hour, minute] = time.split(':').map(Number);
  const localDate = new Date(year, month - 1, day, hour, minute);
  const startAt = localDate.toISOString();
  
  // endAt: startAt에서 30분 추가
  const endDate = new Date(localDate);
  endDate.setMinutes(endDate.getMinutes() + 30);
  const endAt = endDate.toISOString();
  
  const payload = {
    name: form.value.name,
    job: form.value.position || "개발자",
    roomId: form.value.room,
    interviewers: interviewersArr.join(', '),
    startAt,
    endAt,
    score: form.value.score ?? 0,
    status: form.value.status
  };
  
  console.log('지원자 추가 payload:', payload);
  
  try {
    await axios.post('http://3.38.218.18:8080/api/v1/interviewees/interviewee', payload);
    await fetchCandidates();
    closeModal();
    alert('지원자 추가 성공!');
  } catch (e) {
    console.error('지원자 추가 실패:', e);
    alert('지원자 추가 실패');
  }
}

// 지원자 수정 함수 (PUT)
async function updateCandidate() {
  if (!validateCandidateForm()) return;
  
  const interviewersArr = form.value.interviewersString
    ? form.value.interviewersString.split(',').map(s => s.trim()).filter(Boolean)
    : [];
  
  const date = form.value.interviewDate || '';
  const time = form.value.interviewTime || '00:00';
  
  // 날짜 정규화
  const normalizedDate = date.replace(/\./g, '-').replace(/\s/g, '');
  const startAt = `${normalizedDate}T${time}:00`;
  
  // endAt: startAt에서 30분 추가
  const startDateObj = new Date(startAt);
  startDateObj.setMinutes(startDateObj.getMinutes() + 30);
  const endAt = startDateObj.toISOString().replace('Z', '').slice(0, 19);
  
  const payload = {
    name: form.value.name,
    job: form.value.position || " ",
    status: form.value.status,
    startAt,
    endAt,
    interviewers: interviewersArr.join(', '),
    roomName: form.value.room,
    score: form.value.score ?? 0
  };
  
  console.log('지원자 수정 payload:', payload);
  
  try {
    await axios.put(`http://3.38.218.18:8080/api/v1/interviewees/${form.value.id}`, payload);
    await fetchCandidates();
    closeModal();
    alert('지원자 수정 성공!');
  } catch (e) {
    console.error('지원자 수정 실패:', e);
    alert('지원자 수정 실패');
  }
}

// 삭제
function openDeleteModal(candidate: Candidate) {
  deletingCandidate.value = candidate;
  showDeleteModal.value = true;
}

async function confirmDeleteCandidate() {
  if (!deletingCandidate.value) return;
  
  try {
    await axios.delete(`http://3.38.218.18:8080/api/v1/interviews/${deletingCandidate.value.interviewId}/interviewees/${deletingCandidate.value.id}`);
    await fetchCandidates();
    alert('삭제 성공!');
  } catch (e) {
    console.error('삭제 실패:', e);
    alert('삭제 실패');
  } finally {
    showDeleteModal.value = false;
    deletingCandidate.value = null;
  }
}

// 유틸리티 함수들
function formatDate(dateString: string) {
  if (!dateString) return '-';
  
  try {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  } catch {
    return dateString;
  }
}

function getStatusText(status: string) {
  switch ((status || '').toUpperCase()) {
    case 'SCHEDULED': return '예정';
    case 'IN_PROGRESS': return '진행중';
    case 'COMPLETED': return '완료';
    case 'CANCELLED': return '취소';
    case 'UNDECIDED': return '미정';
    default: return status;
  }
}

</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

/* 테이블 호버 효과 개선 */
tbody tr:hover {
  background-color: #f8fafc;
}

/* 필터 태그 호버 효과 */
.px-2.py-1.bg-blue-100:hover {
  background-color: #dbeafe;
}

/* 스크롤바 스타일링 */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>