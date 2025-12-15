<template>
  <div class="brand-layout" v-if="brand">

    <!-- 프로필 헤더 -->
    <BrandProfileHeader :brand="brand" />

    <!-- 상단 버튼 -->
    <BrandDashboardButtons />

    <!-- My Campaigns에서만 보이는 탭 -->
    <!-- <BrandDashboardTabs v-if="showSubTabs" /> -->

    <!-- 하위 라우트 출력 -->
    <router-view />

  </div>

  <!-- 브랜드 정보가 없는 경우 -->
  <div v-else class="not-found">
    <p>브랜드 정보를 찾을 수 없습니다.</p>
  </div>
</template>


<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

import BrandProfileHeader from "@/components/brand/BrandProfileHeader.vue"
import BrandDashboardButtons from "@/components/brand/BrandDashboardButtons.vue"
// import BrandDashboardTabs from "@/components/brand/BrandDashboardTabs.vue"

// stores/brand.js에서 brands 배열 불러오기
import { brands } from "@/stores/brand"

// 현재 라우트 정보
const route = useRoute()

// URL의 :brand_id → 숫자로 변환
const brandId = computed(() => Number(route.params.brand_id))

// brands 배열에서 해당 id를 가진 brand 찾기
const brand = computed(() =>
  brands.value.find(b => b.id === brandId.value)
)

// // 특정 페이지에서만 탭 노출
// const showSubTabs = computed(() =>
//   route.path.includes('/campaign-offers') ||
//   route.path.includes('/campaign-progress')
// )
</script>


<style scoped>
.brand-layout {
  width: 100%;
  margin: 0 auto;
  padding-bottom: 80px;
}

.not-found {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
