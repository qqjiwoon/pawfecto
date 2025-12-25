<template>
  <div class="update-wrapper">
    <h1 class="page-title">Create Campaign</h1>

    <section class="section">
      <h2>Product</h2>

      <div class="input-group">
        <label>상품명</label>
        <input v-model="campaign.product_name" type="text" placeholder="상품명을 입력하세요" />
      </div>

      <div class="input-group">
        <label>상품 이미지</label>
        <div class="image-upload-box" @click="triggerFileInput">
          <img v-if="campaign.product_image_url" :src="campaign.product_image_url" class="preview-img" alt="Preview" />
          <div v-else class="upload-placeholder">
            <span class="icon">+</span>
            <p>이미지 업로드</p>
          </div>
          <input ref="fileInputRef" type="file" accept="image/*" class="hidden-input" @change="onFileChange" />
        </div>
      </div>

      <div class="input-group">
        <label>상품 상세</label>
        <textarea v-model="campaign.product_description" placeholder="상품에 대한 설명을 입력하세요"></textarea>
      </div>
    </section>

    <section class="section">
      <h2>Guideline details</h2>

      <div class="row-group">
        <div class="input-group half">
          <label>캠페인 대상 동물 종류</label>
          <select v-model="campaign.target_pet_type">
            <option value="dog">Dog</option>
            <option value="cat">Cat</option>
          </select>
        </div>

        <div class="input-group half">
          <label>최소 팔로워 수</label>
          <input v-model="campaign.min_follower_count" type="number" placeholder="0" />
        </div>
      </div>

      <div class="input-group">
        <label>필요한 크리에이터 수</label>
        <input v-model="campaign.required_creator_count" type="number" placeholder="1" />
      </div>

      <div class="input-group style-section">
        <label>Style Tags</label>
        <div class="tag-container">
          <button
            v-for="tag in allTags"
            :key="tag.code"
            class="tag-btn"
            :class="{ active: campaign.style_tags.includes(tag.code) }"
            @click="toggleStyle(tag.code)"
            type="button"
          >
            # {{ tag.name }}
          </button>
        </div>
      </div>

      <div class="input-group requirement-section">
        <label>AI 검증 조건</label>
        <div class="req-container">
          <div v-for="(requirement, index) in campaign.requirements" :key="index" class="req-row">
            
            <select v-model="requirement.requirement_type" class="req-select">
              <option value="object">사물</option>
              <option value="scene">배경/장소</option>
              <option value="action">행동</option>
              <option value="text">텍스트</option>
            </select>

            <input 
              v-model="requirement.description" 
              type="text" 
              class="req-input" 
              :placeholder="getPlaceholder(requirement.requirement_type)"
            />

            <div class="req-actions">
              <label class="checkbox-label">
                <input type="checkbox" v-model="requirement.is_required" /> 필수
              </label>
              <button type="button" class="btn-remove" @click="removeRequirement(index)">
                삭제
              </button>
            </div>
            
          </div>
        </div>
        
        <button type="button" class="btn-add-outline" @click="addRequirement">
          + 조건 추가
        </button>
      </div>
    </section>

    <section class="section">
      <h2>Campaign Duration</h2>

      <div class="input-group">
        <label>지원 마감일 (Application Deadline)</label>
        <input v-model="campaign.application_deadline_at" type="date" />
      </div>

      <div class="row-group">
        <div class="input-group half">
          <label>게시 시작일</label>
          <input v-model="campaign.posting_start_at" type="date" />
        </div>

        <div class="input-group half">
          <label>게시 마감일</label>
          <input v-model="campaign.posting_end_at" type="date" />
        </div>
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
const fileInputRef = ref(null)

/* -------------------------------
   캠페인 상태
-------------------------------- */
const campaign = ref({
  product_name: "",
  product_description: "",
  product_image_url: "",
  
  target_pet_type: "dog",
  min_follower_count: 0,
  required_creator_count: 1,

  requirements: [{ requirement_type: "object", description: "", is_required: true }],

  application_deadline_at: "",
  posting_start_at: "",
  posting_end_at: "",

  style_tags: [],
})

/* -------------------------------
   스타일 태그 데이터
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
    campaign.value.style_tags = campaign.value.style_tags.filter(t => t !== code)
  } else {
    campaign.value.style_tags.push(code)
  }
}

/* -------------------------------
   요구조건(requirement)
-------------------------------- */
function addRequirement() {
  campaign.value.requirements.push({ requirement_type: "object", description: "", is_required: true });
}

function removeRequirement(index) {
  // 최소 1개는 유지하고 싶다면 조건 추가 가능
  campaign.value.requirements.splice(index, 1);
}

/* -------------------------------
   플레이스홀더 동적 반환 함수
-------------------------------- */
function getPlaceholder(type) {
  switch (type) {
    case 'object':
      return "예: 화면에 노출될 제품 패키지"
    case 'scene':
      return "예: 촬영 배경이 되는 실내" // 또는 "예: 공원 잔디밭 같은 야외"
    case 'action':
      return "예: 강아지가 신나게 뛰는 장면"
    case 'text':
      return "예: 필수 포함 텍스트 '제일 좋아하는 장난감'"
    default:
      return "조건을 입력해주세요"
  }
}

