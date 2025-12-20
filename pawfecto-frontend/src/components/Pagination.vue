<template>
  <div class="pagination">
    <button
      class="page-btn"
      :disabled="currentPage === 1"
      @click="$emit('change-page', currentPage - 1)"
    >
      ← Previous
    </button>

    <div class="pages">
      <span
        v-for="n in totalPages"
        :key="n"
        :class="['page-number', { active: n === currentPage }]"
        @click="$emit('change-page', n)"
      >
        {{ n }}
      </span>
    </div>

    <button
      class="page-btn"
      :disabled="currentPage === totalPages"
      @click="$emit('change-page', currentPage + 1)"
    >
      Next →
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

defineEmits(['change-page'])
</script>

<style scoped>
/* 페이지네이션 전체 컨테이너 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
  margin-bottom: 40px;
  gap: 20px;
}

/* Previous, Next 버튼 디자인 */
.page-btn {
  background: white;
  border: 1px solid #d1d1d1;
  padding: 8px 16px;
  border-radius: 20px; /* 타원형 라운드 */
  font-size: 14px;
  color: #444;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: #f9f9f9;
  border-color: #bbb;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 숫자 번호 영역 */
.pages {
  display: flex;
  gap: 12px;
}

.page-number {
  padding: 4px 8px;
  cursor: pointer;
  color: #999; /* 기본적으로 흐린 색 */
  font-size: 15px;
  transition: color 0.2s ease;
}

.page-number:hover {
  color: #222;
}

/* 활성화된 숫자 디자인 (검은색 굵게) */
.page-number.active {
  font-weight: 700;
  color: #000;
  cursor: default;
}
</style>
