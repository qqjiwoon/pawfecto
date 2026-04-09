<template>
  <div class="creator-layout" v-if="creator">

    <!-- 프로필 헤더 -->
    <CreatorProfileHeader :creator="creator" />

    <!-- 상단 버튼 -->
    <CreatorDashboardButtons />

    <!-- My Campaigns에서만 보이는 탭 -->
    <CreatorDashboardTabs v-if="showSubTabs" />

    <!-- 하위 라우트 출력 (정상) -->
    <router-view />

  </div>

  <!-- 크리에이터 정보가 없는 경우 -->
  <div v-else class="not-found">
    <p>크리에이터 정보를 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import CreatorProfileHeader from '@/components/creator/CreatorProfileHeader.vue'
import CreatorDashboardButtons from '@/components/creator/CreatorDashboardButtons.vue'
import CreatorDashboardTabs from '@/components/creator/CreatorDashboardTabs.vue'

import { useCreatorStore } from '@/stores/creator'

const route = useRoute()
const creatorStore = useCreatorStore()

// URL 파라미터
const creatorId = computed(() => Number(route.params.creator_id))
// creator 정보
const creator = computed(() => creatorStore.creator)

// 최초 로드
onMounted(async () => {
  await creatorStore.loadCreator()
})

// creator_id 변경 시 대응
watch(creatorId, async (newId) => {
  await creatorStore.fetchCreator(newId)
})

// 탭 노출 여부
const showSubTabs = computed(() =>
  route.path.includes('/campaign-offers') ||
  route.path.includes('/campaign-progress')
)
</script>

<style scoped>
.creator-layout {
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
