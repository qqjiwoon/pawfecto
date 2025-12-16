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

        <button class="update-btn" @click="goUpdate">
          Update
        </button>
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
})

/* -------------------------------
   스타일 태그 파싱 (한국어 표시)
-------------------------------- */
const parsedStyles = computed(() => {
  const styles = campaign.value?.style_tag
  if (!styles) return []

  const toKorean = (raw) => {
    const m = raw.match(/\(([^)]+)\)/)
    return m ? m[1] : raw
  }

  if (typeof styles === 'string') {
    return styles.split(',').map(s => toKorean(s.trim()))
  }

  if (Array.isArray(styles)) {
    return styles.map(s => toKorean(String(s)))
  }

  return []
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

/* Update button */
.update-btn {
  position: absolute;
  bottom: 0;
  right: 30;

  width: 500px;   /* content-box와 동일 */
  padding: 14px;
  background: #695845;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>
