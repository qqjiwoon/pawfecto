<!-- CreatorcampaignProgressTable.vue -->
<template>
  <div class="progress-wrapper">

    <h2 class="title">Campaign Progress</h2>

    <div class="search-box">
      <input 
        type="text" 
        placeholder="Search Campaign..." 
        v-model="searchQuery" 
        @input="currentPage = 1"
      />
      <span class="search-icon">🔍</span>
    </div>

    <table class="progress-table">
      <thead>
        <tr>
          <th style="width: 45%">캠페인</th>
          <th style="width: 15%">업로드 일시</th>
          <th style="width: 25%">포스팅 링크</th>
          <th style="width: 15%">상태</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in paginatedData" :key="item.campaign_acceptance_id">

          <td>
            <div class="campaign-info">
              <img
                :src="item.campaign_acceptance.campaign.product_image_url || defaultImg"
                class="campaign-img"
              />
              <span class="campaign-name">
                {{ item.campaign_acceptance.campaign.product_name }}
              </span>
            </div>
          </td>

          <td>
            {{ item.posted_at ? item.posted_at.slice(0, 10) : '-' }}
          </td>

          <td>
            <div class="link-wrapper">
              <a
                v-if="item.post_url"
                :href="item.post_url"
                target="_blank"
                class="link-text"
              >
                {{ item.post_url }}
              </a>
              <span v-else class="empty-dash">-</span>
            </div>
          </td>

          <td>
            <div
              class="status-tag"
              :class="getStatus(item)"
              @click="openEditModal(item)"
              style="cursor: pointer;"
            >
              <span class="status-dot">●</span>
              {{ getStatusLabel(item) }}
            </div>
          </td>
        </tr>

        <tr v-if="filteredData.length === 0">
          <td colspan="4" class="no-result">진행 중인 캠페인이 없습니다.</td>
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

  <ProgressEditModal
    v-if="isModalOpen"
    :key="editingItem?.deliverable_id"
    :item="editingItem"
    @close="isModalOpen = false"
    @refresh="fetchProgress"
  />

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'
import Pagination from '@/components/Pagination.vue' // 페이지네이션 컴포넌트
import ProgressEditModal from '@/components/creator/ProgressEditModal.vue'
import defaultImg from '@/assets/profile1.jpg' // 임시 이미지

const props = defineProps({
  creatorId: {
    type: Number,
    required: true,
  },
})

const items = ref([])

onMounted(async () => {
  await fetchProgress()
})

/* 데이터 조회 함수 */
const fetchProgress = async () => {
  try {
    const res = await api.get(
      `/api/v1/creator/${props.creatorId}/progress/`
    )
    items.value = res.data
  } catch (err) {
    console.error(err)
  }
}

/* 검색 / 페이지 상태 */
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

/* 모달 상태 */
const isModalOpen = ref(false)
const editingItem = ref(null)

/* 검색 필터 */
const filteredData = computed(() => {
  if (!searchQuery.value) return items.value
  const query = searchQuery.value.toLowerCase()
  return items.value.filter(item =>
    item.campaign_acceptance.campaign.product_name
      .toLowerCase()
      .includes(query)
  )
})

/* 페이지네이션 계산 */
const totalPages = computed(() =>
  Math.ceil(filteredData.value.length / itemsPerPage)
)

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredData.value.slice(start, start + itemsPerPage)
})

const goToPage = (page) => {
  currentPage.value = page
}

/* 모달 제어 */
const openEditModal = (item) => {
  editingItem.value = { ...item }
  isModalOpen.value = true
}

/* 상태 로직 (기존 유지) */
const getStatus = (item) => {
  if (!item.ai_validation_status) return 'in-progress'
  if (item.ai_validation_status === 'pending') return 'in-progress'
  if (item.ai_validation_status === 'passed') return 'completed'
  if (item.ai_validation_status === 'failed') return 'incomplete'
}

const getStatusLabel = (item) => {
  if (!item.ai_validation_status || item.ai_validation_status === 'pending') {
    return '진행중'
  }
  if (item.ai_validation_status === 'passed') return '완료'
  if (item.ai_validation_status === 'failed') return '미완료'
}

</script>

<style scoped>
/* 1. 레이아웃 & 제목 (통일) */
.progress-wrapper {
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

/* 2. 검색창 (통일: 8px 라운드, 우측 정렬) */
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

/* 3. 테이블 스타일 (통일) */
.progress-table {
  width: 100%;
  border-collapse: collapse;
}

.progress-table th {
  padding: 16px 8px;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #eee; /* 헤더 라인 두껍게 */
  text-align: center; /* 중앙 정렬로 통일 */
  color: #333;
}

.progress-table td {
  padding: 18px 15px;
  font-size: 15px;
  border-bottom: 1px solid #eee;
  text-align: center; /* 중앙 정렬로 통일 */
  vertical-align: middle;
  color: #444;
}

/* 4. 내부 요소 스타일 */

/* 캠페인 정보 (왼쪽 정렬 유지하되 중앙 배치 느낌) */
.campaign-info {
  display: flex;
  align-items: center;
  /* justify-content: center; 가운데 정렬 */
  gap: 10px;
}

.campaign-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.campaign-name {
  font-weight: 500;
  color: #333;
}

/* 링크 스타일 */
.link-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.link-text {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #6495ff; /* 링크 색상 통일 */
  text-decoration: none;
}

.link-text:hover {
  text-decoration: underline;
  color: #333;
}

.empty-dash {
  color: #ccc;
}

/* 상태 태그 (Recommendation 스타일과 통일) */
.status-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 80px; /* 너비 통일 */
  padding: 6px 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #444;
}

.status-dot {
  font-size: 10px;
}

/* 상태별 점 색상 */
.completed .status-dot { color: #1ea35a; } /* 초록 */
.incomplete .status-dot { color: #d93232; } /* 빨강 */
.in-progress .status-dot { color: #ff9800; } /* 주황 */

/* 결과 없음 */
.no-result {
  text-align: center;
  padding: 60px !important;
  color: #999;
  font-size: 16px;
}
</style>
