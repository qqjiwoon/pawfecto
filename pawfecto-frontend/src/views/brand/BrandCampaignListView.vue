<template>
  <BrandCampaignList
    v-if="isCampaignLoaded"
    :campaigns="paginatedCampaigns"
    :brandId="brandId"
    :currentPage="currentPage"
    :totalPages="totalPages"
    @change-page="changePage"
  />
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BrandCampaignList from '@/components/brand/BrandCampaignList.vue'
import { campaigns, loadBrandCampaigns, isCampaignLoaded } from '@/stores/campaign'


const route = useRoute()
const brandId = Number(route.params.brand_id)

// 페이지네이션
const currentPage = ref(1)
const itemsPerPage = 6

onMounted(() => {
  loadBrandCampaigns(brandId)
})

// 전체 페이지 수
const totalPages = computed(() =>
  Math.ceil(campaigns.value.length / itemsPerPage)
)

// 현재 페이지 캠페인
const paginatedCampaigns = computed(() => {
  if (!Array.isArray(campaigns.value)) return []

  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return campaigns.value.slice(start, end)
})

// 페이지 변경
function changePage(page) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
