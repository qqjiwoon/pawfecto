<template>
  <div class="recommend-wrapper">
    <h2 class="title">Creator Recommendations</h2>

    <div class="action-bar">
      <button class="recommend-btn" @click="requestAutoMatch">
        ✨ AI 크리에이터 추천받기
      </button>

      <div class="search-box">
        <input
          v-model="keyword"
          type="text"
          placeholder="Search Creator..."
          @input="filterCreators"
        />
        <span class="search-icon">🔍</span>
      </div>
    </div>

    <table class="creator-table">
      <thead>
        <tr>
          <th style="width: 20%">크리에이터</th>
          <th style="width: 12%">반려동물</th>
          <th style="width: 12%">팔로워 수</th>
          <th>스타일</th>
          <th style="width: 12%">브랜드 심사</th>
          <th style="width: 12%">크리에이터 매칭</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="creator in paginatedCreators" :key="creator.id">
          <td class="creator-cell" @click="openProfile(creator)" style="cursor: pointer;">
            <img :src="creator.profileImg" class="profile-img" />
            <div class="info">
              <p class="name">{{ creator.name }}</p>
              <p class="handle">@{{ creator.handle }}</p>
            </div>
          </td>
          <td>{{ creator.petType }}</td>
          <td>{{ creator.followers.toLocaleString() }}</td>
          <td>
            <div class="tag-container">
              <span v-for="tag in creator.styleTags" :key="tag" class="tag">
                #{{ tag }}
              </span>
            </div>
          </td>
          <td class="status-cell">
            <div class="status-wrapper">
              <button
                class="status-btn"
                :class="[creator.brandStatus, { 'is-locked': creator.brandStatus !== 'Pending' }]"
                @click="toggleStatusMenu(creator)"
              >
                {{ getBrandStatusKor(creator.brandStatus) }}
              </button>
              <ul v-if="openStatusId === creator.id" class="status-menu">
                <li v-for="status in brandStatusOptions" :key="status">
                  <button
                    v-if="status !== 'Pending'"
                    class="status-option"
                    :class="status"
                    @click="changeBrandStatus(creator, status)"
                  >
                    {{ getBrandStatusKor(status) }}
                  </button>
                </li>
              </ul>
            </div>
          </td>
          <td>
            <span class="status-text" :class="'text-' + creator.creatorStatus">
              {{ getCreatorStatusKor(creator.creatorStatus) }}
            </span>
          </td>
        </tr>

        <tr v-if="paginatedCreators.length === 0">
          <td colspan="6" class="no-result" style="text-align: center; padding: 40px 0;">
            찾으시는 크리에이터가 없습니다.
          </td>
        </tr>
      </tbody>
    </table>

    <CreatorProfileModal
      v-if="isProfileModalOpen && selectedCreator"
      :creator="selectedCreator"
      @close="closeProfile"
    />

    <Pagination 
      v-if="totalPages > 0"
      :currentPage="currentPage" 
      :totalPages="totalPages" 
      @change-page="goToPage" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRoute } from "vue-router"
import api from "@/plugins/axios"
import Pagination from '@/components/Pagination.vue'
import CreatorProfileModal from "./CreatorProfileModal.vue"
import defaultImg from "@/assets/profile1.jpg"
import { useWarningStore } from '@/stores/warning'
import { useCreatorStore } from '@/stores/creator';

const route = useRoute()
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)
const warningStore = useWarningStore()

// 추천 크리에이터 store 사용
const creatorStore = useCreatorStore();

// 추천 크리에이터 목록
const recommendedCreators = ref(creatorStore.recommendedCreators);

// 데이터 상태
const creators = ref([])
const keyword = ref("")
const filteredCreators = ref([])

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 5

// 드롭다운 및 모달 상태
const openStatusId = ref(null)
const brandStatusOptions = ["Pending", "Approved", "Rejected"]
const isProfileModalOpen = ref(false)
const selectedCreator = ref(null)

