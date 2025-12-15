<template>
  <div class="offers-table">

    <!-- 페이지 제목 -->
    <h2 class="offers-title">Campaign Offers</h2>

    <!-- 검색 영역 -->
    <div class="search-box">
      <input type="text" placeholder="Search Product..." v-model="searchQuery" />
      <span class="search-icon">🔍</span>
    </div>

    <!-- 캠페인 오퍼 테이블 -->
    <table>
      <thead>
        <tr>
          <th>브랜드</th>
          <th>상품</th>
          <th>최소 팔로워 수</th>
          <th>스타일</th>
          <th>시작일</th>
          <th>마감일</th>
          <th>상태</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="offer in paginatedOffers" :key="offer.id">

          <!-- 브랜드 정보 -->
          <td>
            <div class="brand-col">
              <img :src="offer.brand_image" class="brand-img" />
              <span>{{ offer.brand_name }}</span>
            </div>
          </td>

          <!-- 상품명 (상세 모달 오픈) -->
          <td class="product-name" @click="openDetail(offer.campaign)">
            {{ offer.product_name }}
          </td>

          <!-- 최소 팔로워 수 -->
          <td>{{ offer.min_follower_count }}</td>

          <!-- 스타일 태그 -->
          <td>
            <div class="style-col">
              <span
                v-for="style in offer.styles"
                :key="style"
                class="style-tag"
              >
                #{{ style }}
              </span>
            </div>
          </td>

          <!-- 시작일 -->
          <td>{{ offer.start_date }}</td>

          <!-- 마감일 -->
          <td>{{ offer.end_date }}</td>

          <!-- 상태 -->
          <td>
            <span :class="['status', offer.status]">
              {{ toKoreanStatus(offer.status) }}
            </span>
          </td>

        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button
        class="page-btn"
        @click="prevPage"
        :disabled="currentPage === 1"
      >
        ← Previous
      </button>

      <div class="pages">
        <span
          v-for="n in displayedPages"
          :key="n"
          :class="['page-number', n === currentPage ? 'active' : '']"
          @click="currentPage = n"
        >
          {{ n }}
        </span>
      </div>

      <button
        class="page-btn"
        @click="nextPage"
        :disabled="currentPage === totalPages"
      >
        Next →
      </button>
    </div>
  </div>

  <!-- 캠페인 상세 모달 -->
  <CreatorCampaignDetailModal
    v-if="isDetailOpen && selectedCampaign"
    :isOpen="isDetailOpen"
    :campaign="selectedCampaign"
    @close="closeDetail"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import CreatorCampaignDetailModal from '@/components/creator/CreatorCampaignDetailModal.vue'
import { campaignAcceptances } from '@/stores/campaignAcceptance'
import { campaigns } from '@/stores/campaign'
import { brands } from '@/stores/brand'

/* Props */
const props = defineProps({
  creatorId: {
    type: Number,
    required: true
  }
})

/* 검색 / 페이지 상태 */
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

/* 모달 상태 */
const isDetailOpen = ref(false)
const selectedCampaign = ref(null)

/* 상태 한글 변환 */
const toKoreanStatus = (status) => {
  const map = {
    pending: '대기중',
    accepted: '수락됨',
    rejected: '거절됨',
    completed: '완료됨'
  }
  return map[status] || status
}

/* 캠페인 오퍼 데이터 가공 */
const offers = computed(() =>
  campaignAcceptances.value
    .filter(acc => acc.creator_id === props.creatorId)
    .map(acc => {
      const campaign = campaigns.value.find(
        c => c.campaign_id === acc.campaign_id
      )

      return {
        id: acc.campaign_acceptance_id,
        campaign,

        // ✅ 브랜드 정보는 campaign 안에 있는 값만 사용
        brand_name: campaign?.brand_name ?? '',
        brand_image: campaign?.brand_image_url ?? '',

        product_name: campaign?.product_name ?? '',
        min_follower_count: campaign?.min_follower_count ?? 0,

        styles: campaign?.style_tags
          ? campaign.style_tags.split(',')
          : [],

        start_date: campaign?.posting_start_at ?? '',
        end_date: campaign?.posting_end_at ?? '',

        status: acc.acceptance_status
      }
    })
)


/* 검색 필터 */
const filteredOffers = computed(() => {
  if (!searchQuery.value) return offers.value
  return offers.value.filter(o =>
    o.product_name.includes(searchQuery.value) ||
    o.brand_name.includes(searchQuery.value)
  )
})

/* 페이지네이션 계산 */
const totalPages = computed(() =>
  Math.ceil(filteredOffers.value.length / itemsPerPage)
)

const paginatedOffers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredOffers.value.slice(start, start + itemsPerPage)
})

const displayedPages = computed(() =>
  Array.from({ length: totalPages.value }, (_, i) => i + 1)
)

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

/* 모달 제어 */
const openDetail = (campaign) => {
  selectedCampaign.value = campaign
  isDetailOpen.value = true
}

const closeDetail = () => {
  isDetailOpen.value = false
  selectedCampaign.value = null
}
</script>

<style scoped>
/* 전체 레이아웃 */
.offers-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

/* 제목 */
.offers-title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 80px;
  color: #222;
}

/* 검색 */
.search-box {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
  position: relative;
  margin-right: 20px;
}

.search-box input {
  padding: 10px 36px 10px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  width: 220px;
}

.search-icon {
  position: absolute;
  right: 32px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

/* 테이블 */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

thead {
  border-bottom: 1px solid #eee;
}

th {
  text-align: left;
  padding: 14px 16px;
  color: #777;
}

tbody tr {
  border-bottom: 1px solid #f0f0f0;
}

td {
  padding: 18px 16px;
  vertical-align: middle;
}

/* 브랜드 */
.brand-col {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-img {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  object-fit: cover;
}

/* 스타일 태그 */
.style-col {
  display: flex;
  gap: 6px;
}

.style-tag {
  background-color: #f0eaff;
  color: #6b4fd8;
  padding: 3px 8px;
  font-size: 12px;
  border-radius: 8px;
}

/* 상태 */
.status {
  font-size: 13px;
  padding: 6px 14px;
  border-radius: 20px;
}

.status.pending {
  background-color: #fff5d6;
  color: #b88a00;
}

.status.accepted {
  background-color: #e8e8e8;
  color: #333;
}

.status.rejected {
  background-color: #ffe0e0;
  color: #cc0000;
}

.status.completed {
  background-color: #daf5df;
  color: #2e7d32;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 24px;
  gap: 20px;
}

.page-btn {
  background: white;
  border: 1px solid #d1d1d1;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pages {
  display: flex;
  gap: 8px;
}

.page-number {
  padding: 4px 8px;
  cursor: pointer;
  color: #666;
}

.page-number.active {
  font-weight: bold;
  color: #000;
}
</style>
