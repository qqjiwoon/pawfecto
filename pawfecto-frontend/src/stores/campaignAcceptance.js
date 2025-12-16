// src/stores/campaignAcceptance.js
import { defineStore } from "pinia"
import api from "@/plugins/axios"

export const useCampaignAcceptanceStore = defineStore("campaignAcceptance", {
  state: () => ({
    acceptances: [],
    loading: false,
    error: null,
  }),

  actions: {
    // 1️⃣ 크리에이터 캠페인 오퍼 목록 조회
    async fetchCreatorAcceptances(creatorId) {
      this.loading = true
      this.error = null

      try {
        const res = await api.get(
          `/api/v1/creator/${creatorId}/campaign-acceptances/`
        )
        this.acceptances = res.data
      } catch (e) {
        console.error(e)
        this.error = "캠페인 오퍼 목록을 불러오지 못했습니다."
        this.acceptances = []
      } finally {
        this.loading = false
      }
    },

    // 2️⃣ 캠페인 수락
    async acceptCampaign(campaignId) {
      try {
        await api.post(`/api/v1/campaigns/${campaignId}/accept/`)
        // 수락 후 목록 갱신
        this.acceptances = this.acceptances.map(acc =>
          acc.campaign_id === campaignId
            ? { ...acc, acceptance_status: "accepted" }
            : acc
        )
      } catch (e) {
        console.error(e)
        throw new Error("캠페인 수락 실패")
      }
    },

    // 3️⃣ 캠페인 거절
    async rejectCampaign(campaignId) {
      try {
        await api.post(`/api/v1/campaigns/${campaignId}/reject/`)
        this.acceptances = this.acceptances.map(acc =>
          acc.campaign_id === campaignId
            ? { ...acc, acceptance_status: "rejected" }
            : acc
        )
      } catch (e) {
        console.error(e)
        throw new Error("캠페인 거절 실패")
      }
    },
  },
})