/* -------------------------------
   이미지 처리
-------------------------------- */
const imageFile = ref(null)

function triggerFileInput() {
  fileInputRef.value.click()
}

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
  const isConfirmed = await warningStore.confirm(
    "작성하신 내용으로 캠페인을 생성하시겠습니까?"
  )
  if (!isConfirmed) return

  try {
    const styleTagIds = allTags
      .filter(tag => campaign.value.style_tags.includes(tag.code))
      .map(tag => tag.id)

    const formData = new FormData()

    formData.append("product_name", campaign.value.product_name)
    formData.append("product_description", campaign.value.product_description)
    formData.append("target_pet_type", campaign.value.target_pet_type)
    formData.append("min_follower_count", campaign.value.min_follower_count)
    formData.append("required_creator_count", campaign.value.required_creator_count)
    
    // 날짜 필드들
    formData.append("application_deadline_at", campaign.value.application_deadline_at)
    formData.append("posting_start_at", campaign.value.posting_start_at)
    formData.append("posting_end_at", campaign.value.posting_end_at)
    formData.append("requested_at", new Date().toISOString())

    // 요구조건
    formData.append("requirements_data", JSON.stringify(campaign.value.requirements));

    // 스타일 태그
    styleTagIds.forEach(id => {
      formData.append("style_tag_ids", id)
    })

    // 이미지
    if (imageFile.value) {
      formData.append("product_image_url", imageFile.value)
    }

    await campaignStore.createCampaign(brandId, formData)

    warningStore.open("캠페인이 성공적으로 생성되었습니다.")

    router.push({
      name: "brand-campaign-list",
      params: { brand_id: brandId },
    })
  } catch (err) {
    warningStore.open("캠페인이 생성에 실패하였습니다.")
  }
}
</script>

<style scoped>
/* 기존 폰트 사이즈 유지 
  Title: 28px / H2: 18px / Label, Input: 14px
*/

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
  color: #333;
}

.section {
  margin-bottom: 56px;
}

.section h2 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 24px;
}

.input-group label {
  font-size: 16px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

/* 2열 배치 유틸리티 */
.row-group {
  display: flex;
  gap: 16px;
}
.input-group.half {
  flex: 1;
}

/* 기본 Input 스타일 (기존 사이즈 유지하되 깔끔하게) */
input[type="text"],
input[type="number"],
input[type="date"],
select,
textarea {
  padding: 12px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #7e6b5a;
}

textarea {
  min-height: 140px;
  resize: vertical;
}

/* 이미지 업로드 박스 (커스텀) */
.image-upload-box {
  width: 100%;
  height: 200px;
  border: 1px dashed #ccc;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background: #fafafa;
  overflow: hidden;
  position: relative;
}
.image-upload-box:hover {
  background: #f5f5f5;
  border-color: #aaa;
}
.upload-placeholder {
  text-align: center;
  color: #999;
  font-size: 14px;
}
.upload-placeholder .icon {
  display: block;
  font-size: 24px;
  margin-bottom: 5px;
}
.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hidden-input {
  display: none;
}

/* 스타일 태그 컨테이너 */
.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-btn {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid #ddd;
  background: #fff;
  font-size: 14px; /* 기존 폰트 사이즈 */
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}
.tag-btn.active {
  background: #7e6b5a;
  color: #fff;
  border-color: #7e6b5a;
}

/* AI 검증 조건 (통일된 리스트 스타일) */
.req-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.req-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff;
}

.req-select {
  flex: 0 0 100px; /* 너비 고정 */
}

.req-input {
  flex: 1; /* 나머지 공간 차지 */
}

.req-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
  margin-bottom: 0 !important; /* input-group label 마진 상쇄 */
}

.btn-remove {
  background: none;
  border: 1px solid #eee;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  color: #999;
  cursor: pointer;
}
.btn-remove:hover {
  background: #f5f5f5;
  color: #ff4d4f;
}

/* 조건 추가 버튼 (Outline 스타일) */
.btn-add-outline {
  width: 100%;
  padding: 12px;
  border: 1px dashed #ccc;
  border-radius: 10px;
  background: #fff;
  color: #7e6b5a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s;
}
.btn-add-outline:hover {
  background: #fafafa;
  border-color: #7e6b5a;
}

/* 하단 저장 버튼 */
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

/* 모바일 대응 */
@media (max-width: 600px) {
  .row-group {
    flex-direction: column;
    gap: 0;
  }
  .req-row {
    flex-direction: column;
    align-items: stretch;
    background: #f9f9f9;
    padding: 12px;
    border-radius: 10px;
  }
  .req-actions {
    justify-content: space-between;
  }
}
</style>
