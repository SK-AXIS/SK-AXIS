<template>
  <div class="fixed inset-0 bg-white z-50 overflow-auto">
    <div class="container mx-auto px-4 py-6">
      <!-- 헤더 개선 -->
      <div class="flex justify-between items-center mb-8">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center shadow-lg">
            <i class="fas fa-video text-white text-lg"></i>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-gray-900">면접 진행</h3>
            <p class="text-gray-600 text-sm">AI 면접 시스템</p>
          </div>
        </div>
        <button @click="close" class="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-xl flex items-center justify-center transition-all duration-200 group">
          <i class="fas fa-times text-gray-600 group-hover:text-gray-800"></i>
        </button>
      </div>

      <!-- 면접 정보 카드 개선 -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-red-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-door-open text-red-600 text-lg"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">면접실</p>
              <p class="text-lg font-bold text-gray-900">{{ roomName }}</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-clock text-blue-600 text-lg"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">시간</p>
              <p class="text-lg font-bold text-gray-900">{{ timeRange }}</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center">
              <i class="fas fa-users text-green-600 text-lg"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">면접관</p>
              <p class="text-lg font-bold text-gray-900">{{ interviewers }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mb-8">
        <!-- 질문 영역 개선 -->
        <div v-if="Object.keys(questionsPerInterviewee).length > 0" class="grid" :class="[candidates.length > 1 ? 'grid-cols-2 gap-6' : 'grid-cols-1']">
          <div v-for="(candidate, index) in candidates" :key="index" class="bg-white rounded-2xl shadow-lg border border-gray-100">
            
            <!-- 지원자 헤더 -->
            <div class="bg-gray-50 px-6 py-4 rounded-t-2xl border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-lg font-bold text-gray-900">{{ candidate }}님</h4>
                  <p class="text-sm text-gray-500">지원자 {{ index + 1 }}</p>
                </div>
                <div class="px-3 py-1 bg-white border border-gray-200 text-gray-600 rounded-full text-sm font-medium">
                  {{ questionsPerInterviewee[candidateIds[index]]?.length || 0 }}개 질문
                </div>
              </div>
            </div>

            <!-- 질문 목록 -->
            <div class="p-6">
              <div v-if="Object.keys(questionsPerInterviewee).length === 0" class="text-center py-8">
                <i class="fas fa-spinner fa-spin text-2xl text-gray-400 mb-4"></i>
                <p class="text-gray-600">질문을 불러오는 중...</p>
              </div>
              
              <div v-else class="space-y-4">
                <div v-for="(question, qIndex) in questionsPerInterviewee[candidateIds[index]]" 
                     :key="question.questionId" 
                     class="flex items-start gap-4 p-4 bg-gray-50 rounded-xl border border-gray-100 hover:bg-gray-100 transition-colors">
                  
                  <!-- 질문 번호 -->
                  <div class="flex-shrink-0 w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center">
                    <span class="text-white text-sm font-bold">{{ qIndex + 1 }}</span>
                  </div>
                  
                  <!-- 질문 내용 -->
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium"
                            :class="{
                              'bg-blue-100 text-blue-700 border border-blue-200': question.type === '공통질문',
                              'bg-orange-100 text-orange-700 border border-orange-200': question.type !== '공통질문'
                            }">
                        {{ question.type === '공통질문' ? '공통 질문' : '개별 질문' }}
                      </span>
                    </div>
                    <p class="text-gray-800 leading-relaxed font-medium">{{ question.content }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 버튼 영역 개선 -->
        <div class="flex flex-wrap justify-center gap-4 mt-10">
          <button
            class="group px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg flex items-center gap-3 min-w-[160px] justify-center"
            :class="{
              'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-green-500/25 hover:shadow-green-500/40': !isSessionStarted,
              'bg-gray-400 text-gray-200 cursor-not-allowed shadow-gray-400/25': isSessionStarted
            }"
            @click="startSession"
            :disabled="isSessionStarted"
          >
            <div class="flex items-center justify-center w-5 h-5">
              <i class="fas fa-play text-sm" :class="{ 'animate-pulse': isSessionStarted }"></i>
            </div>
            <span>{{ isSessionStarted ? '면접 진행 중' : '면접 시작' }}</span>
          </button>
          
          <button
            class="group px-8 py-4 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white rounded-xl font-semibold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg shadow-red-500/25 hover:shadow-red-500/40 flex items-center gap-3 min-w-[160px] justify-center"
            @click="endSession"
          >
            <div class="flex items-center justify-center w-5 h-5">
              <i class="fas fa-stop text-sm group-hover:scale-110 transition-transform"></i>
            </div>
            <span>면접 종료</span>
          </button>
          
          <button
            class="group px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 hover:border-gray-400 font-semibold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg hover:shadow-xl flex items-center gap-3 min-w-[160px] justify-center"
            @click="close"
          >
            <div class="flex items-center justify-center w-5 h-5">
              <i class="fas fa-times text-sm group-hover:scale-110 transition-transform"></i>
            </div>
            <span>취소</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 우측 하단 실시간 캠/분석 오버레이 (480x270픽셀 고정) -->
    <div
      class="fixed bottom-4 right-4 bg-gray-900 rounded-lg overflow-hidden shadow-lg z-50 flex items-center justify-center"
      style="width:480px; aspect-ratio:4/3; pointer-events:none;">
      <PoseMiniWidget 
        ref="poseMiniWidgetRef"
        :intervieweeNames="candidates"
        :intervieweeIds="candidateIds"
        @updateNonverbalData="handleNonverbalData"
        style="width:100%; height:100%;" 
      />
    </div>

    <!-- AI 로딩 모달 -->
    <AiLoadingModal v-if="isAnalyzing" />
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AiLoadingModal from './AiLoadingModal.vue'
import PoseMiniWidget from './PoseMiniWidget.vue'

