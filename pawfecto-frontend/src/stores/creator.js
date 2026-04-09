import { defineStore } from "pinia"
import api from "@/plugins/axios"
import { useWarningStore } from "./warning"

export const useCreatorStore = defineStore("creator", {
  state: () => ({
    creator: null,
    creators: [],
    recommendedCreators: [],
    isLoaded: false,
    loading: false,
  }),

  actions: {
    async loadCreator() {
      if (this.isLoaded && this.creator) return

      const res = await api.get("/accounts/me/")
      this.creator = res.data
      this.isLoaded = true
    },

    async fetchCreator(creatorId) {
      const res = await api.get(`/accounts/creator/${creatorId}/`)
      this.creator = res.data
      this.isLoaded = true
    },

    async recommendCreators(campaignId, brandId) {
      const warningStore = useWarningStore()

      try {
        this.loading = true

        const response = await api.post(
          `/api/v1/brand/${brandId}/campaign/${campaignId}/auto-match/`
        )

        this.recommendedCreators = response.data.map((creator) => ({
          id: creator.campaign_acceptance_id,
          name: creator.creator.name,
          handle: creator.creator.sns_handle || creator.creator.username,
          profileImg: creator.creator.profile_image_url,
          petType: creator.creator.pet_type,
          followers: creator.creator.follower_count ?? 0,
          styleTags: creator.creator.style_tags || [],
          brandStatus: creator.brand_decision_status,
          creatorStatus: creator.acceptance_status,
        }))

        warningStore.open("크리에이터 추천이 완료되었습니다.")
      } catch (error) {
        console.error(error)
        warningStore.open("추천 작업 중 오류가 발생했습니다.")
      } finally {
        this.loading = false
      }
    },

    addRecommendedCreators(newCreators) {
      this.recommendedCreators = [...this.recommendedCreators, ...newCreators]
    },
  },
})