// 한국어 매핑 함수들
const getBrandStatusKor = (s) => ({ Pending: "검토 중", Approved: "승인", Rejected: "거절" }[s] || s)
const getCreatorStatusKor = (s) => ({ Pending: "응답 대기", Accepted: "매칭 완료", Rejected: "매칭 거절", Completed: "완료" }[s] || s)
const formatStatus = (s) => s ? s.charAt(0).toUpperCase() + s.slice(1) : ""

function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

// [핵심] 데이터 로드 함수 분리 (재사용을 위해)
const fetchCreators = async () => {
  try {
    const res = await api.get(`/api/v1/brand/${brandId}/campaign/${campaignId}/acceptances/`)
    creators.value = res.data.map(a => ({
      id: a.campaign_acceptance_id,
      name: a.creator.name,
      handle: a.creator.sns_handle || a.creator.username,
      profileImg: a.creator.profile_image_url || defaultImg,
      petType: a.creator.pet_type,
      followers: a.creator.follower_count ?? 0,
      styleTags: (a.creator.style_tags || []).map(toKoreanTag),
      brandStatus: formatStatus(a.brand_decision_status),
      creatorStatus: formatStatus(a.acceptance_status),
    }))
    // 데이터 로드 후 필터 재적용 (검색어 유지)
    filterCreators()
  } catch (err) {
    warningStore.open("데이터를 불러오는 중 오류가 발생했습니다.")
  }
}


