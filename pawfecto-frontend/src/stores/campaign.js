// stores/campaign.js
import { ref } from "vue"
import { fetchBrandCampaigns } from "@/api/campaign"

export const campaigns = ref([])
export const isCampaignLoaded = ref(false)

export const loadBrandCampaigns = async (brandId) => {
  try {
    const res = await fetchBrandCampaigns(brandId)
    campaigns.value = res.data || []
  } catch (err) {
    console.error("캠페인 목록 조회 실패:", err)
    campaigns.value = []
  } finally {
    isCampaignLoaded.value = true
  }
}
