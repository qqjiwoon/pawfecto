<template>
  <div class="campaign-wrapper">
    <div class="campaign-list">
      <BrandCampaignCard
        v-for="campaign in campaigns"
        :key="campaign.campaign_id || campaign.id"
        :campaign="campaign"
        :brandId="brandId"
      />
    </div>

    <div class="pagination-wrap">
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
</style>
