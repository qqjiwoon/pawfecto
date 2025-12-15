<template>
  <div class="tabs">
    
    <!-- Campaign Offers -->
    <router-link
      :to="{ 
        name: 'creator-campaign-offers', 
        params: { creator_id: route.params.creator_id } 
      }"
      class="tab-item"
      :class="{ active: route.name === 'creator-campaign-offers' }"
    >
      Campaign Offers
    </router-link>

    <!-- Campaign Progress -->
    <router-link
      :to="{ 
        name: 'creator-campaign-progress', 
        params: { creator_id: route.params.creator_id } 
      }"
      class="tab-item"
      :class="{ active: route.name === 'creator-campaign-progress' }"
    >
      Campaign Progress
    </router-link>

  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

// 현재 경로가 탭의 경로와 일치하면 active 처리
const isActive = (path) => {
  return route.path.startsWith(path)
}
</script>

<style scoped>
.tabs {
  display: flex;
  justify-content: center;
  gap: 180px;
  margin-top: 100px;
  border-bottom: 1px solid #e5e5e5;
  padding-bottom: 4px;
}

.tab-item {
  position: relative;
  font-size: 18px;
  padding-bottom: 3px;
  color: #8a8a8a; 
  cursor: pointer;
  text-decoration: none;       /* router-link 기본 밑줄 제거 */
  transition: all 0.2s ease;
}

/* 기본 밑줄 */
.tab-item::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 250px;
  height: 2px;
  background-color: #dcdcdc;
  transition: all 0.2s ease;
}

/* 활성 탭 글씨 */
.tab-item.active {
  color: #333;
  font-weight: 600;
}

/* 활성 탭 밑줄 */
.tab-item.active::after {
  background-color: #333;
  width: 250px;
}
</style>
