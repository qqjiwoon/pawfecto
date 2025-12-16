import { defineStore } from "pinia"
import axios from "axios"

export const useCreatorStore = defineStore("creator", {
  state: () => ({
    creator: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCreator(creatorId) {
      this.loading = true
      this.error = null

      const token = localStorage.getItem("access")

      if (!token) {
        this.error = "로그인이 필요합니다."
        this.loading = false
        return
      }

      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/accounts/creator/${creatorId}/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        this.creator = res.data
      } catch (err) {
        console.error(err)
        this.error = "크리에이터 정보를 불러오지 못했습니다."
        this.creator = null
      } finally {
        this.loading = false
      }
    },
  },
})