<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">

      <transition name="fade">
        <div v-if="toast.visible" class="toast-message" :class="toast.type">
          {{ toast.message }}
        </div>
      </transition>

      <button class="close-btn" @click="closeModal">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <div class="modal-header-top">
        <h2>Campaign Progress</h2>
      </div>

      <div class="modal-body">
        
        <div class="left-section">
          <div 
            class="upload-box dashed-box" 
            :class="{ 'has-image': imagePreviewUrl }" 
            @click="triggerFileInput"
          >
            <div v-if="imagePreviewUrl" class="image-wrapper">
               <img :src="imagePreviewUrl" class="preview-img" alt="Preview" />
               <div class="hover-overlay">
                 <span>변경하기</span>
               </div>
            </div>
            
            <div v-else class="placeholder-content">
              <div class="plus-sign">+</div>
              <span class="upload-label">이미지 업로드</span>
            </div>

            <input ref="fileInputRef" type="file" accept="image/*" class="hidden-input" @change="onFileChange" />
          </div>
        </div>

        <div class="right-section">
          
          <div class="product-info">
            <span class="label">Product</span>
            <span class="product-name">{{ props.item.campaign_acceptance.campaign.product_name }}</span>
          </div>

          <div class="input-area">
            <label class="section-label">게시글 내용</label>
            <textarea
              v-model="content"
              class="modern-textarea custom-scroll"
              placeholder="내용을 입력해주세요..."
              @input="onContentChange"
            ></textarea>
          </div>

          <div v-if="aiStatus === 'running'" class="process-visualizer">
            <p class="process-text">AI가 꼼꼼히 살펴보고 있어요...</p>
            <div class="steps-container">
              <div class="step" :class="{ active: aiPhase === 'content' || aiPhase === 'done' }">
                <div class="icon">✏️</div>
                <span>내용</span>
              </div>
              <div class="line"></div>
              <div class="step" :class="{ active: aiPhase === 'image' || aiPhase === 'done' }">
                <div class="icon">🖼️</div>
                <span>이미지</span>
              </div>
              <div class="line"></div>
              <div class="step" :class="{ active: aiPhase === 'rule' || aiPhase === 'done' }">
                <div class="icon">📋</div>
                <span>규칙</span>
              </div>
              <div class="line"></div>
              <div class="step" :class="{ active: aiPhase === 'done' }">
                <div class="icon">🤖</div>
                <span>결과</span>
              </div>
            </div>
          </div>

          <div v-if="aiStatus === 'passed' || aiStatus === 'review'" class="status-message" :class="aiStatus">
             <div v-if="aiStatus === 'passed'" class="msg-content">
                <span class="icon">🎉</span>
                <div>
                  <strong>검증 통과!</strong>
                  <p>AI검증에 통과했습니다. 이제 포스팅을 제출할 수 있습니다.</p>
                </div>
             </div>
             <div v-else class="msg-content">
                <span class="icon">⚠️</span>
                <div>
                  <strong>내용 보완이 필요해요</strong>
                  <ul class="error-list">
                    <li v-for="cond in aiResult?.conditions?.filter(c => c.satisfied !== 'yes')" :key="cond.requirement">
                      {{ cond.reason }}
                    </li>
                  </ul>
                </div>
             </div>
          </div>

          <div class="footer-action">
            <button
              class="btn-action btn-save"
              :disabled="aiStatus === 'running' || !content || !imagePreviewUrl"
              @click="saveProgress"
            >
              저장하기
            </button>

            <button
              v-if="aiStatus === 'pending' || aiStatus === 'review' || aiStatus === 'passed'"
              class="btn-action btn-verify"
              :disabled="aiStatus === 'running' || !content || !imagePreviewUrl"
              @click="runAIVerification"
            >
              <span v-if="aiStatus === 'running'">분석 중...</span>
              <span v-else>AI 검증받기</span>
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, reactive } from 'vue'
import api from '@/plugins/axios'

const props = defineProps({
  item: { type: Object, required: true }
})

const emit = defineEmits(['close', 'refresh'])

