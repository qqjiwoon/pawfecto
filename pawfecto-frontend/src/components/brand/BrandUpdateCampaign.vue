<template>
  <div class="update-wrapper" v-if="campaign">

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
        <select v-model="campaign.target_pet_type">
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
        <label>Style Tags</label>
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

      <div class="input-group">
        <label>지원 마감일</label>
        <input v-model="campaign.application_deadline_at" type="date" />
      </div>
    </section>

    <button class="save-btn" @click="updateCampaign">
      저장
    </button>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useCampaignStore } from "@/stores/campaign"
import api from "@/plugins/axios"

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

onMounted(async () => {
  try {
    const res = await api.get(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/`
    )

    campaign.value = {
      ...res.data,
      style_tags: Array.isArray(res.data.style_tags)
        ? res.data.style_tags.map(t => t.code ?? t)
        : [],
    }
  } catch (err) {
    console.error(err.response)
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
    await api.put(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/update/`,
      {
        product_name: campaign.value.product_name,
        product_description: campaign.value.product_description,
        product_image_url: campaign.value.product_image_url,

        target_pet_type: campaign.value.target_pet_type,
        min_follower_count: campaign.value.min_follower_count,
        required_creator_count: campaign.value.required_creator_count,

        application_deadline_at: campaign.value.application_deadline_at,
        posting_start_at: campaign.value.posting_start_at,
        posting_end_at: campaign.value.posting_end_at,

        style_tags: campaign.value.style_tags,
      }
    )

    alert("캠페인이 수정되었습니다.")
    router.push({
      name: "brand-campaign-detail",
      params: { brand_id: brandId, campaign_id: campaignId },
    })
  } catch (err) {
    alert(
      err.response?.data?.error ||
      "캠페인 수정에 실패했습니다."
    )
  }
}

</script>


<style scoped>
/* =========================
   Update Campaign 스타일
========================= */

.update-wrapper {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px 100px;
}

/* 페이지 타이틀 */
.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 56px;
  text-align: center;
}

/* 섹션 공통 */
.section {
  margin-bottom: 56px;
}

.section h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
}

/* 입력 그룹 */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.input-group label {
  font-size: 13px;
  color: #555;
  margin-bottom: 8px;
}

/* input / select / textarea */
input,
select,
textarea {
  padding: 12px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
  background: #fff;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #7e6b5a;
}

textarea {
  min-height: 140px;
  resize: vertical;
}

/* =========================
   스타일 태그
========================= */

.style-tags label {
  font-size: 13px;
  color: #555;
  margin-bottom: 10px;
  display: block;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid #ddd;
  background: #fff;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tag:hover {
  border-color: #7e6b5a;
  color: #7e6b5a;
}

.tag.active {
  background: #7e6b5a;
  color: #fff;
  border-color: #7e6b5a;
}

/* =========================
   저장 버튼
========================= */

.save-btn {
  width: 220px;
  margin: 0 auto;
  display: block;
  background: #3f3f3f;
  padding: 14px 0;
  border-radius: 999px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  border: none;
}

.save-btn:hover {
  background: #2f2f2f;
}

</style>
