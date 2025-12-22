// stores/warning.js
import { defineStore } from 'pinia'

export const useWarningStore = defineStore('warning', {
  state: () => ({
    isOpen: false,
    message: '',
    icon: '!', // 기본값
    isConfirm: false,
    resolvePromise: null,
  }),
  actions: {
    // [수정] open도 Promise를 반환하여 await 가능하게 만듭니다.
    open(msg, isSuccess = false) {
      this.message = msg
      this.icon = isSuccess ? '✔' : '!' 
      this.isConfirm = false
      this.isOpen = true
      
      return new Promise((resolve) => {
        this.resolvePromise = resolve
      })
    },
    
    confirm(msg) {
      this.message = msg
      this.icon = '!'  
      this.isConfirm = true
      this.isOpen = true
      return new Promise((resolve) => {
        this.resolvePromise = resolve
      })
    },

    close(result = false) {
      this.isOpen = false
      if (this.resolvePromise) {
        this.resolvePromise(result)
        this.resolvePromise = null
      }
    }
  }
})
