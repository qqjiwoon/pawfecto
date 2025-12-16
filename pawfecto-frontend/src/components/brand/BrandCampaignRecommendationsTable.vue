<template>
  <div class="recommend-wrapper">

    <h2 class="title">Creator Recommendations</h2>

    <!-- 검색 -->
    <div class="search-box">
      <input 
        type="text" 
        v-model="keyword" 
        placeholder="Search Creator..."
        @input="filterCreators"
      />
      <button class="search-btn">🔍</button>
    </div>

    <!-- 결과 없음 -->
    <p v-if="filteredCreators.length === 0" class="no-result">
      찾으시는 크리에이터가 없습니다.
    </p>

    <!-- 테이블 -->
    <table v-else class="creator-table">
      <thead>
        <tr>
          <th>크리에이터</th>
          <th>반려동물</th>
          <th>팔로워 수</th>
          <th>스타일</th>
          <th>상태</th>
        </tr>
      </thead>

      <tbody>
          <tr v-for="creator in paginatedCreators" :key="creator.id">
          <td class="creator-cell">
            <img :src="creator.profileImg" class="profile-img" />
            <div>
              <p class="name">{{ creator.name }}</p>
              <p class="handle">{{ creator.handle }}</p>
            </div>
          </td>

          <td>{{ creator.petType }}</td>
          <td>{{ creator.followers.toLocaleString() }}</td>

          <td>
            <span 
              v-for="tag in creator.styleTags" 
              :key="tag" 
              class="tag"
            >
              #{{ tag }}
            </span>
          </td>

          <td>
            <span class="status" :class="creator.status">{{ creator.status }}</span>
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
import api from "@/plugins/axios"
import Pagination from "./Pagination.vue"
import defaultImg from "@/assets/profile1.jpg"

const route = useRoute()

const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

// 원본 응답
const acceptances = ref([])

// 테이블용 가공 데이터
const creators = ref([])

// 검색
const keyword = ref("")
const filteredCreators = ref([])

// 페이지네이션
const currentPage = ref(1)
const itemsPerPage = 5

// 상태 포맷
function formatStatus(status) {
  if (!status) return ""
  return status.charAt(0).toUpperCase() + status.slice(1)
}

// 스타일 태그 표시용 변환
function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)   // "Calm (차분한)" -> "차분한"
  return m ? m[1] : raw               // 괄호 없으면 원문
}

// 데이터 조회
onMounted(async () => {
  try {
    const res = await api.get(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/acceptances/`
    )

    acceptances.value = res.data

    creators.value = res.data.map(a => ({
      id: a.campaign_acceptance_id,
      name: a.creator.name,
      handle: a.creator.sns_handle || a.creator.username,
      profileImg: a.creator.profile_image_url || defaultImg,
      petType: a.creator.pet_type,
      followers: a.creator.follower_count ?? 0,
      styleTags: (a.creator.style_tags || []).map(toKoreanTag),
      status: formatStatus(a.acceptance_status),
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
    c.name.toLowerCase().includes(k) ||
    c.handle.toLowerCase().includes(k)
  )
}

// 페이지네이션 계산
const totalPages = computed(() =>
  Math.ceil(filteredCreators.value.length / itemsPerPage)
)

const paginatedCreators = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredCreators.value.slice(start, start + itemsPerPage)
})

function goToPage(page) {
  currentPage.value = page
}
</script>


<style scoped>
.recommend-wrapper {
  width: 90%;
  max-width: 1200px;
  margin: 40px auto;
  text-align: center;
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 80px 0;
  color: #222;
}

.search-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 250px;
  background: #fff;
  border: 1px solid #ddd;
  padding: 6px 10px;
  border-radius: 8px;
  margin-bottom: 20px;
  margin-left: auto; /* 오른쪽 정렬 */
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  padding: 6px 2px;
}

.search-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.no-result {
  text-align: center;
  padding: 20px;
  color: #888;
  font-size: 15px;
}

.creator-table {
  width: 90%;
  margin: 0 auto;
  border-collapse: collapse;
}

.creator-table th {
  font-weight: 600;
  font-size: 14px;
  color: #555;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.creator-table td {
  padding: 14px 0;
  border-bottom: 1px solid #f5f5f5;
  font-size: 14px;
}

.creator-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.profile-img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
}

.tag {
  background: #f1f5ff;
  color: #6495ff;
  padding: 4px 10px;
  border-radius: 12px;
  margin-right: 6px;
  font-size: 12px;
}

.status {
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 12px;
}

.Accepted {
  background: #e5f4e8;
  color: #3c7c46;
}

.Pending {
  background: #fff7da;
  color: #967a00;
}

.Rejected {
  background: #ffe7e7;
  color: #b60000;
}

.Completed {
  background: #e8e8e8;
  color: #444;
}
</style>
