<template>
  <div class="progress-table">

    <!-- 페이지 제목 -->
    <h2 class="page-title">Campaign Progress</h2>

    <!-- 검색 영역 -->
    <div class="search-box">
      <input type="text" placeholder="Search Campaign..." v-model="searchQuery" />
      <span class="search-icon">🔍</span>
    </div>

    <!-- 진행 캠페인 테이블 -->
    <table>
      <thead>
        <tr>
          <th>캠페인</th>
          <th>업로드 일시</th>
          <th>포스팅 링크</th>
          <th>상태</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in paginatedData" :key="item.campaign_acceptance_id">

          <!-- 캠페인 정보 -->
          <td>
            <div class="campaign-info">
              <img :src="item.campaign_image" class="campaign-img" />
              <span class="campaign-name">{{ item.campaign_name }}</span>
            </div>
          </td>

          <!-- 업로드 일시 -->
          <td>{{ item.upload_date || '-' }}</td>

          <!-- 포스팅 링크 -->
          <td>
            <div class="link-wrapper">
              <a
                v-if="item.post_link"
                :href="item.post_link"
                target="_blank"
                class="link-text"
              >
                {{ item.post_link }}
              </a>
              <span v-else class="empty-dash">-</span>
            </div>
          </td>

          <!-- 상태 (수정 가능) -->
          <td>
            <div
              class="status-badge"
              @click="openEditModal(item)"
            >
              <span :class="['dot', item.status]"></span>
              <span class="status-text">
                {{ toKoreanStatus(item.status) }}
              </span>
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

  <!-- 상태 수정 모달 -->
  <ProgressEditModal
    v-if="isModalOpen"
    :item="editingItem"
    @save="saveEditedItem"
    @close="isModalOpen = false"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

import { campaignAcceptances } from '@/stores/campaignAcceptance'
import { deliverables } from '@/stores/deliverable'

import ProgressEditModal from '@/components/creator/ProgressEditModal.vue'

/* Route */
const route = useRoute()
const creatorId = computed(() => Number(route.params.creator_id))

/* 검색 / 페이지 상태 */
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

/* 모달 상태 */
const isModalOpen = ref(false)
const editingItem = ref(null)

/* 진행 캠페인 데이터 */
const progressData = computed(() =>
  campaignAcceptances.value
    .filter(acc => acc.creator_id === creatorId.value)
    .map(acc => {
      const deliverable = deliverables.value.find(
        d => d.campaign_acceptance_id === acc.campaign_acceptance_id
      )
      const campaign = campaigns.value.find(
        c => c.campaign_id === acc.campaign_id
      )

      return {
        campaign_acceptance_id: acc.campaign_acceptance_id,

        campaign_name: campaign?.product_name ?? '캠페인 정보 없음',
        campaign_image: campaign?.product_image_url ?? '',

        upload_date: deliverable?.posted_at ?? '',
        post_link: deliverable?.post_url ?? '',

        status:
          deliverable?.deliverable_status === 'completed'
            ? 'completed'
            : 'incomplete'
      }
    })
)

/* 검색 필터 */
const filteredData = computed(() => {
  if (!searchQuery.value) return progressData.value
  return progressData.value.filter(item =>
    item.campaign_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

/* 페이지네이션 */
const totalPages = computed(() =>
  Math.ceil(filteredData.value.length / itemsPerPage)
)

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredData.value.slice(start, start + itemsPerPage)
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

/* 상태 수정 */
const openEditModal = (item) => {
  editingItem.value = { ...item }
  isModalOpen.value = true
}

const saveEditedItem = (updated) => {
  const d = deliverables.value.find(
    x => x.campaign_acceptance_id === updated.campaign_acceptance_id
  )

  if (d) {
    d.posted_at = updated.upload_date
    d.post_url = updated.post_link
    d.deliverable_status = updated.status
  } else {
    deliverables.value.push({
      id: Date.now(),
      campaign_acceptance_id: updated.campaign_acceptance_id,
      posted_at: updated.upload_date,
      post_url: updated.post_link,
      deliverable_status: updated.status
    })
  }

  isModalOpen.value = false
}

/* 상태 한글 변환 */
const toKoreanStatus = (status) => {
  if (status === 'completed') return '완료'
  if (status === 'incomplete') return '미완료'
  return status
}
</script>

<style scoped>
/* 전체 레이아웃 */
.progress-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

/* 제목 */
.page-title {
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
  padding: 14px 16px;
  text-align: left;
  color: #777;
}

td {
  padding: 18px 16px;
  vertical-align: middle;
}

tbody tr {
  border-bottom: 1px solid #f0f0f0;
}

/* 캠페인 정보 */
.campaign-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.campaign-img {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  object-fit: cover;
}

.campaign-name {
  font-weight: 500;
}

/* 링크 */
.link-wrapper {
  display: flex;
  align-items: center;
}

.link-text {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #666;
  text-decoration: none;
}

.link-text:hover {
  text-decoration: underline;
  color: #333;
}

.empty-dash {
  color: #ccc;
}

/* 상태 배지 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid #eee;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.status-badge:hover {
  background-color: #f9f9f9;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.completed {
  background-color: #4caf50;
}

.dot.incomplete {
  background-color: #f44336;
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
  border: 1px solid #d1d1d1;
  background: white;
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
