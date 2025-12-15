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
                :class="{ active: campaign.pet_type === 'cat' }">
                Cat
              </button>
              <button 
                class="pet-btn" 
                :class="{ active: campaign.pet_type === 'dog' }">
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
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { campaigns } from "@/stores/campaign"

const route = useRoute()
const router = useRouter()

// URL의 campaign_id 가져오기
const campaignId = Number(route.params.campaign_id)

// 캠페인 데이터 찾기
const campaign = computed(() =>
  campaigns.value.find(c => c.campaign_id === campaignId)
)

// style_tags 문자열 → 배열로 변환
const parsedStyles = computed(() => {
  const styles = campaign.value?.style_tags

  if (!styles) return []

  // 문자열인 경우 → 배열로 변환
  if (typeof styles === "string") {
    return styles.split(",")
  }

  // 배열인 경우 → 그대로 반환
  if (Array.isArray(styles)) {
    return styles
  }

  return []
})

// 업데이트 버튼
function goUpdate() {
  router.push({
    name: "brand-update-campaign",
    params: {
      brand_id: route.params.brand_id,
      campaign_id: route.params.campaign_id
    }
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
