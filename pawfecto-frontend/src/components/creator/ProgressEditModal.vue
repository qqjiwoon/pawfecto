<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">

      <button class="close-btn" @click="closeModal">×</button>

      <h2 class="modal-title">Campaign Progress</h2>

      <!-- 제품명 -->
      <div class="modal-row">
        <label class="modal-label">제품</label>
        <p class="modal-value">{{ localItem.campaign_name }}</p>
      </div>

      <!-- 업로드 일시 -->
      <div class="modal-row">
        <label class="modal-label">업로드 일시</label>
        <input
          type="date"
          v-model="localItem.upload_date"
          class="modal-input"
        />
      </div>

      <!-- 포스팅 링크 -->
      <div class="modal-row">
        <label class="modal-label">포스팅 링크</label>
        <input
          type="text"
          v-model="localItem.post_link"
          placeholder="https://www.instagram.com/..."
          class="modal-input"
        />
      </div>

      <!-- 저장 버튼 -->
      <div class="btn-row">
        <button class="save-btn" @click="save">SAVE</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['save', 'close'])

const localItem = ref({})

watch(
  () => props.item,
  (val) => {
    if (val) {
      localItem.value = { ...val }
    }
  },
  { immediate: true }
)

const save = () => {
  const hasAllValues = localItem.value.upload_date && localItem.value.post_link

  // ERD 기준 상태값 통일
  localItem.value.status = hasAllValues ? "completed" : "incomplete"

  emit("save", localItem.value)
}

const closeModal = () => {
  emit("close")
}


</script>

<style scoped>
/* 오버레이 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

/* 모달 박스 */
.modal-container {
  width: 500px;
  background: #ffffff;
  border-radius: 16px;
  padding: 80px 70px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.2s ease-out;
  position: relative; /* X 버튼의 기준점 생성 */
}

.modal-container,
.modal-container * {
  box-sizing: border-box;
}

/* X 버튼 */
.close-btn {
  position: absolute;
  top: 16px;
  right: 20px;
  background: none;
  border: none;
  font-size: 26px;
  color: #555;
  cursor: pointer;
  line-height: 1;
  padding: 0;
}

.close-btn:hover {
  color: #000;
}


/* 제목 */
.modal-title {
  text-align: center;
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 50px;
  color: #222;
}

/* 행 구조 */
.modal-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
}

.modal-label {
  font-size: 15px;
  color: #444;
  margin-bottom: 6px;
}

.modal-value {
  font-size: 15px;
  color: #222;
}

/* 입력창 */
.modal-input {
  border: 1px solid #ddd;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  width: 100%;
  outline: none;
}

.modal-input:focus {
  border-color: #bbb;
}

/* 버튼 영역 */
.btn-row {
  display: flex;
  justify-content: center;
  margin-top: 50px;
  margin-bottom: 20px;
}

.save-btn {
  width: 160px;
  padding: 12px 0;
  background: #333;
  color: white;
  font-size: 15px;
  border-radius: 24px;
  border: none;
  cursor: pointer;
}

.save-btn:hover {
  background: #111;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
