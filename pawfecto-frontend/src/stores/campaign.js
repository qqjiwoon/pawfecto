// src/stores/campaign.js
import { defineStore } from "pinia"
import api from "@/plugins/axios"

export const useCampaignStore = defineStore("campaign", {
  state: () => ({
    campaigns: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchBrandCampaigns(brandId) {
      this.loading = true
      this.error = null

      try {
        const res = await api.get(
          `/api/v1/brand/${brandId}/campaign/`
        )
        this.campaigns = res.data
      } catch (err) {
        console.error(err)
        this.error = "캠페인 목록을 불러오지 못했습니다."
        this.campaigns = []
      } finally {
        this.loading = false
      }
    },
  },
})
