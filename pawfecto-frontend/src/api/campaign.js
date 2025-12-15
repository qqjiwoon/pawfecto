// src/api/campaign.js
import api from "@/plugins/axios"


// 브랜드 대시보드 (메인)
export function fetchBrandCampaigns(brandId) {
  return api.get(`/api/v1/brand/${brandId}/campaign/`)
}


// 캠페인 상세 조회
export function fetchCampaignDetail(brandId, campaignId) {
  return api.get(`/api/v1/brand/${brandId}/campaign/${campaignId}/`)
}


// 캠페인 수정
export function updateCampaign(brandId, campaignId, payload) {
  return axios.put(
    `/api/v1/brand/${brandId}/campaign/${campaignId}/update/`,
    payload
  )
}