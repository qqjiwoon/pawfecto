<template>
  <div>
    <BrandCampaignDetail />   <!-- 상세 정보 -->
    <BrandDashboardTabs />    <!-- status / recommendations 전환 탭 -->
    <router-view />           <!-- status / recommendations 렌더링 -->
  </div>
</template>

<script setup>
import BrandCampaignDetail from '@/components/brand/BrandCampaignDetail.vue'
import BrandDashboardTabs from '@/components/brand/BrandDashboardTabs.vue'
</script>
