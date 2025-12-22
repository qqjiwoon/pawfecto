<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">

      <!-- 닫기 버튼 -->
      <button class="close-btn" @click="closeModal">×</button>

      <h2 class="modal-title">Campaign Progress</h2>

      <div class="modal-content">

        <!-- 캠페인 정보 -->
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

        <!-- 🔄 AI 진행 상태 -->
        <div v-if="aiStatus === 'running'" class="ai-progress-box">
          <div class="progress-step" :class="{ active: aiPhase === 'content' }">
            ✏️ 게시글 내용 검증 중
          </div>
          <div class="progress-step" :class="{ active: aiPhase === 'image' }">
            🖼️ 이미지 분석 중
          </div>
          <div class="progress-step" :class="{ active: aiPhase === 'rule' }">
            📋 캠페인 조건 비교 중
          </div>
          <div class="progress-step" :class="{ active: aiPhase === 'final' }">
            🤖 결과 정리 중
          </div>

          <div class="progress-bar">
            <div class="progress-fill" />
          </div>
        </div>

        <!-- ✅ AI 결과 -->
        <div v-if="aiStatus !== 'pending' && aiStatus !== 'running'" class="ai-result-box modern">

          <!-- 요약 카드 -->
          <div class="ai-summary" :class="aiStatus">
            <span class="icon">
              <template v-if="aiStatus === 'passed'">🎉</template>
              <template v-else-if="aiStatus === 'review'">⚠️</template>
              <template v-else>❌</template>
            </span>

            <div class="summary-text">
              <p class="title">
                <template v-if="aiStatus === 'passed'">AI 검증 통과</template>
                <template v-else-if="aiStatus === 'review'">보완이 필요합니다</template>
                <template v-else>검증 실패</template>
              </p>
              <p class="desc">
                <template v-if="aiStatus === 'passed'">
                  콘텐츠가 캠페인 조건을 충족했습니다.
                </template>
                <template v-else>
                  아래 항목을 보완하면 통과될 수 있습니다.
                </template>
              </p>
            </div>
          </div>

          <!-- 실패 / 불확실 항목만 표시 -->
          <ul v-if="aiStatus !== 'passed'" class="ai-issues">
            <li
              v-for="cond in aiResult.conditions.filter(c => c.satisfied !== 'yes')"
              :key="cond.requirement"
            >
              <strong>{{ cond.requirement }}</strong>
              <p>{{ cond.reason }}</p>
            </li>
          </ul>

        </div>

        <!-- 🔘 버튼 영역 -->
        <div class="btn-row">
          <button
            v-if="aiStatus !== 'passed'"
            class="save-btn"
            :disabled="aiStatus === 'running'"
            @click="runAIVerification"
          >
            AI 검증받기
          </button>

          <button
            v-if="aiStatus === 'passed'"
            class="submit-btn"
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

/**
 * props.item
 * - campaign_acceptance, deliverable 정보 포함
 * - 서버에서 내려온 현재 진행 상태 기반으로 UI 초기화
 */
const props = defineProps({
  item: { type: Object, required: true }
})

const emit = defineEmits(['close', 'refresh'])

/**
 * AI 검증 전체 상태
 * - pending : 아직 검증 전
 * - running : AI 검증 중 (progress UI 표시)
 * - passed  : 검증 통과
 * - review  : 보완 필요
 * - failed  : 검증 실패
 */
const aiStatus = ref('pending')

/**
 * AI 검증 결과 원본
 * - conditions 배열을 사용해 실패/불확실 항목 표시
 */
const aiResult = ref(null)

/**
 * 게시글 내용 / 이미지 상태
 */
const content = ref('')
const imageFile = ref(null)
const imagePreviewUrl = ref(null)

/**
 * AI 진행 단계 (UX용, 서버와 무관)
 * - content → image → rule → final
 */
const aiPhase = ref(null)

/**
 * 파일 선택 시 미리보기 생성
 */
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  imageFile.value = file
  imagePreviewUrl.value = URL.createObjectURL(file)
}

/**
 * props 변경 시 서버 상태로 UI 동기화
 */
watch(
  () => props.item,
  (item) => {
    if (!item) return
    content.value = item.content || ''
    imagePreviewUrl.value = item.image || null
    aiStatus.value = item.ai_validation_status || 'pending'
    aiResult.value = item.ai_result_raw || null
  },
  { immediate: true }
)

/**
 * AI 검증 실행
 * - 실제로는 단일 API 호출
 * - UX를 위해 단계별 진행 상태를 시뮬레이션
 */
