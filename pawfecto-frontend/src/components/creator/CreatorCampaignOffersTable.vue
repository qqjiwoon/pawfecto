<template>
  <div class="offers-wrapper">
    <h2 class="title">Campaign Offers</h2>

    <div class="search-box">
      <input 
        type="text" 
        placeholder="Search Product..." 
        v-model="searchQuery" 
        @input="currentPage = 1"
      />
      <span class="search-icon">🔍</span>
    </div>

    <table class="offers-table">
      <thead>
        <tr>
          <th style="width: 15%">브랜드</th>
          <th style="width: 30%">상품</th>
          <th style="width: 10%">최소 팔로워</th>
          <th style="width: 15%">스타일</th>
          <th style="width: 10%">시작일</th>
          <th style="width: 10%">마감일</th>
          <th style="width: 10%">상태</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="offer in paginatedOffers"
          :key="offer.campaign_acceptance_id ?? offer.campaign?.id"
        >
          <td>
            <div class="brand-col">
              <img :src="offer.brand_image || defaultProfile" class="brand-img" />
              <span class="brand-name">{{ offer.campaign.brand.name }}</span>
            </div>
          </td>

          <td
            class="product-name"
            @click="openDetail(offer.campaign)"
          >
            {{ offer.campaign.product_name }}
          </td>

          <td>{{ offer.campaign.min_follower_count.toLocaleString() }}</td>

          <td>
            <div class="tag-container">
              <span
                v-for="tag in offer.campaign.style_tags"
                :key="tag.id || tag"
                class="tag"
              >
                #{{ toKoreanTag(tag) }}
              </span>
            </div>
          </td>

          <td>{{ offer.campaign.requested_at.slice(0, 10) }}</td>

          <td>{{ offer.campaign.application_deadline_at }}</td>

          <td class="status-cell">
            <div class="status-wrapper">
              <button
                class="status-btn"
                :class="[statusClass(offer.acceptance_status), {
                  'is-locked': offer.acceptance_status === 'accepted'
                }]"
                @click="toggleStatusMenu(offer)"
              >
                {{ getCreatorStatusKor(offer.acceptance_status) }}
              </button>

              <ul
                v-if="openStatusId === offer.campaign_acceptance_id"
                class="status-menu"
              >
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
        
        <tr v-if="filteredOffers.length === 0">
          <td colspan="7" class="no-result">진행 가능한 캠페인이 없습니다.</td>
        </tr>
      </tbody>
    </table>

    <Pagination
      v-if="totalPages > 0"
      :currentPage="currentPage"
      :totalPages="totalPages"
      @change-page="goToPage"
    />
  </div>

  <CreatorCampaignDetailModal
    v-if="isDetailOpen && selectedCampaign"
    :isOpen="isDetailOpen"
    :campaign="selectedCampaign"
    @close="closeDetail"
  />

  <div v-if="showToast" class="toast">
    {{ toastMessage }}
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import api from '@/plugins/axios'
import Pagination from '@/components/Pagination.vue'
import CreatorCampaignDetailModal from '@/components/creator/CreatorCampaignDetailModal.vue'
import defaultProfile from '@/assets/profile1.jpg' 

/* Props */
const props = defineProps({
  creatorId: {
    type: Number,
    required: true,
  },
})

const offers = ref([])
const safeOffers = computed(() => offers.value ?? [])

// [수정] 스타일 태그 변환 함수 (Creator Recommendations 코드와 동일한 로직)
function toKoreanTag(t) {
  // 문자열이면 그대로, 객체면 name_ko > label > name 순으로 확인
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  // "English(Korean)" 형태인 경우 괄호 안의 내용 추출
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

onMounted(async () => {
  window.addEventListener('click', handleOutsideClick)
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

const handleOutsideClick = (event) => {
  if (openStatusId.value !== null && !event.target.closest('.status-wrapper')) {
    openStatusId.value = null
  }
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

  if (nextStatus === 'accepted' && prevStatus !== 'accepted') {
    const confirmed = window.confirm(
      '한 번 수락하면 거절할 수 없습니다.\n수락하시겠습니까?'
    )
    if (!confirmed) return
  }

  try {
    const action = nextStatus === 'accepted' ? 'accept' : 'reject'
    await api.post(
      `/api/v1/creator/offers/${offer.campaign_acceptance_id}/${action}/`
    )
    offer.acceptance_status = nextStatus
    openToast(nextStatus === 'accepted' ? '캠페인을 수락했습니다.' : '캠페인을 거절했습니다.')
    openStatusId.value = null
  } catch (err) {
    offer.acceptance_status = prevStatus
    const message = err.response?.data?.error ?? '상태 변경에 실패했습니다.'
    openToast(message)
    console.error(err)
  }
}

/* 검색 필터 */
const filteredOffers = computed(() => {
  if (!searchQuery.value) return safeOffers.value
  const query = searchQuery.value.toLowerCase()
  return safeOffers.value.filter(o =>
    o.campaign.product_name.toLowerCase().includes(query) ||
    o.campaign.brand.name.toLowerCase().includes(query)
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

const goToPage = (page) => {
  currentPage.value = page
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
/* 1. 레이아웃 & 제목 */
.offers-wrapper {
  width: 95%;
  max-width: 1200px;
  margin: 40px auto;
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 80px 0;
  color: #222;
}

/* 2. 검색창 (8px 라운드, 우측 정렬) */
.search-box {
  display: flex;
  align-items: center;
  width: 240px;
  background: #fff;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 8px;
  margin: 0 0 20px auto;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
}

.search-icon {
  color: #888;
  font-size: 14px;
}

/* 3. 테이블 스타일 */
.offers-table {
  width: 100%;
  border-collapse: collapse;
}

.offers-table th {
  padding: 16px 8px;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #eee;
  text-align: center;
  color: #333;
}

.offers-table td {
  padding: 18px 15px;
  font-size: 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
  vertical-align: middle;
  color: #444;
}

/* 4. 내부 컬럼 스타일 */

/* 브랜드 컬럼 */
.brand-col {
  display: flex;
  align-items: center;
  /* justify-content: center; */
  gap: 10px;
}

.brand-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.brand-name {
  font-weight: 500;
  color: #333;
}

/* 상품명 */
.product-name {
  cursor: pointer;
  color: #222;
  font-weight: 500;
  transition: color 0.2s;
}
.product-name:hover {
  color: #6495ff;
  text-decoration: underline;
}

/* 태그 컨테이너 */
.tag-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 4px;
}

/* 스타일 태그 */
.tag {
  background: #f1f5ff;
  color: #6495ff;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

/* 상태 셀 및 버튼 스타일 */
.status-cell {
  position: relative;
  min-width: 120px;
}

.status-wrapper {
  position: relative;
  display: inline-block;
}

.status-btn,
.status-option {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 34px;
  padding: 0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  text-align: center;
}

.status-option {
  width: 100%;
  margin: 4px 0;
}

/* 상태별 색상 */
.Pending { background: #fff7da; color: #967a00; }
.Approved { background: #e5f4e8; color: #3c7c46; }
.Rejected { background: #ffe7e7; color: #b60000; }

.is-locked {
  cursor: default !important;
  opacity: 0.9;
}

/* 드롭다운 메뉴 */
.status-menu {
  position: absolute;
  top: 115%;
  left: 50%;
  transform: translateX(-50%);
  width: 110px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  z-index: 20;
  list-style: none;
  margin: 0;
}

/* 결과 없음 */
.no-result {
  text-align: center;
  padding: 60px !important;
  color: #999;
  font-size: 16px;
}

/* 토스트 메시지 */
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
