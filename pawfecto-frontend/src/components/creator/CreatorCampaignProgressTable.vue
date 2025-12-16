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
              <!-- 이미지 나중에 아래 것으로 고치기 -->
              <!-- <img
                :src="item.campaign_acceptance.campaign.product_image_url"
                class="campaign-img"
              /> -->
              <span class="campaign-name">
                {{ item.campaign_acceptance.campaign.product_name }}
              </span>
            </div>
          </td>

          <!-- 업로드 일시 -->
          <td>
            {{ item.posted_at ? item.posted_at.slice(0, 10) : '-' }}
          </td>


          <!-- 포스팅 링크 -->
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

          <!-- 상태 (수정 가능) -->
          <td>
            <div
              class="status-badge"
              @click="openEditModal(item)"
            >
              <span :class="['dot', item.deliverable_status]"></span>
              <span class="status-text">
                {{ toKoreanStatus(item.deliverable_status) }}
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
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'
import ProgressEditModal from '@/components/creator/ProgressEditModal.vue'

const props = defineProps({
  creatorId: {
    type: Number,
    required: true,
  },
})

const items = ref([])

onMounted(async () => {
  const res = await api.get(
    `/api/v1/creator/${props.creatorId}/progress/`
  )
  items.value = res.data
})

const emit = defineEmits(['save', 'close'])

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
  return items.value.filter(item =>
    item.campaign_acceptance.campaign.product_name
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())
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

/* 모달 제어 */
const openEditModal = (item) => {
  editingItem.value = { ...item }
  isModalOpen.value = true
}

const saveEditedItem = (updated) => {
  emit('save', updated)
  isModalOpen.value = false
}

/* 상태 한글 */
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
