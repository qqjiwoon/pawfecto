<template>
  <nav class="campaign-tabs">
    <RouterLink
      :to="{
        name: 'campaign-recommendations',
        params: {
          brand_id: brandId,
          campaign_id: campaignId
        }
      }"
      class="tab"
      :class="{ active: currentRoute === 'campaign-recommendations' || currentRoute === 'brand-campaign-detail' }"
    >
      Creator Recommendations
    </RouterLink>

    <RouterLink
      :to="{
        name: 'campaign-status',
        params: {
          brand_id: brandId,
          campaign_id: campaignId
        }
      }"
      class="tab"
      :class="{ active: currentRoute === 'campaign-status' }"
    >
      Campaign Status
    </RouterLink>
  </nav>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

defineProps({
  brandId: Number,
  campaignId: Number,
})

const route = useRoute()
const currentRoute = computed(() => route.name)
</script>

<style scoped>
/* 크리에이터의 .tabs 스타일 적용 */
.campaign-tabs {
  display: flex;
  justify-content: center;
  gap: 180px;            /* 48px -> 180px 변경 */
  margin-top: 100px;     /* margin: 150px 0 -> margin-top: 100px 변경 */
  border-bottom: 1px solid #e5e5e5;
  padding-bottom: 4px;
}

/* 크리에이터의 .tab-item 스타일 적용 */
.tab {
  position: relative;
  font-size: 18px;       /* 15px -> 18px 변경 */
  padding-bottom: 3px;
  color: #8a8a8a;        /* #555 -> #8a8a8a 변경 */
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
}

/* 크리에이터의 기본 밑줄 (.tab-item::after) 스타일 적용 */
.tab::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 250px;          /* width: 100% -> 250px 고정으로 변경 */
  height: 2px;
  background-color: #dcdcdc; /* 회색 밑줄 기본 표시 */
  transition: all 0.2s ease;
}

/* 활성 탭 글씨 (.tab-item.active) */
.tab.active {
  color: #333;
  font-weight: 600;
}

/* 활성 탭 밑줄 (.tab-item.active::after) */
.tab.active::after {
  background-color: #333;
  width: 250px;
}
</style>
