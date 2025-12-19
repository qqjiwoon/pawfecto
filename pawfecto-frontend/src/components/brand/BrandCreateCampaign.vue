<template>
  <div class="update-wrapper">

    <h1 class="page-title">Create Campaign</h1>

    <!-- 상품 정보 -->
    <section class="section">
      <h2>Product</h2>

      <div class="input-group">
        <label>상품명</label>
        <input v-model="campaign.product_name" type="text" />
      </div>

      <div class="input-group">
        <label>상품 이미지</label>
        <input type="file" @change="onFileChange" />
      </div>

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
            :key="tag.code"
            class="tag"
            :class="{ active: campaign.style_tags.includes(tag.code) }"
            @click="toggleStyle(tag.code)"
            type="button"
          >
            #{{ tag.name }}
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

    <button class="save-btn" @click="createCampaign">
      생성
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useCampaignStore } from "@/stores/campaign"
import { useWarningStore } from '@/stores/warning'

const route = useRoute()
const router = useRouter()
const brandId = Number(route.params.brand_id)

const warningStore = useWarningStore() 
const campaignStore = useCampaignStore()

/* -------------------------------
   생성용 캠페인 상태 (Update와 동일 구조)
-------------------------------- */
const campaign = ref({
  product_name: "",
  product_description: "",
  product_image_url: "",

  target_pet_type: "dog",
  min_follower_count: 0,
  required_creator_count: 1,

  posting_start_at: "",
  posting_end_at: "",

  style_tags: [],
})

/* -------------------------------
   스타일 태그 (Update와 동일)
-------------------------------- */
const allTags = [
  { id: 1, code: "energetic", name: "활발한" },
  { id: 2, code: "calm", name: "차분한" },
  { id: 3, code: "funny", name: "웃긴" },
  { id: 4, code: "wholesome", name: "힐링되는" },
  { id: 5, code: "cozy", name: "포근한" },
  { id: 6, code: "heartfelt", name: "감동적인" },
  { id: 7, code: "aesthetic", name: "감각적인" },
  { id: 8, code: "minimal", name: "깔끔한" },
  { id: 9, code: "outdoor", name: "야외감성" },
  { id: 10, code: "no_preference", name: "상관없음" },
]


function toggleStyle(code) {
  if (campaign.value.style_tags.includes(code)) {
    campaign.value.style_tags =
      campaign.value.style_tags.filter(t => t !== code)
  } else {
    campaign.value.style_tags.push(code)
  }
}

/* -------------------------------
   이미지
-------------------------------- */
const imageFile = ref(null)

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    campaign.value.product_image_url = URL.createObjectURL(file)
  }
}

/* -------------------------------
   캠페인 생성
-------------------------------- */
async function createCampaign() {
  const isConfirmed = await warningStore.confirm("작성하신 내용으로 캠페인을 생성하시겠습니까?")
  if (!isConfirmed) return

  try {
    const styleTagIds = allTags
      .filter(tag => campaign.value.style_tags.includes(tag.code))
      .map(tag => tag.id)

    await campaignStore.createCampaign(brandId, {
      ...campaign.value,
      requested_at: new Date().toISOString(),
      application_deadline_at: campaign.value.posting_start_at,
      style_tag_ids: styleTagIds,
    })

    // [수정] 성공 알림 모달 호출
    warningStore.open("캠페인이 성공적으로 생성되었습니다.") 

    router.push({
      name: "brand-campaign-list",
      params: { brand_id: brandId },
    })
  } catch (err) {
    // [수정] 에러 알림 모달 호출
    warningStore.open("캠페인 생성에 실패했습니다. 다시 시도해 주세요.") 
  }
}
</script>

<style scoped>
/* Update Campaign 스타일 재사용 */
.update-wrapper {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px 100px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 56px;
  text-align: center;
}

.section {
  margin-bottom: 56px;
}

.section h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.input-group label {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

input,
select,
textarea {
  padding: 12px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
}

textarea {
  min-height: 140px;
}

.style-tags label {
  font-size: 14px;
  font-weight: 500;
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
  cursor: pointer;
}

.tag.active {
  background: #7e6b5a;
  color: #fff;
  border-color: #7e6b5a;
}

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
  border: none;
  cursor: pointer;
}
</style>
