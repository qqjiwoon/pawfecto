<template>
  <Transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="cancel">
      <div class="modal-box">
        <div class="icon-wrap">
          <span class="warning-icon">!</span>
        </div>
        
        <h3 class="modal-title">알림</h3>
        <p class="message">{{ message }}</p>
        
        <div class="button-group">
          <button v-if="isConfirm" class="cancel-btn" @click="cancel">취소</button>
          <button class="confirm-btn" :class="{ 'full': !isConfirm }" @click="confirm">확인</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useWarningStore } from '@/stores/warning'

const warningStore = useWarningStore()

const isOpen = computed(() => warningStore.isOpen)
const message = computed(() => warningStore.message)
const isConfirm = computed(() => warningStore.isConfirm)

const confirm = () => warningStore.close(true)
const cancel = () => warningStore.close(false)
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 10000;
}

.modal-box {
  background: #ffffff; padding: 40px 32px 30px;
  border-radius: 24px; width: 90%; max-width: 340px;
  text-align: center; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.icon-wrap {
  width: 50px; height: 50px; background-color: #fdf2f2;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}

.warning-icon { color: #8B3A3A; font-size: 24px; font-weight: 800; }
.modal-title { font-size: 18px; font-weight: 700; color: #333; margin-bottom: 12px; }
.message { font-size: 15px; color: #666; line-height: 1.6; margin-bottom: 30px; word-break: keep-all; }

/* 버튼 레이아웃: 이전의 2.5:1 비율 감성을 적용 */
.button-group { display: flex; gap: 10px; }

.confirm-btn, .cancel-btn {
  padding: 14px; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s;
}

.confirm-btn { background-color: #65481F; color: white; flex: 2; }
.confirm-btn.full { flex: 1; } /* 알림 모드일 땐 꽉 차게 */
.confirm-btn:hover { background-color: #523a1a; }

.cancel-btn { background-color: #f5f1ec; color: #7e6b5a; flex: 1; border: 1px solid #e0d6cc; }
.cancel-btn:hover { background-color: #ede6de; }

/* 애니메이션 */
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.9) translateY(20px); }
</style>
