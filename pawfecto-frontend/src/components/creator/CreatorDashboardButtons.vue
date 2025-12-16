<template>
  <div class="btn-wrap">

    <!-- My Campaigns -->
    <router-link
      :to="{
        name: 'creator-campaign-offers',
        params: { creator_id: creatorId }
      }"
      class="toggle-btn"
      :class="{ active: isMyCampaignsActive }"
    >
      My Campaigns
    </router-link>

    <!-- Settings -->
    <router-link
      :to="{
        name: 'creator-settings',
        params: { creator_id: creatorId }
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

const creatorId = computed(() => Number(route.params.creator_id))

// My Campaigns 활성 여부 (offers + progress 포함)
const isMyCampaignsActive = computed(() =>
  route.name === "creator-campaign-offers" ||
  route.name === "creator-campaign-progress"
)

// Settings 활성 여부
const isSettingsActive = computed(() =>
  route.name === "creator-settings" ||
  route.name === "creator-settings-update"
)
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
