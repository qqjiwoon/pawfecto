<template>
  <div class="status-wrapper">
    <h2 class="title">Campaign Status</h2>

    <div class="search-box">
      <input
        v-model="keyword"
        type="text"
        placeholder="Search Creator..."
        @input="filterCreators"
      />
      <span class="search-icon">🔍</span>
    </div>

    <table class="status-table">
      <thead>
        <tr>
          <th style="width: 20%;">크리에이터</th>
          <th style="width: 15%;">업로드 일시</th>
          <th style="width: 50%;">포스팅 링크</th>
          <th style="width: 15%;">상태</th>
        </tr>
      </thead>

      <tbody>
        <tr 
          v-for="creator in paginatedCreators" 
          :key="creator.id"
        >
          <td 
            class="creator-cell" 
            @click="openProfile(creator)" 
            style="cursor: pointer;"
          >
            <img :src="creator.profileImg" class="creator-img" />
            <div class="info">
              <p class="name">{{ creator.name }}</p>
              <p class="handle">@{{ creator.handle }}</p>
            </div>
          </td>

          <td>{{ creator.uploadDate }}</td>

          <td class="link-cell">
            <a 
              v-if="creator.postLink !== '링크 없음'" 
              :href="creator.postLink" 
              target="_blank" 
              class="post-link"
            >
              {{ creator.postLink }}
            </a>
            <span v-else class="no-link">{{ creator.postLink }}</span>
          </td>

          <td>
            <span 
              class="status-tag"
              :class="creator.status.toLowerCase()"
            >
              <span class="status-dot">●</span> {{ getStatusKor(creator.status) }}
            </span>
          </td>
        </tr>

        <tr v-if="filteredCreators.length === 0">
          <td colspan="4" class="no-result">매칭된 크리에이터가 없습니다.</td>
        </tr>
      </tbody>
    </table>

    <Pagination
      v-if="totalPages > 0"
      :currentPage="currentPage"
      :totalPages="totalPages"
      @change-page="goToPage"
    />

    <CreatorProfileModal
      v-if="isProfileModalOpen && selectedCreator"
      :creator="selectedCreator"
      @close="closeProfile"
    />
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { useRoute } from "vue-router"
import api from "@/plugins/axios"
import Pagination from '@/components/Pagination.vue'
import CreatorProfileModal from "./CreatorProfileModal.vue"
import defaultImg from "@/assets/profile1.jpg"

const route = useRoute()
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

/* 상태 관리 */
const creators = ref([])
const keyword = ref("")
const currentPage = ref(1)
const itemsPerPage = 10

const isProfileModalOpen = ref(false)
const selectedCreator = ref(null)

/* 유틸리티 및 매핑 함수 */
const getStatusKor = (status) => {
  const mapping = { Complete: "완료", Incomplete: "미완료" }
  return mapping[status] || status
}

function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

/* 데이터 로드 */
onMounted(async () => {
  try {
    const res = await api.get(`/api/v1/brand/${brandId}/campaign/${campaignId}/progress/`)
    
    creators.value = res.data.map(d => ({
      id: d.deliverable_id || d.id,
      name: d.campaign_acceptance?.creator?.name || "알 수 없음",
      handle: d.campaign_acceptance?.creator?.sns_handle || d.campaign_acceptance?.creator?.username || "unknown",
      profileImg: d.campaign_acceptance?.creator?.profile_image_url || defaultImg,
      
      // 모달용 데이터
      address: d.campaign_acceptance?.creator?.address || "",
      petType: d.campaign_acceptance?.creator?.pet_type,
      followers: d.campaign_acceptance?.creator?.follower_count ?? 0,
      styleTags: (d.campaign_acceptance?.creator?.style_tags || []).map(toKoreanTag),
      
      uploadDate: d.posted_at || "미정", 
      postLink: d.post_url || "링크 없음",
      status: d.post_url ? "Complete" : "Incomplete"
    }))
  } catch (err) {
    console.error("데이터 로드 실패:", err)
  }
})

/* 검색 및 페이지네이션 로직 */
const filterCreators = () => {
  // @input 시 호출되는 함수 (필요 시 추가 로직 작성)
  currentPage.value = 1
}

const filteredCreators = computed(() => {
  const k = keyword.value.trim().toLowerCase()
  if (!k) return creators.value
  return creators.value.filter(c =>
    c.name.toLowerCase().includes(k) || c.handle.toLowerCase().includes(k)
  )
})

const totalPages = computed(() => {
  return Math.ceil(filteredCreators.value.length / itemsPerPage)
})

const paginatedCreators = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredCreators.value.slice(start, start + itemsPerPage)
})

const goToPage = (page) => {
  currentPage.value = page
}

// 검색어 변경 시 페이지 초기화
watch(keyword, () => {
  currentPage.value = 1
})

/* 모달 제어 */
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
/* 1. 레이아웃 (Recommendation과 동일하게 맞춤) */
.status-wrapper {
  width: 95%;
  max-width: 1200px;
  margin: 40px auto; /* 상하 여백 40px로 통일 */
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 80px 0;
  color: #222;
}

/* 2. 검색창 (Recommendation 스타일: border-radius 8px, 우측 정렬) */
.search-box {
  display: flex;
  align-items: center;
  width: 240px;
  background: #fff;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 8px; /* 20px -> 8px로 변경 */
  margin: 0 0 20px auto; /* margin auto를 사용하여 우측 정렬 */
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

/* 3. 테이블 스타일 (Recommendation과 헤더/셀 스타일 통일) */
.status-table {
  width: 100%;
  border-collapse: collapse;
}

.status-table th {
  padding: 16px 8px; /* 패딩 확대 */
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #eee; /* 헤더 라인 두껍게 (2px) */
  text-align: center;
  color: #333; /* 글자색 진하게 (#777 -> #333) */
}

.status-table td {
  padding: 18px 8px;
  font-size: 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
  vertical-align: middle;
  color: #444; /* 기본 글자색 지정 */
}

/* 4. 내부 요소 스타일 */
.creator-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
}

.creator-img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.info .name { 
  font-weight: 600; 
  color: #333; 
  margin: 0; 
  font-size: 15px; 
}

/* 마우스 올렸을 때 이름 색상 변경 */
.creator-cell:hover .name {
  color: #6495ff;
}

.info .handle { 
  font-size: 13px; 
  color: #888; 
  margin: 0; 
}

/* 마우스 올렸을 때 이름 색상 변경 */
.creator-cell:hover .handle {
  color: #B8A58D;
}

.post-link {
  color: #6495ff;
  text-decoration: none;
  word-break: break-all;
}
.no-link { color: #bbb; }

/* 상태 태그 (기존 로직 유지하되 디자인 톤 앤 매너 맞춤) */
.status-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 80px;
  padding: 6px 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #444;
}

.status-dot { font-size: 10px; }
.complete .status-dot { color: #1ea35a; }
.incomplete .status-dot { color: #d93232; }

.no-result {
  text-align: center;
  padding: 60px !important;
  color: #999;
  font-size: 16px;
}
</style>
