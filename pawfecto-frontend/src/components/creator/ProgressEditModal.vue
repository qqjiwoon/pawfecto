<!-- ProgresesEditModal.vue -->
<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">

      <button class="close-btn" @click="closeModal">×</button>

      <h2 class="modal-title">Campaign Progress</h2>
      <!-- 캠페인 / 제품 이름 -->
      <div class="campaign-info-box">
        <span class="campaign-label">캠페인 제품</span>
        <p class="campaign-name">
          {{ props.item.campaign_acceptance.campaign.product_name }}
        </p>
      </div>

      <!-- 게시글 내용 -->
      <div class="modal-row">
        <label class="modal-label">게시글 내용</label>
        <textarea
          v-model="content"
          placeholder="게시글 내용을 입력하세요"
          class="modal-textarea"
        />
      </div>

      <!-- 이미지 업로드 -->
      <div class="modal-row">
        <label class="modal-label">이미지 업로드</label>
        <input type="file" @change="onFileChange" />
      </div>

      <!-- AI 검증 -->
      <div v-if="aiResult" class="ai-result-box">
      <h4>AI 검증 결과</h4>
      <ul>
        <li
          v-for="cond in aiResult.conditions"
          :key="cond.requirement"
          :class="cond.satisfied ? 'pass' : 'fail'"
        >
          {{ cond.requirement_type.toUpperCase() }} :
          {{ cond.requirement }}
        </li>
      </ul>

      <p v-if="aiStatus === 'failed'" class="fail-msg">
        필수 조건을 충족하지 못했습니다.
      </p>

      <p v-if="aiStatus === 'passed'" class="pass-msg">
        모든 필수 조건을 충족했습니다 🎉
      </p>
    </div>


      <!-- AI 검증 버튼 -->
      <div class="btn-row">
      <button
        class="save-btn"
        :disabled="aiStatus === 'running'"
        @click="runAIVerification"
      >
        AI 검증받기
      </button>

      <button
        class="submit-btn"
        :disabled="aiStatus !== 'passed'"
        @click="submitDeliverable"
      >
        제출하기
      </button>
    </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/plugins/axios'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})



const emit = defineEmits(['close', 'refresh'])

// AI 검증 상태
const aiStatus = ref('pending') 
// pending | running | passed | failed

const aiResult = ref(null)

// 게시글 내용
const content = ref('')

// 이미지 파일
const imageFile = ref(null)

// 파일 선택 핸들러
const onFileChange = (event) => {
  imageFile.value = event.target.files[0]
}

watch(
  () => props.item,
  (newItem) => {
    // 최초 로딩 시에만 반영
    if (aiResult.value === null) {
      aiStatus.value = newItem.ai_validation_status || 'pending'
      aiResult.value = newItem.ai_result_raw || null
    }
  },
  { immediate: true }
)

const runAIVerification = async () => {
  if (!content.value || !imageFile.value) return

  aiStatus.value = 'running'

  try {
    const res = await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/verify/`
    )

    // 모달이 살아있을 때만 상태 갱신
    if (!props.item) return

    aiResult.value = res.data.ai_result
    aiStatus.value = res.data.ai_validation_status
  } catch (e) {
    aiStatus.value = 'failed'
  }
}



// 모달 닫기
const closeModal = () => {
  emit('close')
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
  width: 520px;
  background: #ffffff;
  border-radius: 20px;
  padding: 64px 56px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
  animation: fadeIn 0.2s ease-out;
  position: relative;
}

.modal-container,
.modal-container * {
  box-sizing: border-box;
}

/* 닫기 버튼 */
.close-btn {
  position: absolute;
  top: 18px;
  right: 22px;
  background: none;
  border: none;
  font-size: 26px;
  color: #777;
  cursor: pointer;
}

.close-btn:hover {
  color: #000;
}

/* 제목 */
.modal-title {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 36px;
  color: #222;
}

/* 입력 블록 */
.modal-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 22px;
}

.modal-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

/* textarea */
.modal-textarea {
  min-height: 140px;
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid #7d6c61;
  font-size: 14px;
  resize: none;
  outline: none;
  line-height: 1.6;
}

.modal-textarea:focus {
  border-color: #7d6c61;
  background-color: #fafafa;
}

/* 파일 업로드 */
.modal-row input[type="file"] {
  padding: 10px;
  border-radius: 12px;
  border: 1px dashed #7d6c61;
  font-size: 13px;
  cursor: pointer;
  background-color: #fafafa;
}

/* 버튼 영역 */
.btn-row {
  display: flex;
  justify-content: center;
  margin-top: 42px;
}

/* AI 검증 버튼 */
.save-btn {
  width: 180px;
  padding: 14px 0;
  background: #7d6c61;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
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

/* 캠페인 정보 박스 */
.campaign-info-box {
  /* background-color: #f8f8f8; */
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 26px;
  text-align: center;
}

.campaign-label {
  display: block;
  font-size: 12px;
  color: #7d6c61;
  margin-bottom: 6px;
}

.campaign-name {
  font-size: 16px;
  font-weight: 600;
  color: #4c3d2c;
  line-height: 1.4;
}

/* AI 검증 */
.ai-result-box {
  margin-top: 24px;
  padding: 16px;
  border-radius: 12px;
  background: #fafafa;
  font-size: 14px;
}

.ai-result-box ul {
  list-style: none;
  padding: 0;
}

.ai-result-box li.pass {
  color: #1ea35a;
}

.ai-result-box li.fail {
  color: #d93232;
}

.pass-msg {
  margin-top: 12px;
  color: #1ea35a;
  font-weight: 600;
}

.fail-msg {
  margin-top: 12px;
  color: #d93232;
  font-weight: 600;
}

/* 제출 버튼 */
.submit-btn {
  width: 180px;
  padding: 14px 0;
  margin-left: 12px;
  background: #1ea35a;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.submit-btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

</style>
