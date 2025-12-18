<template>
  <div class="recommend-wrapper">
    <h2 class="title">Creator Recommendations</h2>

    <div class="search-box">
      <input
        type="text"
        v-model="keyword"
        placeholder="Search Creator..."
        @input="filterCreators"
      />
      <span class="search-icon">🔍</span>
    </div>

    <p v-if="filteredCreators.length === 0" class="no-result">
      찾으시는 크리에이터가 없습니다.
    </p>

    <table v-else class="creator-table">
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

          <CreatorProfileModal
            v-if="isProfileModalOpen && selectedCreator"
            :creator="selectedCreator"
            @close="closeProfile"
          />

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
      </tbody>
    </table>

    <Pagination
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
import Pagination from "./Pagination.vue"
import CreatorProfileModal from "./CreatorProfileModal.vue" // 모달 임포트
import defaultImg from "@/assets/profile1.jpg"

const route = useRoute()
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

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
const isProfileModalOpen = ref(false) // 모달 오픈 여부
const selectedCreator = ref(null)     // 선택된 크리에이터 정보

// 한국어 매핑 함수들
const getBrandStatusKor = (s) => ({ Pending: "검토 중", Approved: "승인", Rejected: "거절" }[s] || s)
const getCreatorStatusKor = (s) => ({ Pending: "응답 대기", Accepted: "수락", Rejected: "거절", Completed: "완료" }[s] || s)

// 유틸리티 함수
const formatStatus = (s) => s ? s.charAt(0).toUpperCase() + s.slice(1) : ""
function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

// [핵심] 데이터 로드 및 이벤트 리스너 통합
onMounted(async () => {
  window.addEventListener('click', handleOutsideClick)
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
    filteredCreators.value = [...creators.value]
  } catch (err) {
    console.error(err)
  }
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
  currentPage.value = 1
}

const totalPages = computed(() => Math.ceil(filteredCreators.value.length / itemsPerPage))
const paginatedCreators = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredCreators.value.slice(start, start + itemsPerPage)
})
function goToPage(page) { currentPage.value = page }

// 드롭다운 제어
const toggleStatusMenu = (creator) => {
  if (creator.brandStatus !== 'Pending') return
  openStatusId.value = openStatusId.value === creator.id ? null : creator.id
}

const handleOutsideClick = (event) => {
  if (openStatusId.value !== null && !event.target.closest('.status-wrapper')) {
    openStatusId.value = null
  }
}

// [핵심] 브랜드 상태 변경
async function changeBrandStatus(creator, status) {
  if (creator.brandStatus !== 'Pending') return
  if (!confirm("심사 상태를 변경하면 이후 취소나 수정이 불가능합니다.\n그래도 심사를 확정하시겠습니까?")) return

  const action = status === "Approved" ? "approve" : "reject"
  try {
    await api.patch(`/api/v1/brand/${brandId}/campaign/${campaignId}/acceptances/${creator.id}/${action}/`)
    creator.brandStatus = status
    openStatusId.value = null
    alert(`${getBrandStatusKor(status)} 처리가 완료되었습니다.`)
  } catch (err) {
    alert(err.response?.data?.error || "처리 중 오류가 발생했습니다.")
  }
}

// [핵심] 크리에이터 프로필 모달 제어
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
  font-size: 32px;
  font-weight: 700;
  margin: 100px 0 40px 0;
  text-align: center;
  color: #222;
}

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

.creator-table {
  width: 100%;
  border-collapse: collapse;
}

.creator-table th {
  padding: 16px 8px;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #eee;
  text-align: center;
  color: #333;
}

.creator-table td {
  padding: 18px 8px;
  font-size: 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
  vertical-align: middle;
}

.creator-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
}

.profile-img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.info .name { 
  font-weight: 600; 
  color: #333; 
  font-size: 15px; 
  margin: 0;
}

.info .handle { 
  font-size: 13px; 
  color: #888; 
  margin: 0;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 4px;
}

.tag {
  background: #f1f5ff;
  color: #6495ff;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

/* 브랜드 심사 버튼 스타일 */
.status-btn, .status-option {
  display: inline-block;
  width: 100%;
  max-width: 90px;
  padding: 6px 0;
  border-radius: 8px;
  font-size: 13px;
  border: none;
  text-align: center;
  cursor: pointer;
  font-weight: 500;
}

/* 완료된 상태일 때 마우스 포인터 변경 */
.is-locked {
  cursor: default !important;
  opacity: 0.9;
}

/* 크리에이터 매칭 텍스트 스타일 */
.status-text {
  font-size: 14px;
}

/* 배경색이 있는 브랜드 상태 클래스 */
.Pending { background: #fff7da; color: #967a00; }
.Approved { background: #e5f4e8; color: #3c7c46; }
.Rejected { background: #ffe7e7; color: #b60000; }

/* 글자색만 있는 크리에이터 상태 클래스 */
.text-Pending { color: #f39c12; }
.text-Accepted { color: #27ae60; }
.text-Rejected { color: #e74c3c; }
.text-Completed { color: #2980b9; }

/* 드롭다운 설정 */
.status-cell {
  min-width: 100px;
}

.status-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}

.status-menu {
  position: absolute;
  top: 115%;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  min-width: 90px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  z-index: 20;
  list-style: none;
  margin: 0;
  animation: fadeIn 0.15s ease-out; /* 부드럽게 나타나기 */
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-50%) translateY(-10px); }
  to { opacity: 1; transform: translateX(-50%) translateY(0); }
}

.status-option {
  margin: 3px 0;
}
</style>
