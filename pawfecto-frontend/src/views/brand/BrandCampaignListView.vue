<template>
  <BrandCampaignList
    :campaigns="paginatedCampaigns"
    :brandId="brandId"
    :currentPage="currentPage"
    :totalPages="totalPages"
    @change-page="changePage"
  />
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { campaigns } from '@/stores/campaign'
import BrandCampaignList from '@/components/brand/BrandCampaignList.vue'

const route = useRoute()
const brandId = Number(route.params.brand_id)

// 페이지네이션 설정
const currentPage = ref(1)
const itemsPerPage = 6  // 페이지당 표시할 캠페인 수

// 브랜드별 캠페인 필터링
const brandCampaigns = computed(() =>
  campaigns.value.filter(c => c.brand_id === brandId)
)

// 전체 페이지 수 계산
const totalPages = computed(() =>
  Math.ceil(brandCampaigns.value.length / itemsPerPage)
)

// 현재 페이지에 표시할 캠페인
const paginatedCampaigns = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return brandCampaigns.value.slice(start, end)
})

// 페이지 변경 핸들러
function changePage(page) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>