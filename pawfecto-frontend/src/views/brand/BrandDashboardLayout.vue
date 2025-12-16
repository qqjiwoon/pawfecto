<template>
  <div class="brand-layout" v-if="brandStore">

    <!-- 프로필 헤더 -->
    <BrandProfileHeader :brand="brandStore" />

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
// ===============================
// Brand Dashboard Layout (최소 수정)
// ===============================

import { onMounted, watch } from "vue"
import { useRoute } from "vue-router"

import BrandProfileHeader from "@/components/brand/BrandProfileHeader.vue"
import BrandDashboardButtons from "@/components/brand/BrandDashboardButtons.vue"

// stores/brand.js
import { brand as brandStore, loadBrand } from "@/stores/brand"

const route = useRoute()

// 최초 진입 시 brand 로드
onMounted(() => {
  loadBrand(route.params.brandId)
})

// brandId 변경 시 brand 재로드 (핵심)
watch(
  () => route.params.brandId,
  (newBrandId) => {
    if (newBrandId) {
      loadBrand(newBrandId)
    }
  }
)
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
