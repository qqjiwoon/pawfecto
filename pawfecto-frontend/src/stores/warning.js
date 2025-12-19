import { defineStore } from 'pinia'

export const useWarningStore = defineStore('warning', {
  state: () => ({
    isOpen: false,
    message: '',
    isConfirm: false, // true면 확인/취소 두 버튼 노출
    resolvePromise: null, // Promise 해결을 위한 함수 저장
  }),
  actions: {
    // 단순 알림용
    open(msg) {
      this.message = msg
      this.isConfirm = false
      this.isOpen = true
    },
    // 예/아니오 선택용 (Promise 반환)
    confirm(msg) {
      this.message = msg
      this.isConfirm = true
      this.isOpen = true
      return new Promise((resolve) => {
        this.resolvePromise = resolve
      })
    },
    // 모달 닫기 (결과 전달)
    close(result = false) {
      this.isOpen = false
      if (this.resolvePromise) {
        this.resolvePromise(result)
        this.resolvePromise = null
      }
    }
  }
})
