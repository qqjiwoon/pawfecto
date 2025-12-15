<template>
  <div class="create-campaign-page">

    <h1 class="title">Create Campaign</h1>

    <!-- Product Section -->
    <div class="section">
      <h2 class="section-title">Product</h2>

      <div class="field">
        <label>상품명</label>
        <input v-model="productName" type="text" placeholder="상품 이름을 입력해주세요." />
      </div>

      <div class="field">
        <label>사진</label>
        <input type="file" @change="onImageSelect" />
      </div>

      <div class="field">
        <label>상품 설명</label>
        <textarea v-model="productDescription" placeholder="상품 설명을 입력해주세요."></textarea>
      </div>
    </div>

    <!-- Guideline Section -->
    <div class="section">
      <h2 class="section-title">Guideline details</h2>

      <div class="field">
        <label>캠페인 대상 동물 종류</label>
        <select v-model="petType">
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
        </select>
      </div>

      <div class="field">
        <label>최소 팔로워 수 조건</label>
        <input v-model.number="minFollower" type="number" placeholder="최소 팔로워 수" />
      </div>

      <div class="field">
        <label>필요한 크리에이터 수</label>
        <input v-model.number="requiredCreators" type="number" placeholder="숫자를 입력해주세요." />
      </div>

      <div class="field">
        <label>스타일</label>
        <div class="tag-container">
          <div
            v-for="tag in styleTags"
            :key="tag"
            class="tag"
            :class="{ active: selectedTags.includes(tag) }"
            @click="toggleTag(tag)"
          >
            #{{ tag }}
          </div>
        </div>
      </div>
    </div>

    <!-- Duration Section -->
    <div class="section">
      <h2 class="section-title">Campaign Duration</h2>

      <div class="field">
        <label>캠페인 시작일</label>
        <input v-model="startDate" type="date" />
      </div>

      <div class="field">
        <label>캠페인 마감일</label>
        <input v-model="endDate" type="date" />
      </div>
    </div>

    <button class="save-btn" @click="saveCampaign">SAVE</button>
  </div>
</template>


<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { campaigns } from "@/stores/campaign"

// ========== 1) 라우터에서 brand_id 가져오기 ==========
const route = useRoute()
const router = useRouter()
const brandId = Number(route.params.brand_id)


// ========== 2) 입력 상태 관리 ==========
const productName = ref("")
const productDescription = ref("")
const petType = ref("dog")
const minFollower = ref(0)
const requiredCreators = ref(1)
const startDate = ref("")
const endDate = ref("")

// 이미지 파일
const imageFile = ref(null)
const imageUrl = ref(null)

function onImageSelect(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imageUrl.value = URL.createObjectURL(file)
  }
}

// ========== 3) 스타일 태그 ==========
const styleTags = [
  'outdoor','energetic','no_preference','minimal',
  'aesthetic','heartfelt','cozy','wholesome','funny','calm'
]

const selectedTags = ref([])

function toggleTag(tag) {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter(t => t !== tag)
  } else {
    selectedTags.value.push(tag)
  }
}


// ========== 4) SAVE → store에 push ==========
function saveCampaign() {
  // 새로운 campaign_id 생성
  const newId = campaigns.value.length
    ? Math.max(...campaigns.value.map(c => c.campaign_id)) + 1
    : 1

  const newCampaign = {
    campaign_id: newId,
    brand_id: brandId,
    product_name: productName.value,
    product_image_url: imageUrl.value || "/assets/default.jpg",
    product_description: productDescription.value,
    pet_type: petType.value,
    min_follower_count: minFollower.value,
    required_creator_count: requiredCreators.value,
    posting_start_at: startDate.value,
    posting_end_at: endDate.value,
    style_tags: [...selectedTags.value], 
    requested_at: new Date().toISOString(),
    application_deadline_at: endDate.value
  }

  campaigns.value.push(newCampaign)

  alert("캠페인이 생성되었습니다!")

  router.push({
    name: "brand-dashboard",
    params: { brand_id: brandId }
  })
}
</script>

<style scoped>
.create-campaign-page {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
}

.title {
  font-size: 32px;
  font-weight: Bold;
  margin-bottom: 40px;
  text-align: center;
}

.section {
  margin-bottom: 50px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.field label {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 8px;
}

.field input,
.field textarea,
.field select {
  border: 1px solid #ccc;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  background: #fff;
}

textarea {
  height: 120px;
  resize: none;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 8px 14px;
  border-radius: 20px;
  background: #f3f3f3;
  cursor: pointer;
  border: 1px solid transparent;
  user-select: none;
  transition: 0.2s;
}

.tag.active {
  background: #493629;
  color: white;
  border-color: #493629;
}

.save-btn {
  width: 100%;
  padding: 16px;
  font-size: 18px;
  background: #493629;
  color: white;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  margin-top: 20px;
}

.save-btn:hover {
  background: #2c2019;
}
</style>