interface Props {
  roomName: string
  timeRange: string
  interviewers: string
  candidates: string[]
  candidateIds: number[]
  interviewerIds: number[]
}

const props = withDefaults(defineProps<Props>(), {
  roomName: '',
  timeRange: '',
  interviewers: '',
  candidates: () => [],
  candidateIds: () => [],
  interviewerIds: () => []
})

type Emits = {
  (e: 'startSession'): void
  (e: 'endSession'): void
  (e: 'close'): void
}

const emit = defineEmits<Emits>()

const router = useRouter()
const route = useRoute()
const isAnalyzing = ref(false)
const isSessionStarted = ref(false)

// PoseMiniWidget ref 추가
const poseMiniWidgetRef = ref<InstanceType<typeof PoseMiniWidget> | null>(null)

// 비언어적 데이터 저장소
const nonverbalData = ref<Record<number, any>>({})

// 질문 데이터를 저장할 상태
const questionsPerInterviewee = ref<Record<number, any[]>>({})

const interviewId = computed(() => Number(route.query.interview_id))

// PoseMiniWidget으로부터 비언어적 데이터 업데이트
const handleNonverbalData = (data: Record<string, any>) => {
  // string 키를 number로 변환
  const convertedData: Record<number, any> = {}
  Object.entries(data).forEach(([key, value]) => {
    convertedData[Number(key)] = value
  })
  nonverbalData.value = convertedData
}

const startSession = async () => {
  try {
    // isAnalyzing.value = true; // 로딩 모달 제거
    // FastAPI 서버에 면접 시작 요청
    const token = localStorage.getItem('accessToken');
    
    const requestBody = {
      intervieweeIds: props.candidateIds
    };
    
    const response = await fetch('http://3.38.218.18:8080/api/v1/interviews/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      },
      body: JSON.stringify(requestBody)
    })

    if (!response.ok) {
      const contentType = response.headers.get('content-type')
      
      let errorMessage = '면접 시작 실패'
      try {
        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } else {
          const text = await response.text()
          errorMessage = `서버 오류 (${response.status}): ${text}`
        }
      } catch (e) {
        errorMessage = `서버 오류 (${response.status})`
      }
      throw new Error(errorMessage)
    }

    // 성공 응답 처리
    const contentType = response.headers.get('content-type')
    
    let result;
    if (contentType && contentType.includes('application/json')) {
      result = await response.json()
    } else {
      const text = await response.text()
      // 텍스트 응답인 경우 기본 구조로 변환
      result = {
        questionsPerInterviewee: {},
        message: text
      }
    }
    
    // 질문 데이터 저장
    questionsPerInterviewee.value = result.questionsPerInterviewee || {}
    isSessionStarted.value = true  // 면접 시작 상태로 변경
    emit('startSession')  // 면접 시작 이벤트 발생

    // === 감지 시작 명령 추가 ===
    if (poseMiniWidgetRef.value) {
      poseMiniWidgetRef.value.startDetection()
    }
  } catch (error: unknown) {
    // isAnalyzing.value = false; // 로딩 모달 제거
    alert('면접 시작 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)))
  }
}

