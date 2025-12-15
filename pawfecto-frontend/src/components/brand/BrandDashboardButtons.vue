<template>
  <div class="btn-wrap">

    <!-- My Campaigns -->
    <router-link
      :to="{
        name: 'brand-campaign-list',
        params: { brand_id }
      }"
      class="toggle-btn"
      :class="{ active: isMyCampaignsActive }"
    >
      My Campaigns
    </router-link>

    <!-- Settings -->
    <router-link
      :to="{
        name: 'brand-settings',
        params: { brand_id }
      }"
      class="toggle-btn"
      :class="{ active: isSettingsActive }"
    >
      Settings
    </router-link>

  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

// 라우트 파라미터에서 brand_id 추출
const brand_id = computed(() => route.params.brand_id)

// My Campaigns 활성 여부 (campaign-list + create-campaign + campaign-detail 포함)
const isMyCampaignsActive = computed(() => {
  return route.name?.includes("campaign")
})

// Settings 활성 여부
const isSettingsActive = computed(() => {
  return route.name === "brand-settings"
})
</script>

<style scoped>
.btn-wrap {
  margin: 90px 0px;
  display: flex;
  justify-content: center;
  gap: 50px;
}

.toggle-btn {
  padding: 12px 36px;
  font-size: 16px;
  border-radius: 999px;
  cursor: pointer;
  background-color: #fff;
  border: 1px solid #d3d3d3;
  color: #444;
  transition: all 0.15s ease;
  width: 250px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}

/* 선택된 버튼 스타일 */
.toggle-btn.active {
  background-color: #f1f1f1;
  border-color: #f1f1f1;
  color: #000;
}
</style>
