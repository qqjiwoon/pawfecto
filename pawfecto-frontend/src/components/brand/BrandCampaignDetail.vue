<template>
  <div class="campaign-detail-page" v-if="campaign">

    <div class="campaign-info">
      
      <img :src="campaign.product_image_url" class="product-img" />
      
      <div class="content-box">
        <h1>{{ campaign.product_name }}</h1>

        <p class="desc" v-html="campaign.product_description"></p>

        <div class="pref">
          <h3>Creator Preferences</h3>

          <div class="row">
            <span class="label">캠페인 대상 동물 종류</span>
            <div class="pet-type">
              <button 
                class="pet-btn" 
                :class="{ active: campaign.target_pet_type === 'cat' }">
                Cat
              </button>
              <button 
                class="pet-btn" 
                :class="{ active: campaign.target_pet_type === 'dog' }">
                Dog
              </button>
            </div>
          </div>

          <div class="row">
            <span class="label">최소 팔로워 수</span>
            <span class="value">{{ campaign.min_follower_count.toLocaleString() }}</span>
          </div>

          <div class="row">
            <span class="label">필요 크리에이터 수</span>
            <span class="value">{{ campaign.required_creator_count }}</span>
          </div>

          <div class="row">
            <span class="label">스타일</span>
            <div class="style-tags">
              <span
                v-for="tag in parsedStyles"
                :key="tag"
                class="style-tag"
              >
                #{{ tag }}
              </span>
            </div>
          </div>

        </div>

        <!-- 수정 / 삭제 버튼 -->
        <div class="button-group">
          <button class="update-btn" @click="goUpdate">수정</button>
          <button class="delete-btn" @click="goDelete">삭제</button>
        </div>

      </div>
    </div>

    </div>
</template>


<script setup>
/* ================================
   캠페인 상세 조회
================================ */

import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCampaignDetail } from '@/api/campaign'
import api from "@/plugins/axios"
import { useWarningStore } from '@/stores/warning'

const warningStore = useWarningStore()

const route = useRoute()
const router = useRouter()

// URL 파라미터
const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)

// 캠페인 상태
const campaign = ref(null)

/* -------------------------------
   상세 데이터 로드
-------------------------------- */
onMounted(async () => {
  const res = await fetchCampaignDetail(brandId, campaignId)
  campaign.value = res.data
  console.log("style_tags:", res.data.style_tags)
})

/* -------------------------------
   스타일 태그 파싱 (한국어 표시)
-------------------------------- */
const parsedStyles = computed(() => {
  const tags = campaign.value?.style_tags
  if (!Array.isArray(tags)) return []

  return tags
    .filter(tag => tag && tag.name)   // 핵심
    .map(tag => {
      const m = tag.name.match(/\(([^)]+)\)/)
      return m ? m[1] : tag.name
    })
})

/* -------------------------------
   수정 페이지 이동
-------------------------------- */
function goUpdate() {
  router.push({
    name: 'brand-update-campaign',
    params: {
      brand_id: brandId,
      campaign_id: campaignId,
    },
  })
}

/* -------------------------------
   캠페인 삭제
-------------------------------- */
async function goDelete() {
  // 1. 커스텀 컨펌창 호출 (사용자 선택을 기다림)
  const isConfirmed = await warningStore.confirm("정말 이 캠페인을 삭제하시겠습니까?")
  
  if (!isConfirmed) return // 취소를 누르면 중단

  try {
    const res = await api.delete(`/api/v1/brand/${brandId}/campaign/${campaignId}/delete/`)
    
    // 2. 성공 알림창 호출
    warningStore.open("캠페인이 성공적으로 삭제되었습니다.")
    
    router.push({ name: "brand-campaign-list", params: { brand_id: brandId } })
  } catch (err) {
    const errorMsg = err.response?.data?.error || "삭제 중 오류가 발생했습니다."
    // 3. 에러 알림창 호출
    warningStore.open(errorMsg)
  }
}

</script>


<style scoped>
.campaign-info {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 115px;
  margin: 50px auto;
  max-width: 1200px;
  position: relative;
}

.product-img {
  width: 420px;
  height: 520px;
  object-fit: cover;
  border-radius: 12px;
}

/* Right content */
.content-box {
  width: 500px;
}

.desc {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 45px;
}

.pref .row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.label {
  width: 250px;
}

.value {
  font-size: 15px;
}

/* Pet Type Buttons */
.pet-btn {
  border: 1px solid #ddd;
  background: #fff;
  padding: 6px 18px;
  border-radius: 6px;
  cursor: default;
  margin-right: 8px;
  color: #777;
}

.pet-btn.active {
  background: #C4B199;
  border-color: #C4B199;
  color: white;
}

/* Style tags */
.style-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.style-tag {
  padding: 6px 12px;
  background: #f5f1ec;
  border-radius: 8px;
  font-size: 13px;
  border: 1px solid #e0d6cc;
  color: #7d6c61;
}

/* button */
.button-group {
  display: flex;
  gap: 12px;
  margin-top: 40px;
  width: 100%;
}

.update-btn,
.delete-btn {
  border-radius: 50px;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.update-btn {
  flex: 2.5;         /* 삭제 버튼보다 2.5배 더 길어집니다 */
  background: #695845;
  color: white;
}

.update-btn:hover {
  background: #564839; /* 마우스 올리면 조금 더 진하게 */
  border-color: #564839;
}

.delete-btn {
  flex: 1;           /* 상대적으로 짧은 너비 */
  background: #f5f1ec; /* 배경을 연하게 해서 심리적 거부감을 줄임 */
  color: #8B3A3A;    /* 텍스트만 삭제 컬러 사용 */
  border: 1px solid #e0d6cc;
}

.delete-btn:hover {
  background: #ffe7e7;
  border-color: #8B3A3A;
}
</style>
