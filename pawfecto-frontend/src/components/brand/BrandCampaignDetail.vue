<template>
  <div class="campaign-detail-page" v-if="campaign">

    <div class="campaign-info">
      
      <img :src="campaignImageUrl" class="product-img" />
      
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
            <span class="value">{{ campaign.required_creator_count }}명</span>
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

          <hr class="divider" />

          <div class="row items-start">
            <span class="label">AI 검증 조건</span>
            <div class="req-list">
              <div v-for="(req, idx) in campaign.requirements" :key="idx" class="req-item">
                <span class="req-type">[{{ getReqTypeLabel(req.requirement_type) }}]</span>
                <span class="req-desc">{{ req.description }}</span>
                <span v-if="req.is_required" class="req-badge">필수</span>
              </div>
              <div v-if="!campaign.requirements?.length" class="empty-msg">설정된 조건이 없습니다.</div>
            </div>
          </div>

          <div class="row">
            <span class="label">지원 마감일</span>
            <span class="value date">{{ campaign.application_deadline_at }}</span>
          </div>

          <div class="row">
            <span class="label">게시 기간</span>
            <span class="value date">
              {{ campaign.posting_start_at }} ~ {{ campaign.posting_end_at }}
            </span>
          </div>

        </div>

        <div class="button-group">
          <button class="update-btn" @click="goUpdate">수정</button>
          <button class="delete-btn" @click="goDelete">삭제</button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCampaignDetail } from '@/api/campaign'
import api from "@/plugins/axios"
import { useWarningStore } from '@/stores/warning'

const warningStore = useWarningStore()
const route = useRoute()
const router = useRouter()

const brandId = Number(route.params.brand_id)
const campaignId = Number(route.params.campaign_id)
const campaign = ref(null)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://127.0.0.1:8000"

const campaignImageUrl = computed(() => {
  const url = campaign.value?.product_image_url
  if (!url) return ""
  // http로 시작하면 그대로 쓰고, 아니면 백엔드 주소(API_BASE_URL)를 붙임
  return url.startsWith("http") ? url : `${API_BASE_URL}${url}`
})

onMounted(async () => {
  try {
    const res = await fetchCampaignDetail(brandId, campaignId)
    campaign.value = res.data
  } catch (err) {
    warningStore.open("데이터를 불러오는 중 오류가 발생했습니다.")
  }
})

const parsedStyles = computed(() => {
  const tags = campaign.value?.style_tags
  if (!Array.isArray(tags)) return []
  return tags
    .filter(tag => tag && tag.name)
    .map(tag => {
      const m = tag.name.match(/\(([^)]+)\)/)
      return m ? m[1] : tag.name
    })
})

/* AI 타입 한글 변환 함수 */
function getReqTypeLabel(type) {
  const labels = {
    object: '사물',
    scene: '배경',
    action: '행동',
    text: '텍스트'
  }
  return labels[type] || type
}

function goUpdate() {
  router.push({ name: 'brand-update-campaign', params: { brand_id: brandId, campaign_id: campaignId } })
}

async function goDelete() {
  const isConfirmed = await warningStore.confirm("정말 이 캠페인을 삭제하시겠습니까?")
  if (!isConfirmed) return
  try {
    await api.delete(`/api/v1/brand/${brandId}/campaign/${campaignId}/delete/`)
    warningStore.open("캠페인이 성공적으로 삭제되었습니다.")
    router.push({ name: "brand-campaign-list", params: { brand_id: brandId } })
  } catch (err) {
    warningStore.open("삭제 중 오류가 발생했습니다.")
  }
}
</script>

<style scoped>
/* 기존 스타일 유지 */
.campaign-info {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 115px;
  margin: 50px auto;
  max-width: 1200px;
}

.product-img {
  width: 420px;
  height: 520px;
  object-fit: cover;
  border-radius: 12px;
}

.content-box { width: 500px; }

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

/* AI 조건처럼 내용이 길 때 상단 정렬 */
.row.items-start {
  align-items: flex-start;
}

.label {
  width: 180px; /* 기존 250px에서 약간 조정 (공간 확보) */
  font-size: 14px;
  color: #888;
}

.value {
  font-size: 15px;
  font-weight: 500;
}

.value.date {
  color: #555;
  letter-spacing: -0.2px;
}

/* AI Requirements Style */
.req-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.req-item {
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.req-type {
  color: #7e6b5a;
  font-weight: 600;
  white-space: nowrap;
}

.req-desc {
  color: #444;
}

.req-badge {
  font-size: 10px;
  background: #ffeded;
  color: #ff4d4f;
  padding: 1px 6px;
  border-radius: 4px;
  border: 1px solid #ffccc7;
}

.divider {
  border: 0;
  border-top: 1px solid #f0f0f0;
  margin: 24px 0;
}

.empty-msg {
  color: #ccc;
  font-size: 13px;
}

/* 기존 버튼 및 기타 스타일 생략 (동일하게 유지됨) */
.pet-btn {
  border: 1px solid #ddd;
  background: #fff;
  padding: 6px 18px;
  border-radius: 6px;
  cursor: default;
  margin-right: 8px;
  color: #777;
}
.pet-btn.active { background: #C4B199; border-color: #C4B199; color: white; }

.style-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.style-tag {
  padding: 6px 12px; background: #f5f1ec; border-radius: 8px;
  font-size: 13px; border: 1px solid #e0d6cc; color: #7d6c61;
}

.button-group { display: flex; gap: 12px; margin-top: 40px; }
.update-btn, .delete-btn { border-radius: 50px; padding: 14px; font-size: 16px; font-weight: 600; cursor: pointer; }
.update-btn { flex: 2.5; background: #695845; color: white; border: 1px solid #695845}
.delete-btn { flex: 1; background: #f5f1ec; color: #8B3A3A; border: 1px solid #e0d6cc; }
</style>
