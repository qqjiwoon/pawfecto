<template>
  <div class="campaign-wrapper">
    <h1 class="title">My Campaigns</h1>

    <div class="campaign-list">

      <!-- 캠페인 생성 버튼 (항상 노출) -->
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
        v-for="campaign in campaigns"
        :key="campaign.campaign_id || campaign.id"
        :campaign="campaign"
        :brandId="brandId"
      />
    </div>

    <!-- 캠페인 없음 (최상단) -->
    <p v-if="campaigns.length === 0" class="empty-message">
      현재 진행 중인 캠페인이 없습니다. 첫 캠페인을 등록해보세요!
    </p>

    <!-- 캠페인 목록 -->
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
.title {
  font-size: 32px;
  font-weight: Bold;
  margin: 90px 0;
  text-align: center;
}

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
  margin-left: 10%;
  margin-right: 10%;
}

/* 등록 카드 스타일 */
.add-card {
  width: 250px;
  height: 380px; /* BrandCampaignCard의 실제 높이에 맞춰 조절하세요 */
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px dashed #e0d6cc; /* 연한 브라운 점선 테두리 */
  border-radius: 16px;
  background-color: #fdfaf8; /* 아주 연한 베이지 배경 */
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

/* 마우스 올렸을 때 효과 */
.add-card:hover {
  background-color: #f5f1ec;
  border-color: #C4B199;
  transform: translateY(-5px); /* 살짝 위로 이동 */
}

.add-card:hover .plus-icon,
.add-card:hover .add-text {
  color: #65481F; /* 마우스 올리면 글자색 진하게 */
}

.pagination-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* 버튼을 감싸는 영역 - 중앙 정렬 유지 */
.create-button-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

/* Option A: Solid 스타일 버튼 */
.create-button {
  display: inline-block; /* a 태그를 버튼 모양으로 만들기 위해 */
  background-color: #65481F; /* 브랜드 메인 브라운 컬러 */
  color: white; /* 글자색은 흰색으로 */
  padding: 12px 32px; /* 내부 여백을 주어 버튼 형태 만들기 */
  border-radius: 50px; /* 둥근 알약 모양 */
  text-decoration: none; /* 밑줄 제거 */
  font-weight: 700; /* 글자를 조금 더 두껍게 */
  font-size: 16px;
  transition: all 0.3s ease; /* 부드러운 호버 효과 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 살짝 그림자 주어 입체감 더하기 */
}

/* 마우스 올렸을 때 효과 */
.create-button:hover {
  background-color: #4e3817; /* 조금 더 진한 색으로 변경 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* 그림자 더 깊게 */
  transform: translateY(-2px); /* 살짝 위로 떠오르는 느낌 */
}

.empty-message {
  text-align: center;
  color: #7E6B5A;
  font-size: 15px;
  margin: 80px 0;
}

</style>