// 상태: 'pending', 'running', 'passed', 'review', 'failed'
const aiStatus = ref('pending')
const aiResult = ref(null)
const aiPhase = ref(null)

const content = ref('')
const imagePreviewUrl = ref(null)
const imageFile = ref(null)
const fileInputRef = ref(null)

// 변경 사항 저장 여부 추적 (Dirty Check)
const isDirty = ref(false)

// Toast 상태 관리
const toast = reactive({
  visible: false,
  message: '',
  type: 'info' // info, success, warning
})

const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.visible = true
  setTimeout(() => {
    toast.visible = false
  }, 3000) // 3초 뒤 사라짐
}

const triggerFileInput = () => fileInputRef.value?.click()

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  imageFile.value = file
  imagePreviewUrl.value = URL.createObjectURL(file)
  
  // 변경됨 표시 및 상태 리셋
  isDirty.value = true
  if (aiStatus.value !== 'running') {
    aiStatus.value = 'pending'
  }
}

const onContentChange = () => {
  // 변경됨 표시 및 상태 리셋
  isDirty.value = true
  if (aiStatus.value !== 'running') {
    aiStatus.value = 'pending'
  }
}

watch(
  () => props.item,
  (item) => {
    if (!item) return
    content.value = item.content || ''
    imagePreviewUrl.value = item.image || null
    aiStatus.value = item.ai_validation_status === 'passed' ? 'passed' : 'pending'
    aiResult.value = item.ai_result_raw || null
    isDirty.value = false // 초기 로드시엔 변경사항 없음
  },
  { immediate: true }
)

