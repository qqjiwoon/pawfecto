<template>
  <div class="pagination">
    <button
      v-for="page in totalPages"
      :key="page"
      :class="['page-btn', { active: page === currentPage }]"
      @click="$emit('change-page', page)"
    >
      {{ page }}
    </button>

    
    <button
      class="page-btn next-btn"
      :disabled="currentPage === totalPages"
      @click="$emit('change-page', currentPage + 1)"
    >
      Next
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  currentPage: Number,
  totalPages: Number
})
</script>

<style scoped>

.pagination {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 30px;
}

.page-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  background-color: #eee;
  color: #444;
  cursor: pointer;
  transition: 0.2s;
}

.page-btn:hover {
  background-color: #e2e2e2;
}

.page-btn.active {
  background-color: #7E6B5A; 
  color: white;
}

.next-btn {
  background-color: #eee;
}

.next-btn:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
