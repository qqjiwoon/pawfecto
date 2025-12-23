<template>
  <div class="campaign-wrapper">
    <h1 class="title">My Campaigns</h1>

    <div class="campaign-list">

      <router-link
        :to="{
          name: 'brand-create-campaign',
          params: { brand_id: brandId }
        }"
        class="add-card"
      >
        <div class="add-content">
          <span class="plus-icon">+</span>
          <span class="add-text">새 캠페인 등록</span>
        </div>
      </router-link>

      <BrandCampaignCard
        v-for="campaign in sortedCampaigns"
        :key="campaign.campaign_id || campaign.id"
        :campaign="campaign"
        :brandId="brandId"
      />
    </div>

    <p v-if="campaigns.length === 0" class="empty-message">
      현재 진행 중인 캠페인이 없습니다. 첫 캠페인을 등록해보세요!
    </p>

    <div v-if="campaigns.length > 0" class="pagination-wrap">
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        @change-page="$emit('change-page', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BrandCampaignCard from './BrandCampaignCard.vue'
import Pagination from '@/components/Pagination.vue'

// Props 정의
const props = defineProps({
  campaigns: {
    type: Array,
    required: true,
    default: () => []
  },
  brandId: {
    type: Number,
    required: true
  },
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

// Emits 정의
defineEmits(['change-page'])

// [수정됨] requested_at 기준 최신순 정렬
const sortedCampaigns = computed(() => {
  if (!props.campaigns) return []

  // 원본 배열 복사 후 정렬
  return [...props.campaigns].sort((a, b) => {
    // 날짜 문자열을 Date 객체로 변환하여 밀리초 단위로 비교
    // 값이 없으면 0으로 처리하여 맨 뒤로 보냄
    const dateA = a.requested_at ? new Date(a.requested_at).getTime() : 0;
    const dateB = b.requested_at ? new Date(b.requested_at).getTime() : 0;
    
    // 내림차순 (최신 날짜가 더 큰 숫자이므로 B - A)
    return dateB - dateA;
  })
})
</script>

<style scoped>
.title {
  font-size: 32px;
  font-weight: bold;
  margin: 90px 0;
  text-align: center;
}

.empty-message {
  text-align: center;
  color: #7E6B5A;
  font-size: 15px;
  margin: 80px 0;
}

.campaign-wrapper {
  margin-bottom: 10%;
}

.campaign-list {
  display: grid;
  /* 반응형 그리드: 최소 250px 너비 유지, 자동 줄바꿈 */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  justify-content: center;
  gap: 30px;
  margin-bottom: 5%;
  margin-left: 10%;
  margin-right: 10%;
}

/* 등록 카드 스타일 */
.add-card {
  width: 100%;
  aspect-ratio: 5 / 7; /* BrandCampaignCard와 동일한 비율로 맞추기 */

  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px dashed #e0d6cc;
  border-radius: 16px;
  background-color: #fdfaf8;
  text-decoration: none;
  transition: all 0.3s ease;
}

.add-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.plus-icon {
  font-size: 48px;
  font-weight: 300;
  color: #C4B199;
  line-height: 1;
}

.add-text {
  font-size: 16px;
  font-weight: 600;
  color: #7E6B5A;
}

.add-card:hover {
  background-color: #f5f1ec;
  border-color: #C4B199;
  transform: translateY(-5px);
}

.add-card:hover .plus-icon,
.add-card:hover .add-text {
  color: #65481F;
}

.pagination-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