// [핵심 2] 크리에이터 자동 추천 요청 함수
const requestAutoMatch = async () => {
  const warningStore = useWarningStore();

  try {
    // 서버로 추천 크리에이터 API 요청
    const response = await api.post(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/auto-match/`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // JWT 토큰 추가
        }
      }
    );

    // 추천된 크리에이터들을 store에 저장
    await creatorStore.recommendCreators(campaignId, brandId);

    // 추천된 크리에이터 목록을 새로고침하여 갱신
    recommendedCreators.value = creatorStore.recommendedCreators;

    warningStore.open("새로운 크리에이터가 추천 목록에 추가되었습니다!");
  } catch (error) {
    console.error(error);
    const msg = error.response?.data?.error || "추천 과정에서 오류가 발생했습니다.";
    warningStore.open(msg);
  }
};



// 초기 로드
onMounted(async () => {
  window.addEventListener('click', handleOutsideClick)
  await fetchCreators()
})

onUnmounted(() => {
  window.removeEventListener('click', handleOutsideClick)
})

// 검색 및 페이지네이션 로직
function filterCreators() {
  const k = keyword.value.toLowerCase()
  filteredCreators.value = creators.value.filter(c =>
    c.name.toLowerCase().includes(k) || c.handle.toLowerCase().includes(k)
  )
  // 검색 시 페이지 1로 리셋 (필요하다면)
  // currentPage.value = 1 
}

const totalPages = computed(() => Math.ceil(filteredCreators.value.length / itemsPerPage))
const paginatedCreators = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredCreators.value.slice(start, start + itemsPerPage)
})
function goToPage(page) { currentPage.value = page }

// 드롭다운 및 상태 변경 로직
const toggleStatusMenu = (creator) => {
  if (creator.brandStatus !== 'Pending') return
  openStatusId.value = openStatusId.value === creator.id ? null : creator.id
}

const handleOutsideClick = (event) => {
  if (openStatusId.value !== null && !event.target.closest('.status-wrapper')) {
    openStatusId.value = null
  }
}

async function changeBrandStatus(creator, status) {
  if (creator.brandStatus !== 'Pending') return
  const isConfirmed = await warningStore.confirm(
    "심사 상태를 변경하면 이후 취소나 수정이 불가능합니다. 그래도 심사를 확정하시겠습니까?"
  )
  if (!isConfirmed) return

  const action = status === "Approved" ? "approve" : "reject"
  try {
    await api.patch(`/api/v1/brand/${brandId}/campaign/${campaignId}/acceptances/${creator.id}/${action}/`)
    creator.brandStatus = status
    openStatusId.value = null
    warningStore.open(`${getBrandStatusKor(status)} 처리가 완료되었습니다.`)
  } catch (err) {
    const errorMsg = err.response?.data?.error || "처리 중 오류가 발생했습니다."
    warningStore.open(errorMsg)
  }
}

const openProfile = (creator) => {
  selectedCreator.value = creator
  isProfileModalOpen.value = true
}
const closeProfile = () => {
  isProfileModalOpen.value = false
  selectedCreator.value = null
}
</script>

<style scoped>
.recommend-wrapper {
  width: 95%;
  max-width: 1200px;
  margin: 40px auto;
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 60px 0; /* 마진 조정 */
  color: #222;
}

/* [추가] 액션 바 스타일 (버튼과 검색창 배치) */
.action-bar {
  display: flex;
  justify-content: space-between; /* 양 끝 정렬 */
  align-items: center;
  margin-bottom: 20px;
}

/* [추가] 추천 버튼 스타일 */
.recommend-btn {
  background-color: #6495ff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  box-shadow: 0 4px 6px rgba(100, 149, 255, 0.2);
}

.recommend-btn:hover {
  background-color: #5078d4;
  transform: translateY(-1px);
}

.search-box {
  display: flex;
  align-items: center;
  width: 240px;
  background: #fff;
  border: 1px solid #ddd;
  padding: 8px 12px; /* 패딩 약간 조정 */
  border-radius: 8px;
  /* margin-left: auto; 제거 (flex space-between 사용) */
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

/* 아래는 기존 스타일 유지 */
.creator-table { width: 100%; border-collapse: collapse; }
.creator-table th { padding: 16px 8px; font-size: 16px; font-weight: 600; border-bottom: 2px solid #eee; text-align: center; color: #333; }
.creator-table td { padding: 18px 8px; font-size: 15px; border-bottom: 1px solid #eee; text-align: center; vertical-align: middle; color: #444; }
.creator-cell { display: flex; align-items: center; gap: 12px; text-align: left; }
.creator-cell:hover .name { color: #6495ff; }
.creator-cell:hover .handle { color: #B8A58D; }
.profile-img { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.info .name { font-weight: 600; color: #333; font-size: 15px; margin: 0; }
.info .handle { font-size: 13px; color: #888; margin: 0; }
.tag-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 4px; }
.tag { background: #f1f5ff; color: #6495ff; padding: 4px 10px; border-radius: 12px; font-size: 12px; }
.status-btn, .status-option { display: inline-block; width: 100%; max-width: 90px; padding: 6px 0; border-radius: 8px; font-size: 13px; border: none; text-align: center; cursor: pointer; font-weight: 500; transition: all 0.2s ease; }
.is-locked { cursor: default; opacity: 0.9; }
.status-btn:not(.is-locked):hover { filter: brightness(0.98); transform: translateY(-1px); }
.status-text { font-size: 14px; }
.Pending { background: #fff7da; color: #967a00; }
.Approved { background: #e5f4e8; color: #3c7c46; }
.Rejected { background: #ffe7e7; color: #b60000; }
.text-Pending { color: #f39c12; }
.text-Accepted { color: #27ae60; }
.text-Rejected { color: #e74c3c; }
.text-Completed { color: #2980b9; }
.status-cell { min-width: 100px; }
.status-wrapper { position: relative; display: inline-block; width: 100%; }
.status-menu { position: absolute; top: 115%; left: 50%; transform: translateX(-50%); width: 100%; min-width: 90px; background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); z-index: 20; list-style: none; margin: 0; animation: fadeIn 0.15s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateX(-50%) translateY(-10px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
.status-option { margin: 3px 0; }
.no-result { text-align: center; padding: 60px !important; color: #999; font-size: 16px; }
</style>