<template>
  <div class="status-wrapper">
    <h2 class="title">Campaign Status</h2>

    <div class="search-box">
      <input
        v-model="search"
        type="text"
        placeholder="Search Creator..."
        @keyup.enter="filterSearch"
      />
      <button class="search-btn" @click="filterSearch">🔍</button>
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
          v-for="creator in filteredCreators" 
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
            <a :href="creator.postLink" target="_blank" class="post-link">
              {{ creator.postLink }}
            </a>
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

    <CreatorProfileModal
      v-if="isProfileModalOpen && selectedCreator"
      :creator="selectedCreator"
      @close="closeProfile"
    />
    
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import api from "@/plugins/axios"
import CreatorProfileModal from "./CreatorProfileModal.vue" // 1. 모달 임포트
import defaultImg from "@/assets/profile1.jpg"

const route = useRoute()
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

const search = ref("")
const creators = ref([])

// 2. 모달 관련 상태 추가
const isProfileModalOpen = ref(false)
const selectedCreator = ref(null)

const getStatusKor = (status) => {
  const mapping = { Complete: "완료", Incomplete: "미완료" }
  return mapping[status] || status
}

// 태그 변환 함수 (기존 recommendations에서 가져옴)
function toKoreanTag(t) {
  const raw = typeof t === "string" ? t : (t?.name_ko || t?.label || t?.name || "")
  const m = raw.match(/\(([^)]+)\)/)
  return m ? m[1] : raw
}

onMounted(async () => {
  try {
    const res = await api.get(`/api/v1/brand/${brandId}/campaign/${campaignId}/progress/`)
    
    creators.value = res.data.map(d => ({
      id: d.deliverable_id || d.id,
      name: d.campaign_acceptance?.creator?.name || "알 수 없음",
      handle: d.campaign_acceptance?.creator?.sns_handle || d.campaign_acceptance?.creator?.username || "unknown",
      profileImg: d.campaign_acceptance?.creator?.profile_image_url || defaultImg,
      
      // [중요] 모달에 보여줄 상세 정보들 추가 매핑
      address: d.campaign_acceptance?.creator?.address || "", // 주소 추가!
      petType: d.campaign_acceptance?.creator?.pet_type,
      followers: d.campaign_acceptance?.creator?.follower_count ?? 0,
      styleTags: (d.campaign_acceptance?.creator?.style_tags || []).map(toKoreanTag),
      
      uploadDate: d.uploaded_at || "미정", 
      postLink: d.post_url || "링크 없음",
      status: d.post_url ? "Complete" : "Incomplete"
    }))
  } catch (err) {
    console.error("로드 실패:", err)
  }
})

// 3. 모달 제어 함수
const openProfile = (creator) => {
  selectedCreator.value = creator
  isProfileModalOpen.value = true
}
const closeProfile = () => {
  isProfileModalOpen.value = false
  selectedCreator.value = null
}

const filteredCreators = computed(() => {
  const k = search.value.trim().toLowerCase()
  if (!k) return creators.value
  return creators.value.filter(c =>
    c.name.toLowerCase().includes(k) || c.handle.toLowerCase().includes(k)
  )
})
</script>


<style scoped>
.status-wrapper {
  width: 95%;
  max-width: 1200px;
  margin: 40px auto;
}

.title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  margin: 100px 0 40px 0;
  color: #222;
}

/* 검색창 */
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

.search-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #888;
}

/* 테이블 디자인 - Recommendations 스타일 통일 */
.status-table {
  width: 100%;
  border-collapse: collapse;
}

.status-table th {
  padding: 16px 8px;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #eee;
  text-align: center;
  color: #333;
}

.status-table td {
  padding: 18px 8px;
  font-size: 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
  vertical-align: middle;
  color: #444;
}

/* 크리에이터 셀 */
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

.info .name { font-weight: 600; color: #333; margin: 0; }
.info .handle { font-size: 13px; color: #888; margin: 0; }

.post-link {
  color: #6495ff;
  text-decoration: none;
}

/* 상태 태그 - 요청하신 스타일 적용 */
.status-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  max-width: 80px;
  padding: 6px 0;
  background: #fff;           /* 흰색 배경 */
  border: 1px solid #ddd;     /* 회색 실선 테두리 */
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #444;
}

.status-dot {
  font-size: 10px;
}

/* 상태별 점(Dot) 색상 */
.complete .status-dot {
  color: #1ea35a; /* 초록색 점 */
}

.incomplete .status-dot {
  color: #d93232; /* 빨간색 점 */
}

.no-result {
  text-align: center;
  padding: 40px !important;
  color: #888;
}
</style>
