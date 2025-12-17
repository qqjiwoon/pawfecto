<template>
  <div class="brand-layout" v-if="brand">

    <!-- 프로필 헤더 -->
    <BrandProfileHeader :brand="brand" />

    <!-- 상단 버튼 -->
    <BrandDashboardButtons />

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
// Brand Dashboard Layout
// ===============================
import { computed, onMounted } from "vue"

import BrandProfileHeader from "@/components/brand/BrandProfileHeader.vue"
import BrandDashboardButtons from "@/components/brand/BrandDashboardButtons.vue"

import { useBrandStore } from "@/stores/brand"

// store
const brandStore = useBrandStore()

// brand 정보 (creator와 동일한 패턴)
const brand = computed(() => brandStore.brand)

// 최초 로드
onMounted(async () => {
  await brandStore.loadBrand()
})
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