const runAIVerification = async () => {
  if (!content.value || !imageFile.value) return

  aiStatus.value = 'running'
  aiPhase.value = 'content'

  // UX용 단계 시뮬레이션
  setTimeout(() => (aiPhase.value = 'image'), 700)
  setTimeout(() => (aiPhase.value = 'rule'), 1400)
  setTimeout(() => (aiPhase.value = 'final'), 2100)

  try {
    const res = await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/verify/`
    )
    aiResult.value = res.data.ai_result
    aiStatus.value = res.data.ai_validation_status
  } catch {
    aiStatus.value = 'failed'
  } finally {
    aiPhase.value = null
  }
}

/**
 * Deliverable 최종 제출
 * - AI 검증 passed 상태에서만 노출됨
 */
const submitDeliverable = async () => {
  try {
    await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/submit/`
    )
    emit('refresh')
    closeModal()
  } catch (e) {
    alert(e.response?.data?.error || '제출에 실패했습니다.')
  }
}

/**
 * 모달 닫기 + ObjectURL 정리
 */
const closeModal = () => {
  if (imagePreviewUrl.value) URL.revokeObjectURL(imagePreviewUrl.value)
  emit('close')
}
</script>

<style scoped>
/* ================================
   Overlay & Modal
================================ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

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
  padding-right: 6px;
}

.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

/* ================================
   Header
================================ */
.close-btn {
  position: absolute;
  top: 18px;
  right: 22px;
  border: none;
  background: none;
  font-size: 26px;
  cursor: pointer;
  color: #777;
}

.close-btn:hover {
  color: #111;
}

.modal-title {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 36px;
  color: #111827;
}

/* ================================
   Campaign Info
================================ */
.campaign-info-box {
  text-align: center;
  margin-bottom: 28px;
}

.campaign-label {
  font-size: 12px;
  color: #7d6c61;
}

.campaign-name {
  font-size: 16px;
  font-weight: 600;
  color: #4c3d2c;
  margin-top: 6px;
}

/* ================================
   Form
================================ */
.modal-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 22px;
}

.modal-label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
}

.modal-textarea {
  min-height: 140px;
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid #d1d5db;
  font-size: 14px;
  line-height: 1.6;
  resize: none;
}

.modal-textarea:focus {
  outline: none;
  border-color: #7d6c61;
  background: #fafafa;
}

.modal-row input[type="file"] {
  padding: 10px;
  border-radius: 12px;
  border: 1px dashed #7d6c61;
  font-size: 13px;
  background: #fafafa;
  cursor: pointer;
}

/* ================================
   Image Preview
================================ */
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
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
}

/* ================================
   AI Progress (Running)
================================ */
.ai-progress-box {
  margin-top: 26px;
  padding: 18px;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

.progress-step {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 6px;
  transition: color 0.3s;
}

.progress-step.active {
  color: #111827;
  font-weight: 600;
}

.progress-bar {
  margin-top: 14px;
  height: 6px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    #7d6c61,
    #1ea35a,
    #7d6c61
  );
  animation: progressMove 1.6s linear infinite;
}

@keyframes progressMove {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* ================================
   AI Result (Modern)
================================ */
.ai-result-box.modern {
  margin-top: 28px;
  padding: 20px;
  border-radius: 16px;
  background: #f9fafb;
}

.ai-summary {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 14px;
}

.ai-summary.passed {
  background: #ecfdf3;
  color: #027a48;
}

.ai-summary.review {
  background: #fffaeb;
  color: #b54708;
}

.ai-summary.failed {
  background: #fef3f2;
  color: #b42318;
}

.ai-summary .icon {
  font-size: 28px;
}

.summary-text .title {
  font-size: 16px;
  font-weight: 700;
}

.summary-text .desc {
  font-size: 13px;
  opacity: 0.85;
}

/* 문제 항목 */
.ai-issues {
  list-style: none;
  padding: 0;
  margin-top: 16px;
}

.ai-issues li {
  background: #ffffff;
  border-radius: 12px;
  padding: 12px 14px;
  border: 1px solid #eee;
  margin-bottom: 10px;
}

.ai-issues strong {
  font-size: 14px;
  display: block;
  margin-bottom: 4px;
}

.ai-issues p {
  font-size: 13px;
  color: #555;
}

/* ================================
   Buttons
================================ */
.btn-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
}

.save-btn {
  width: 180px;
  padding: 14px 0;
  border-radius: 999px;
  background: #7d6c61;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

.save-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.submit-btn {
  width: 180px;
  padding: 14px 0;
  border-radius: 999px;
  background: #1ea35a;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}
</style>