const saveProgress = async () => {
  if (!content.value || !imagePreviewUrl.value) return;

  const formData = new FormData();
  formData.append('content', content.value);
  if (imageFile.value) formData.append('image', imageFile.value);

  try {
    const res = await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/save/`, 
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    
    // 저장 성공 처리
    isDirty.value = false; // 변경사항 저장됨
    showToast('내용이 저장되었습니다.', 'success');
    
    // 저장 후 상태가 바뀌었다면 업데이트 (필요시)
    // aiStatus.value = 'pending'; 
  } catch (error) {
    console.error('저장 실패:', error);
    showToast('저장에 실패했습니다.', 'warning');
  }
};

const runAIVerification = async () => {
  if (!content.value || !imagePreviewUrl.value) return;

  // 1. 저장되지 않은 변경사항이 있는지 확인
  if (isDirty.value) {
    showToast('내용을 먼저 저장해 주세요.', 'warning');
    return;
  }

  aiStatus.value = 'running';
  aiPhase.value = 'content';

  setTimeout(() => { if(aiStatus.value === 'running') aiPhase.value = 'image' }, 800);
  setTimeout(() => { if(aiStatus.value === 'running') aiPhase.value = 'rule' }, 1600);

  try {
    const res = await api.post(
      `/api/v1/deliverables/${props.item.deliverable_id}/verify/`,
      { content: content.value }
    );

    setTimeout(() => {
      aiPhase.value = 'done';
      aiResult.value = res.data.ai_result;
      aiStatus.value = res.data.ai_validation_status;
    }, 2500);

  } catch (error) {
    console.error(error);
    showToast('검증 중 오류가 발생했습니다.', 'warning');
    aiStatus.value = 'pending';
  }
};


const closeModal = () => {
  if (imagePreviewUrl.value && imageFile.value) URL.revokeObjectURL(imagePreviewUrl.value)
  emit('close')
}
</script>

<style scoped>
* { box-sizing: border-box; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-container {
  width: 1000px;
  height: 700px;
  background: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  padding: 40px;
  position: relative;
}

/* --- Toast Message Styles --- */
.toast-message {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(33, 33, 33, 0.9);
  color: #fff;
  padding: 12px 24px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  z-index: 2100;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  gap: 8px;
}
.toast-message.success { background: #405445; } /* 성공 시 짙은 녹색 */
.toast-message.warning { background: #E65100; } /* 경고 시 주황색 */

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translate(-50%, 20px); }

/* --- Rest of Styles --- */

.close-btn {
  position: absolute;
  top: 24px;
  right: 24px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  z-index: 100;
}

.modal-header-top {
  text-align: center;
  margin-bottom: 30px;
}

.modal-body {
  display: flex;
  flex: 1;
  gap: 40px;
  min-height: 0;
}

/* --- 왼쪽: 이미지 업로드 --- */
.left-section {
  width: 45%;
  display: flex;
  flex-direction: column;
}

.dashed-box {
  width: 100%;
  height: 100%;
  border: 2px dashed #BDBDBD;
  border-radius: 12px;
  background: #FAFAFA;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s;
}

.dashed-box:hover {
  border-color: #405445;
  background: #F0F4F1;
}

.dashed-box.has-image {
  border: none;
  background: transparent;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.plus-sign {
  font-size: 48px;
  font-weight: 300;
  color: #8D6E63;
  margin-bottom: 12px;
  line-height: 1;
}

.upload-label {
  font-size: 16px;
  font-weight: 700;
  color: #5D4037;
}

.image-wrapper { width: 100%; height: 100%; position: relative; }
.preview-img { width: 100%; height: 100%; object-fit: cover; border-radius: 10px; }
.hover-overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,0.3);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.2s;
}
.dashed-box:hover .hover-overlay { opacity: 1; }
.hover-overlay span { color: #FFF; font-weight: 600; border: 1px solid #FFF; padding: 6px 12px; border-radius: 20px; }
.hidden-input { display: none; }

/* --- 오른쪽: 콘텐츠 --- */
.right-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.product-info { margin-bottom: 15px; }
.product-info .label { color: #888; font-weight: 600; margin-right: 6px; }
.product-info .product-name { color: #333; font-weight: 700; font-size: 15px; }

.input-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  min-height: 0;
}
.section-label { font-size: 16px; font-weight: 700; color: #333; margin-bottom: 10px; display: block; }
.modern-textarea {
  width: 100%; flex: 1; padding: 16px; font-size: 15px;
  border: 1px solid #E0E0E0; border-radius: 8px; resize: none; outline: none;
}
.modern-textarea:focus { border-color: #405445; background: #FFF; }

.process-visualizer {
  background: #F5F5F5;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
}
.process-text { margin: 0 0 15px 0; color: #666; font-size: 14px; }
.steps-container { display: flex; justify-content: center; align-items: center; gap: 10px; }
.step { opacity: 0.3; transition: all 0.3s; transform: scale(0.9); display: flex; flex-direction: column; align-items: center;}
.step.active { opacity: 1; transform: scale(1.1); font-weight: bold; color: #2E7D32; }
.step .icon { font-size: 24px; margin-bottom: 4px; }
.step span { font-size: 12px; }
.line { width: 30px; height: 2px; background: #DDD; }

.status-message {
  padding: 15px; border-radius: 8px; margin-bottom: 20px; animation: slideUp 0.3s;
}
@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.status-message.passed { background: #E8F5E9; border: 1px solid #C8E6C9; color: #1B5E20; }
.status-message.review { background: #FFF3E0; border: 1px solid #FFE0B2; color: #E65100; }
.msg-content { display: flex; gap: 12px; align-items: flex-start; }
.msg-content .icon { font-size: 24px; }
.msg-content p, .msg-content li { margin: 0; font-size: 13px; }
.error-list { padding-left: 20px; margin-top: 4px; }

/* 버튼 영역 Flex 배치 */
.footer-action {
  margin-top: auto;
  display: flex; /* 가로 배치 */
  gap: 12px;     /* 버튼 사이 간격 */
}

.btn-action {
  flex: 1;       /* 공간 균등 분할 */
  height: 54px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  color: #FFF;
  /* 공통 색상 적용 */
  background: #405445; 
}

.btn-action:hover:not(:disabled) {
  background: #2F3E33;
  transform: translateY(-2px);
}

.btn-action:disabled {
  background: #CCC;
  cursor: not-allowed;
  transform: none;
}
</style>