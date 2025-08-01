<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white/95 backdrop-blur-xl rounded-2xl p-10 max-w-md w-full mx-4 text-center shadow-2xl border border-white/20">
      <div class="mb-8">
        <div class="relative w-20 h-20 mx-auto mb-6">
          <!-- 외부 회전 링 -->
          <div class="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
          <div class="absolute inset-0 border-4 border-t-red-500 border-r-orange-500 border-b-transparent border-l-transparent rounded-full animate-spin"></div>
          <!-- 내부 아이콘 -->
          <div class="absolute inset-0 flex items-center justify-center">
            <i class="fas fa-brain text-red-600 text-2xl"></i>
          </div>
        </div>
        
        <h3 class="text-xl font-bold mb-3">
          <span class="text-red-600">SK</span><span class="text-orange-500">AXIS</span>가
          <span class="text-gray-900">면접 결과를 분석 중입니다...</span>
        </h3>
        <p class="text-gray-600">AI가 면접 내용을 평가하고 있습니다</p>
      </div>
      
      <div class="w-full bg-gray-200 h-3 rounded-full overflow-hidden">
        <div class="loading-progress bg-gradient-to-r from-red-600 to-orange-500 h-full rounded-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 아무 props/state 필요 없음(타이머 등은 부모가 관리)
</script>

<style scoped>
@keyframes loading {
  0% { width: 0; }
  100% { width: 100%; }
}

.loading-progress {
  animation: loading 10s linear forwards;
}

/* 부드러운 회전 애니메이션 */
.animate-spin {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>