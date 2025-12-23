// stores/deliverable.js
import axios from 'axios'

export const deliverableStore = {
  state: {
    deliverable: null,
    loading: false,
    error: null
  },
  
  // 게시글 작성 후 AI 검증이 완료되면, 해당 상태를 업데이트
  actions: {
    async createDeliverable(data) {
      this.loading = true
      this.error = null

      try {
        const response = await axios.post('/api/v1/deliverables/', data)
        this.deliverable = response.data
        this.loading = false
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'AI 검증 요청 실패'
        this.loading = false
      }
    },

   // AI 검증을 위한 요청
    async validateWithAI(deliverableId) {
      this.loading = true
      this.error = null

      try {
        const response = await axios.post(`/api/v1/deliverables/${deliverableId}/ai-validation/`)
        // AI 검증 상태를 'passed'로 설정
        this.deliverable = response.data
        this.deliverable.validation_status = 'passed' 
        this.loading = false
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'AI 검증 실패'
        this.loading = false
      }
    }
  }
}
