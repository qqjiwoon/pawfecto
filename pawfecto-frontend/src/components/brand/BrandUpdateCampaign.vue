<template>
  <div class="update-wrapper">

    <h1 class="page-title">Update Campaign</h1>

    <!-- 상품 정보 -->
    <section class="section">
      <h2>Product</h2>

      <!-- 상품명 -->
      <div class="input-group">
        <label>상품명</label>
        <input v-model="campaign.product_name" type="text" />
      </div>

      <!-- 사진 -->
      <div class="input-group">
        <label>상품 이미지</label>
        <input type="file" @change="onFileChange" />
      </div>

      <!-- 상품 상세 -->
      <div class="input-group">
        <label>상품 상세</label>
        <textarea v-model="campaign.product_description"></textarea>
      </div>
    </section>

    <!-- 가이드라인 -->
    <section class="section">
      <h2>Guideline details</h2>

      <div class="input-group">
        <label>캠페인 대상 동물 종류</label>
        <select v-model="campaign.pet_type">
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
        </select>
      </div>

      <div class="input-group">
        <label>최소 팔로워 수 조건</label>
        <input v-model="campaign.min_follower_count" type="number" />
      </div>

      <div class="input-group">
        <label>필요한 크리에이터 수</label>
        <input v-model="campaign.required_creator_count" type="number" />
      </div>

      <!-- 스타일 태그 -->
      <div class="style-tags">
        <h2>Style Tags</h2>
        <div class="tag-list">
          <button
            v-for="tag in allTags"
            :key="tag"
            class="tag"
            :class="{ active: (campaign.style_tags || []).includes(tag) }"
            @click="toggleStyle(tag)"
            type="button"
          >
            #{{ tag }}
          </button>
        </div>
      </div>
    </section>

    <!-- 기간 -->
    <section class="section">
      <h2>Campaign Duration</h2>

      <div class="input-group">
        <label>캠페인 시작일</label>
        <input v-model="campaign.posting_start_at" type="date" />
      </div>

      <div class="input-group">
        <label>캠페인 마감일</label>
        <input v-model="campaign.posting_end_at" type="date" />
      </div>
    </section>

    <button class="save-btn" @click="updateCampaign">
      SAVE
    </button>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useCampaignStore } from "@/stores/campaign"

const route = useRoute()
const router = useRouter()

const campaignId = Number(route.params.campaign_id)
const brandId = Number(route.params.brand_id)

// ✅ Pinia store
const campaignStore = useCampaignStore()

// 수정용 캠페인
const campaign = ref(null)

// 스타일 태그
const allTags = [
  "outdoor","energetic","no_preference","minimal",
  "aesthetic","heartfelt","cozy","wholesome","funny","calm"
]

// 최초 진입 시 캠페인 단건 조회
onMounted(async () => {
  try {
    await campaignStore.fetchCampaign(campaignId)

    // deep copy (수정용)
    campaign.value = JSON.parse(
      JSON.stringify(campaignStore.campaignDetail)
    )

    if (!Array.isArray(campaign.value.style_tags)) {
      campaign.value.style_tags = []
    }
  } catch (err) {
    console.error(err)
    alert("캠페인 정보를 불러오지 못했습니다.")
  }
})

// 스타일 태그 토글
function toggleStyle(tag) {
  if (campaign.value.style_tags.includes(tag)) {
    campaign.value.style_tags =
      campaign.value.style_tags.filter(t => t !== tag)
  } else {
    campaign.value.style_tags.push(tag)
  }
}

// 이미지
const imageFile = ref(null)
function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    campaign.value.product_image_url = URL.createObjectURL(file)
  }
}

// 업데이트
async function updateCampaign() {
  try {
    await campaignStore.updateCampaign(
      brandId,
      campaignId,
      {
        product_name: campaign.value.product_name,
        product_description: campaign.value.product_description,
        product_image_url: campaign.value.product_image_url,
        pet_type: campaign.value.pet_type,
        min_follower_count: campaign.value.min_follower_count,
        required_creator_count: campaign.value.required_creator_count,
        posting_start_at: campaign.value.posting_start_at,
        posting_end_at: campaign.value.posting_end_at,
        style_tags: campaign.value.style_tags,
      }
    )

    alert("캠페인이 수정되었습니다.")

    router.push({
      name: "brand-campaign-detail",
      params: { brand_id: brandId, campaign_id: campaignId }
    })
  } catch (err) {
    console.error(err)
    alert("캠페인 수정에 실패했습니다.")
  }
}
</script>


<style scoped>
.update-wrapper {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 20px;
  text-align: center;
}

.section {
  margin-bottom: 40px;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.input-group label {
  font-size: 14px;
  margin-bottom: 6px;
}

input,
select,
textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

textarea {
  height: 120px;
}

/* 태그 스타일 */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #aaa;
  background: #f5f5f5;
  cursor: pointer;
}

.tag.active {
  background: #5b4636;
  color: white;
  border-color: #5b4636;
}

.save-btn {
  width: 100%;
  background: #5b4636;
  padding: 12px 0;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
}
</style>
