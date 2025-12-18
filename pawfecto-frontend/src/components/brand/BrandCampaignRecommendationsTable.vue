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
          <td class="creator-cell">
            <img :src="creator.profileImg" class="profile-img" />
            <div class="info">
              <p class="name">{{ creator.name }}</p>
              <p class="handle">{{ creator.handle }}</p>
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
// 크리에이터 신청 현황 조회 (캠페인별)
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import api from "@/plugins/axios" // axios 인스턴스 (Bearer 토큰 설정 포함 가정)
import Pagination from "./Pagination.vue"
import defaultImg from "@/assets/profile1.jpg"

const route = useRoute()
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

// 테이블용 가공 데이터
const creators = ref([])

// 검색
const keyword = ref("")
const filteredCreators = ref([])

// 페이지네이션
const currentPage = ref(1)
const itemsPerPage = 5

// 브랜드 상태 드롭다운 옵션
const openStatusId = ref(null)
const brandStatusOptions = ["Pending", "Approved", "Rejected"]

// 브랜드 심사 상태 한국어 매핑
const getBrandStatusKor = (status) => {
  const mapping = {
    Pending: "검토 중",
    Approved: "승인",
    Rejected: "거절",
  }
  return mapping[status] || status
}

// 크리에이터 매칭 상태 한국어 매핑
const getCreatorStatusKor = (status) => {
  const mapping = {
    Pending: "응답 대기",
    Accepted: "수락",
    Rejected: "거절",
    Completed: "완료",
  }
  return mapping[status] || status
}

// 상태 포맷 (API 원본 데이터를 TitleCase로 변환)
const formatStatus = (s) => s ? s.charAt(0).toUpperCase() + s.slice(1) : ""

// 스타일 태그 표시용 변환
function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

// 데이터 조회
onMounted(async () => {
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
    filteredCreators.value = []
  }
})

// 검색 필터
function filterCreators() {
  const k = keyword.value.toLowerCase()
  filteredCreators.value = creators.value.filter(c =>
    c.name.toLowerCase().includes(k) || c.handle.toLowerCase().includes(k)
  )
  currentPage.value = 1
}

// 페이지네이션 계산
const totalPages = computed(() => Math.ceil(filteredCreators.value.length / itemsPerPage))

const paginatedCreators = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredCreators.value.slice(start, start + itemsPerPage)
})

function goToPage(page) {
  currentPage.value = page
}

// 드롭다운 토글 (이미 심사가 끝난 건은 열리지 않도록 방어)
const toggleStatusMenu = (creator) => {
  if (creator.brandStatus !== 'Pending') {
    return // 이미 완료된 상태면 메뉴를 열지 않음
  }
  openStatusId.value = openStatusId.value === creator.id ? null : creator.id
}

// 브랜드 상태 변경 및 DB 저장
async function changeBrandStatus(creator, status) {
  // 1. 방어 코드: 백엔드 로직에 맞춰 Pending일 때만 진행
  if (creator.brandStatus !== 'Pending') {
    alert("이미 심사가 완료된 크리에이터입니다.")
    return
  }

  // 2. 선택한 상태에 따른 엔드포인트 액션 결정 (Approved -> approve, Rejected -> reject)
  const action = status === "Approved" ? "approve" : "reject"
  
  try {
    // 3. API 요청 (백엔드 URL 구조: .../acceptances/{id}/{action}/)
    const url = `/api/v1/brand/${brandId}/campaign/${campaignId}/acceptances/${creator.id}/${action}/`
    const res = await api.patch(url)
    
    // 4. 성공 시 로컬 데이터 업데이트 및 알림
    creator.brandStatus = status
    openStatusId.value = null
    alert(res.data.message || `${getBrandStatusKor(status)} 처리가 완료되었습니다.`)
  } catch (err) {
    console.error(err)
    // 백엔드에서 보낸 에러 메시지가 있으면 노출 (예: "이미 승인 또는 거절된...")
    const errorMsg = err.response?.data?.error || "처리 중 오류가 발생했습니다."
    alert(errorMsg)
  }
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

.info .name { font-weight: 600; color: #333; font-size: 15px; }
.info .handle { font-size: 13px; color: #888; }

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
  font-weight: 600;
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
}

.status-option {
  margin: 3px 0;
}
</style>
