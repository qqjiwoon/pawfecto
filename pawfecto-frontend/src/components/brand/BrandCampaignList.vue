<template>
  <div class="campaign-wrapper">

    <!-- 캠페인 없음 (최상단) -->
    <p
      v-if="campaigns.length === 0"
      class="empty-message"
    >
      등록된 캠페인이 없습니다.
    </p>

    <!-- 캠페인 생성 버튼 (항상 노출) -->
    <div class="create-button-wrap">
      <router-link
        :to="{
          name: 'brand-create-campaign',
          params: { brand_id: brandId }
        }"
        class="create-button"
      >
        캠페인 등록 →
      </router-link>
    </div>

    <!-- 캠페인 목록 -->
    <div
      v-if="campaigns.length > 0"
      class="campaign-list"
    >
      <BrandCampaignCard
        v-for="campaign in campaigns"
        :key="campaign.campaign_id || campaign.id"
        :campaign="campaign"
        :brandId="brandId"
      />
    </div>

    <!-- 페이지네이션 -->
    <div
      v-if="campaigns.length > 0"
      class="pagination-wrap"
    >
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        @change-page="$emit('change-page', $event)"
      />
    </div>

  </div>
</template>


<script setup>
import BrandCampaignCard from './BrandCampaignCard.vue'
import Pagination from './Pagination.vue'

// Props 정의
defineProps({
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
</script>

<style scoped>
/* 안내 문구 스타일 */
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
  grid-template-columns: repeat(auto-fit, 250px);
  justify-content: center;
  gap: 30px;
  margin-bottom: 5%;
}

.pagination-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
}

.create-button-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.create-button {
  color: #65481F;
  font-weight: 600;
  text-decoration: none;
}

.empty-message {
  text-align: center;
  color: #7E6B5A;
  font-size: 15px;
  margin: 80px 0;
}

</style>
