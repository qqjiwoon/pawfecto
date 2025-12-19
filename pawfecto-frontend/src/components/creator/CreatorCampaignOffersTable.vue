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
        <tr
          v-for="offer in paginatedOffers"
          :key="offer.campaign_acceptance_id ?? offer.campaign?.id"
        >
          <!-- 브랜드 정보 -->
          <td>
            <div class="brand-col">
              <img :src="offer.brand_image" class="brand-img" />
              <!-- 나중에 브랜드 이미지 이렇게 불러오기!!! -->
              <!-- <img
                :src="offer.campaign.brand.profile_image_url"
                class="brand-img"
              /> -->
              <span>{{ offer.campaign.brand.name }}</span>
            </div>
          </td>

          <!-- 상품명 (상세 모달 오픈) -->
          <td
            class="product-name"
            @click="openDetail(offer.campaign)"
          >
            {{ offer.campaign.product_name }}
          </td>

          <!-- 최소 팔로워 수 -->
          <td>{{ offer.creator.follower_count.toLocaleString() }}</td>

          <!-- 스타일 태그 -->
          <td>
            <div class="style-col">
              <span
                v-for="tag in offer.campaign.style_tags"
                :key="tag.id"
                class="style-tag"
              >
                #{{ tag.code }}
              </span>

            </div>
          </td>

          <!-- 시작일 -->
          <td>{{ offer.campaign.requested_at.slice(0, 10) }}</td>

          <!-- 마감일 -->
          <td>{{ offer.campaign.application_deadline_at }}</td>

          <!-- 상태 -->
          <td class="status-cell">
            <div class="status-wrapper">

              <!-- 상태 버튼 (항상 하나) -->
              <button
                class="status-btn"
                :class="[statusClass(offer.acceptance_status), {
                  'is-locked': offer.acceptance_status === 'accepted'
                }]"
                @click="toggleStatusMenu(offer)"
              >
                {{ getCreatorStatusKor(offer.acceptance_status) }}
              </button>

              <!-- 드롭다운 메뉴 -->
              <ul
                v-if="openStatusId === offer.campaign_acceptance_id"
                class="status-menu"
              >
                <!-- 1️. 대기중 -->
                <template v-if="offer.acceptance_status === 'pending'">
                  <li>
                    <button
                      class="status-option Approved"
                      @click="changeStatus(offer, 'accepted')"
                    >
                      수락
                    </button>
                  </li>
                  <li>
                    <button
                      class="status-option Rejected"
                      @click="changeStatus(offer, 'rejected')"
                    >
                      거절
                    </button>
                  </li>
                </template>

                <!-- 2️. 거절 후 -->
                <template v-else-if="offer.acceptance_status === 'rejected'">
                  <li>
                    <button
                      class="status-option Approved"
                      @click="changeStatus(offer, 'accepted')"
                    >
                      다시 수락
                    </button>
                  </li>
                </template>
              </ul>
            </div>
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

  <!-- Toast -->
  <div v-if="showToast" class="toast">
    {{ toastMessage }}
  </div>

</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import api from '@/plugins/axios'

import CreatorCampaignDetailModal from '@/components/creator/CreatorCampaignDetailModal.vue'

/* Props */
const props = defineProps({
  creatorId: {
    type: Number,
    required: true,
  },
})

const offers = ref([])
const safeOffers = computed(() => offers.value ?? [])

onMounted(async () => {
  try {
    const res = await api.get(
      `/api/v1/creator/${props.creatorId}/offers/`
    )
    offers.value = res.data
  } catch (err) {
    console.error(err)
    openToast('캠페인 오퍼를 불러오지 못했습니다.')
  }
})

onUnmounted(() => {
  window.removeEventListener('click', handleOutsideClick)
})


/* 검색 / 페이지 상태 */
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

/* 모달 상태 */
const isDetailOpen = ref(false)
const selectedCampaign = ref(null)

// 토스트 상태
const showToast = ref(false)
const toastMessage = ref('')

// 토스트 열기
const openToast = (message) => {
  toastMessage.value = message
  showToast.value = true

  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

// 상태 변경 함수
const statusClass = (status) => {
  return {
    pending: 'Pending',
    accepted: 'Approved',
    rejected: 'Rejected',
  }[status]
}
const openStatusId = ref(null)

const toggleStatusMenu = (offer) => {
  if (offer.acceptance_status === 'accepted') return

  openStatusId.value =
    openStatusId.value === offer.campaign_acceptance_id
      ? null
      : offer.campaign_acceptance_id
}
const getCreatorStatusKor = (status) => {
  return {
    pending: '대기중',
    accepted: '수락함',
    rejected: '거절함',
  }[status]
}

const changeStatus = async (offer, nextStatus) => {
  const prevStatus = offer.acceptance_status

  // 수락 시 최종 확인
  if (nextStatus === 'accepted' && prevStatus !== 'accepted') {
    const confirmed = window.confirm(
      '한 번 수락하면 거절할 수 없습니다.\n수락하시겠습니까?'
    )

    if (!confirmed) {
      return
    }
  }

  try {
    if (nextStatus === 'accepted') {
      await api.post(
        `/api/v1/creator/offers/${offer.campaign_acceptance_id}/accept/`
      )
      offer.acceptance_status = 'accepted'
      openToast('캠페인을 수락했습니다.')
    }

    if (nextStatus === 'rejected') {
      await api.post(
        `/api/v1/creator/offers/${offer.campaign_acceptance_id}/reject/`
      )
      offer.acceptance_status = 'rejected'
      openToast('캠페인을 거절했습니다.')
    }
  } catch (err) {
    offer.acceptance_status = prevStatus

    const message =
      err.response?.data?.error ??
      '상태 변경에 실패했습니다.'

    openToast(message)
    console.error(err)
  }
}


/* 검색 필터 */
const filteredOffers = computed(() => {
  if (!searchQuery.value) return safeOffers.value

  return safeOffers.value.filter(o =>
    o.campaign.product_name.includes(searchQuery.value) ||
    o.campaign.brand.name.includes(searchQuery.value)
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
const openDetail = (offer) => {
  selectedCampaign.value = offer
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
/* 상태 버튼 공통 */
.status-btn,
.status-option {
  display: inline-flex;              /* ✔ 중앙 정렬 */
  align-items: center;
  justify-content: center;

  width: 112px;                      /* ✔ 실제 크기 */
  height: 38px;

  padding: 0;                        
  border-radius: 12px;

  font-size: 13px;                   
  font-weight: 600;

  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
}

.status-cell {
  padding: 18px 24px;   /* 좌우 여백 증가 */
  text-align: center;
}


/* 드롭다운 옵션 전용 */
.status-option {
  margin: 4px 0;
}
.is-locked {
  cursor: default !important;
  opacity: 0.9;
}

.Pending { background: #fff7da; color: #967a00; }
.Approved { background: #e5f4e8; color: #3c7c46; }
.Rejected { background: #ffe7e7; color: #b60000; }

.status-wrapper {
  position: relative;
  display: inline-block;
}

.status-menu {
  position: absolute;
  top: 115%;
  left: 50%;
  list-style: none; 
  transform: translateX(-50%);
  width: 100%;
  min-width: 90px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  z-index: 20;
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

.toast {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 12px 24px;
  border-radius: 20px;
  font-size: 14px;
  z-index: 3000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

</style>
