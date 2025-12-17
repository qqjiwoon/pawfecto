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
    // 브랜드 캠페인 목록
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

    // 캠페인 생성 (추가)
    async createCampaign(brandId, payload) {
      this.loading = true
      this.error = null

      try {
        const res = await api.post(
          `/api/v1/brand/${brandId}/campaign/create/`,
          payload
        )

        // 생성 후 목록에 즉시 반영하고 싶다면
        this.campaigns.push(res.data)

        return res.data
      } catch (err) {
        console.error(err.response || err)
        this.error = "캠페인 생성에 실패했습니다."
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})