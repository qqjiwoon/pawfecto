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
          <th style="width: 35%">캠페인</th>
          <th style="width: 15%">업로드 일시</th>
          <th style="width: 20%">포스팅 링크</th>
          <th style="width: 15%">AI 검증 상태</th> <th style="width: 15%">제출</th> </tr>
      </thead>

      <tbody>
        <tr v-for="item in paginatedData" :key="item.deliverable_id">
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
            {{ item.created_at ? item.created_at.slice(0, 10) : '-' }}
          </td>
          
          <td>
            <div class="link-wrapper">
              <a
                v-if="item.post_url"
                :href="item.post_url"
                target="_blank"
                class="link-text"
              >
                Link
              </a>
              <span v-else class="empty-dash">-</span>
            </div>
          </td>

          <td>
            <div
              class="status-tag"
              :class="getAiStatusClass(item.ai_validation_status)"
              @click="openEditModal(item)"
              style="cursor: pointer;"
              title="클릭하여 내용 수정 및 AI 재검증"
            >
              <span class="status-dot">●</span>
              {{ getAiStatusLabel(item.ai_validation_status) }}
            </div>
          </td>

          <td>
            <div 
              v-if="item.deliverable_status === 'completed'" 
              class="status-tag completed disabled"
            >
              <span class="status-dot">●</span>
              제출 완료
            </div>

            <button 
              v-else-if="item.ai_validation_status === 'passed'" 
              class="status-tag btn-action active-submit"
              @click="openSubmitModal(item)"
            >
              <span class="status-dot">●</span>
              제출하기
            </button>
            
            <div 
              v-else 
              class="status-tag disabled"
              style="opacity: 0.5;"
            >
              <span class="status-dot">●</span>
              제출 불가
            </div>
          </td>

        </tr>

        <tr v-if="filteredData.length === 0">
          <td colspan="5" class="no-result">진행 중인 캠페인이 없습니다.</td>
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

  <SubmitModal
    v-if="isSubmitModalOpen"
    :item="submitItem"
    @close="isSubmitModalOpen = false"
    @refresh="fetchProgress"
  />

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'
import Pagination from '@/components/Pagination.vue'
import ProgressEditModal from '@/components/creator/ProgressEditModal.vue'
import SubmitModal from '@/components/creator/SubmitModal.vue'
import defaultImg from '@/assets/profile1.jpg'

const props = defineProps({
  creatorId: { type: Number, required: true },
})

const items = ref([])

onMounted(async () => {
  await fetchProgress()
})

/* 데이터 조회 함수 */
const fetchProgress = async () => {
  try {
    const res = await api.get(`/api/v1/creator/${props.creatorId}/progress/`)
    console.log("받아온 데이터:", res.data); // 데이터 확인용 로그
    items.value = res.data
  } catch (err) {
    console.error(err)
  }
}

/* 검색 및 페이지네이션 */
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

const filteredData = computed(() => {
  if (!searchQuery.value) return items.value
  const query = searchQuery.value.toLowerCase()
  return items.value.filter(item =>
    item.campaign_acceptance.campaign.product_name.toLowerCase().includes(query)
  )
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredData.value.slice(start, start + itemsPerPage)
})

const goToPage = (page) => { currentPage.value = page }

/* 모달 상태 */
const isModalOpen = ref(false)
const editingItem = ref(null)
const isSubmitModalOpen = ref(false)
const submitItem = ref(null)

const openEditModal = (item) => {
  editingItem.value = { ...item }
  isModalOpen.value = true
}

const openSubmitModal = (item) => {
  submitItem.value = { ...item }
  isSubmitModalOpen.value = true
}

/* [중요] 상태 관련 로직 수정 */
// 변수명을 ai_validation_status로 통일해야 합니다.

const getAiStatusClass = (status) => {
  if (!status || status === 'pending') return 'in-progress' // 주황 (대기)
  if (status === 'passed') return 'completed'   // 초록 (통과)
  if (status === 'failed') return 'incomplete'  // 빨강 (실패)
  return 'in-progress'
}

const getAiStatusLabel = (status) => {
  if (!status || status === 'pending') return '검증 대기'
  if (status === 'passed') return '검증 통과'
  if (status === 'failed') return '검증 실패'
  return '진행중'
}
</script>

<style scoped>
/* 기본 레이아웃 (기존 유지) */
.progress-wrapper {
  width: 95%; max-width: 1200px; margin: 40px auto;
}
.title {
  text-align: center; font-size: 40px; font-weight: 700; margin: 140px 0 80px 0; color: #222;
}
.search-box {
  display: flex; align-items: center; width: 240px; background: #fff;
  border: 1px solid #ddd; padding: 6px 12px; border-radius: 8px; margin: 0 0 20px auto;
}
.search-box input { flex: 1; border: none; outline: none; font-size: 14px; }
.search-icon { color: #888; font-size: 14px; }

/* 테이블 스타일 */
.progress-table { width: 100%; border-collapse: collapse; }
.progress-table th {
  padding: 16px 8px; font-size: 15px; font-weight: 600; border-bottom: 2px solid #eee;
  text-align: center; color: #555;
}
.progress-table td {
  padding: 18px 15px; font-size: 14px; border-bottom: 1px solid #eee;
  text-align: center; vertical-align: middle; color: #444;
}

/* 캠페인 정보 */
.campaign-info { 
  display: flex; 
  align-items: center; 
  justify-content: flex-start; 
  gap: 15px; 
}
.campaign-img { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.campaign-name { font-weight: 500; color: #333; }
.link-text { color: #6495ff; text-decoration: none; }
.link-text:hover { text-decoration: underline; }
.empty-dash { color: #ccc; }

/* --- [핵심] 상태 태그 & 버튼 디자인 통일 --- */

/* 1. 기본 모양 (4번, 5번 컬럼 공통) */
.status-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100px;         /* 너비 고정 */
  height: 36px;         /* 높이 고정 */
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;  /* 둥근 알약 모양 */
  font-size: 13px;
  font-weight: 600;
  color: #555;
  transition: all 0.2s;
  user-select: none;
}

/* 2. 상태별 점(Dot) 색상 */
.status-dot { font-size: 12px; line-height: 1; }

.completed .status-dot, 
.active-submit .status-dot { color: #4CAF50; } /* 초록 */

.incomplete .status-dot { color: #F44336; }    /* 빨강 */
.in-progress .status-dot { color: #FF9800; }   /* 주황 */
.disabled .status-dot { color: #BDBDBD; }      /* 회색 */

/* 3. 상호작용 스타일 (버튼 역할인 경우) */
button.status-tag {
  cursor: pointer;
  outline: none;
  font-family: inherit;
}

/* 제출하기 버튼 (활성 상태) */
.active-submit {
  border-color: #4CAF50; /* 테두리 초록 */
  color: #2E7D32;        /* 글자 짙은 초록 */
  background: #F1F8E9;   /* 배경 연한 초록 */
}

.active-submit:hover {
  background: #4CAF50;   /* 호버 시 배경 초록 */
  color: #FFF;           /* 글자 흰색 */
}
.active-submit:hover .status-dot { color: #FFF; } /* 호버 시 점도 흰색 */

/* 비활성 태그 (제출 불가 등) */
.disabled {
  background: #F5F5F5;
  border-color: #EEE;
  color: #999;
  cursor: default;
}

/* No Result */
.no-result { padding: 60px; color: #999; }
</style>