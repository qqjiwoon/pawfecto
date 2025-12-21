<!-- ProgresesEditModal.vue -->
<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">

      <button class="close-btn" @click="closeModal">×</button>

      <h2 class="modal-title">Campaign Progress</h2>

      <!-- 👇 스크롤 영역 -->
      <div class="modal-content">
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

        <!-- 이미지 미리보기 -->
        <div v-if="imagePreviewUrl" class="image-preview">
          <img :src="imagePreviewUrl" alt="업로드 이미지 미리보기" />
        </div>

        <!-- AI 검증 -->
        <div v-if="aiStatus !== 'pending'" class="ai-result-box">
          <h4>AI 검증 결과</h4>

          <!-- 진행 바 -->
          <div v-if="aiStatus === 'running'" class="ai-progress">
            <div class="bar">
              <div class="fill" />
            </div>
            <p class="progress-text">AI가 콘텐츠를 분석 중입니다...</p>
          </div>

          <!-- 체크 리스트 -->
          <ul v-if="aiResult && aiStatus !== 'running'" class="ai-checklist">
            <li
              v-for="cond in aiResult.conditions"
              :key="cond.requirement"
              :class="{
                pass: cond.satisfied === 'yes',
                review: cond.satisfied === 'uncertain',
                fail: cond.satisfied === 'no'
              }"
            >
              <div class="check-main">
                <span class="icon">
                  <template v-if="cond.satisfied === 'yes'">✔</template>
                  <template v-else-if="cond.satisfied === 'uncertain'">⚠</template>
                  <template v-else>✖</template>
                </span>

                <span class="text">
                  {{ cond.requirement }}
                </span>
              </div>

              <!-- 실패 / 불확실 사유 -->
              <p
                v-if="cond.satisfied !== 'yes' && cond.reason"
                class="fail-reason"
              >
                {{ cond.reason }}
              </p>
            </li>
          </ul>

          <!-- 최종 상태 메시지 -->
          <p v-if="aiStatus === 'failed'" class="fail-msg">
            일부 조건이 충족되지 않았습니다. 아래 항목을 보완해주세요.
          </p>

          <p v-else-if="aiStatus === 'review'" class="review-msg">
            일부 조건이 명확하지 않습니다. 보완 시 통과될 수 있습니다.
          </p>

          <p v-else-if="aiStatus === 'passed'" class="pass-msg">
            모든 조건을 충족했습니다 🎉
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
const imagePreviewUrl = ref(null)

// 파일 선택 핸들러
const onFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  imageFile.value = file

  // 미리보기 URL 생성
  imagePreviewUrl.value = URL.createObjectURL(file)
}

watch(
  () => props.item,
  (newItem) => {
    if (!newItem) return

    // 서버 값으로 초기화
    content.value = newItem.content || ''
    imagePreviewUrl.value = newItem.image || null

    aiStatus.value = newItem.ai_validation_status || 'pending'
    aiResult.value = newItem.ai_result_raw || null
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

    aiResult.value = res.data.ai_result
    aiStatus.value = res.data.ai_validation_status
  } catch (e) {
    aiStatus.value = 'failed'
  }
}

const submitDeliverable = async () => {
  try {
    const res = await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/submit/`
    )

    // 제출 성공 시
    emit('refresh')  
  } catch (e) {
    alert(e.response?.data?.error || '제출에 실패했습니다.')
  }
}

// 모달 닫기
const closeModal = () => {
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value)
  }
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
  max-height: 90vh;        
  background: #ffffff;
  border-radius: 20px;
  padding: 48px 56px 36px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 6px;   /* 스크롤바 겹침 방지 */
}

.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #cfcfcf;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
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

/* 이미지 미리보기 */
.image-preview {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 220px;
  border-radius: 14px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  margin-top: 28px;
  padding: 18px;
  border-radius: 14px;
  background: #fafafa;
  font-size: 14px;
}

/* Progress Bar */
.ai-progress {
  margin-top: 10px;
}

.ai-progress .bar {
  height: 8px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.ai-progress .fill {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #7d6c61, #1ea35a);
  animation: loading 1.4s infinite;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-text {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
  text-align: center;
}

/* 체크리스트 */
.ai-checklist li {
  margin-bottom: 12px;
}

/* 메인 라인 */
.check-main {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-checklist li.pass {
  color: #1ea35a;
  font-weight: 600;
}

.ai-checklist li.fail {
  color: #d93232;
  font-weight: 600;
}

/* 실패 이유 */
.fail-reason {
  margin-top: 4px;
  margin-left: 26px; /* 아이콘 들여쓰기 */
  font-size: 13px;
  color: #666;
  line-height: 1.5;
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
.btn-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

</style>