const endSession = async () => {
  try {
    isAnalyzing.value = true;
    console.log('면접 종료...', { nonverbalData: nonverbalData.value });

    // PoseMiniWidget 감지 중단
    if (poseMiniWidgetRef.value) {
      poseMiniWidgetRef.value.stopDetection();
    }

    // FastAPI 서버에 면접 종료 요청
    const rawNonverbalData = JSON.parse(JSON.stringify(nonverbalData.value));
    const requestBody = {
      interview_id: interviewId.value,
      data: Object.fromEntries(
        props.candidateIds.map((id) => {
          const data = rawNonverbalData[id] || {
            posture: { upright: 0, leaning: 0, slouching: 0 },
            facial_expression: { smile: 0, neutral: 0, frown: 0, angry: 0 },
            gaze: 0,
            gesture: 0,
            timestamp: Date.now()
          };
          return [id, data];
        })
      )
    };
    console.log('[면접 종료] 전송되는 request body:', requestBody);
    const response = await fetch('/api/ai/interview/end', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const contentType = response.headers.get('content-type');
      let errorMessage = '면접 종료 실패';
      try {
        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } else {
          const text = await response.text();
          console.error('서버 응답 (JSON이 아님):', text);
          errorMessage = `서버 오류 (${response.status}): ${text}`;
        }
      } catch (e) {
        console.error('에러 응답 파싱 실패:', e);
        errorMessage = `서버 오류 (${response.status})`;
      }
      throw new Error(errorMessage);
    }

    // === 여기서 폴링 시작 ===
    await pollUntilDone(props.candidateIds);

    // 결과 페이지로 이동
    router.push({
      name: 'result',
      query: {
        candidates: JSON.stringify(props.candidates),
        candidateIds: JSON.stringify(props.candidateIds),
        tab: '0'
      }
    });
  } catch (error) {
    console.error('면접 종료 중 오류:', error);
    alert('면접 종료 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
  } finally {
    isAnalyzing.value = false;
  }
};

// 폴링 함수 추가
async function pollUntilDone(candidateIds: number[]) {
  const ids = candidateIds.join(',');
  let attempts = 0;
  const maxAttempts = 300; // 최대 5분 대기 (300초)
  
  while (attempts < maxAttempts) {
    try {
      const response = await fetch(`http://3.38.218.18:8000/api/ai/results/statuses?interviewee_ids=${ids}`);
      const statuses: { status: string }[] = await response.json();
      console.log('[pollUntilDone] 현재 status 응답:', statuses);
      const allDone = statuses.every((item: { status: string }) => item.status === 'DONE');
      if (allDone) {
        console.log('[pollUntilDone] 모든 면접자의 status가 DONE입니다.');
        
        // ✅ Spring Boot /complete 엔드포인트 호출 추가
        try {
          const completeResponse = await fetch('http://3.38.218.18:8080/api/v1/interviews/complete', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              intervieweeIds: candidateIds
            })
          });
          
          if (completeResponse.ok) {
            console.log('[pollUntilDone] Spring Boot /complete 호출 성공');
          } else {
            console.error('[pollUntilDone] Spring Boot /complete 호출 실패:', completeResponse.status);
          }
        } catch (error) {
          console.error('[pollUntilDone] Spring Boot /complete 호출 중 오류:', error);
        }
        
        break;
      }
    } catch (e) {
      // 네트워크 오류 등은 무시하고 재시도
    }
    await new Promise(res => setTimeout(res, 1000));
    attempts++;
  }
  
  if (attempts >= maxAttempts) {
    console.warn('[pollUntilDone] 최대 대기 시간을 초과했습니다.');
  }
}

const close = () => {
  router.push('/')
}

// 컴포넌트 마운트 시 자동으로 질문 로드
// onMounted(() => {
//   startSession()
// })
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
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>