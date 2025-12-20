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
            :key="tag.code"
            class="tag"
            :class="{ active: campaign.style_tags.includes(tag.code) }"
            @click="toggleStyle(tag.code)"
            type="button"
          >
            #{{ getStyleLabel(tag.name) }}
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
import api from "@/plugins/axios"
import { useWarningStore } from '@/stores/warning'

const route = useRoute()
const router = useRouter()
const warningStore = useWarningStore()

const campaignId = Number(route.params.campaign_id)
const brandId = Number(route.params.brand_id)

// 수정용 캠페인
const campaign = ref(null)


// 스타일 태그 (DB styletag 기준, 한국어 표시용)
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


// code → 한국어 매핑
const styleLabelMap = ref({})

onMounted(async () => {
  try {
    const res = await api.get(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/`
    )

    // 기존 로직 유지
    campaign.value = {
      ...res.data,
      style_tags: Array.isArray(res.data.style_tags)
        ? res.data.style_tags.map(t => t.code ?? t)
        : [],
    }

    // 🔹 한국어 라벨만 따로 추출 (최소 추가)
    if (Array.isArray(res.data.style_tags)) {
      res.data.style_tags.forEach(t => {
        if (t?.code && t?.name) {
          const m = t.name.match(/\(([^)]+)\)/)
          styleLabelMap.value[t.code] = m ? m[1] : t.name
        }
      })
    }

  } catch (err) {
    warningStore.open("캠페인 정보를 불러오지 못했습니다.")
  }
})

// 스타일 태그 토글 (기존 유지)
function toggleStyle(tag) {
  if (campaign.value.style_tags.includes(tag)) {
    campaign.value.style_tags =
      campaign.value.style_tags.filter(t => t !== tag)
  } else {
    campaign.value.style_tags.push(tag)
  }
}

// 표시용
function getStyleLabel(code) {
  return styleLabelMap.value[code] || code
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

// 업데이트 (기존 유지)
async function updateCampaign() {
  try {
    const styleTagIds = allTags
      .filter(tag => campaign.value.style_tags.includes(tag.code))
      .map(tag => tag.id)

    // 🔥 핵심: FormData 사용
    const formData = new FormData()

    formData.append("product_name", campaign.value.product_name)
    formData.append("product_description", campaign.value.product_description)

    formData.append("target_pet_type", campaign.value.target_pet_type)
    formData.append("min_follower_count", campaign.value.min_follower_count)
    formData.append("required_creator_count", campaign.value.required_creator_count)

    formData.append("application_deadline_at", campaign.value.application_deadline_at)
    formData.append("posting_start_at", campaign.value.posting_start_at)
    formData.append("posting_end_at", campaign.value.posting_end_at)

    // 스타일 태그 (M2M)
    styleTagIds.forEach(id => {
      formData.append("style_tag_ids", id)
    })

    // 🔥 이미지: 파일이 선택된 경우에만
    if (imageFile.value) {
      formData.append("product_image_url", imageFile.value)
    }

    await api.put(
      `/api/v1/brand/${brandId}/campaign/${campaignId}/update/`,
      formData
    )

    warningStore.open("캠페인이 성공적으로 수정되었습니다.")

    router.push({
      name: "brand-campaign-detail",
      params: { brand_id: brandId, campaign_id: campaignId },
    })
  } catch (err) {
    const errorMsg = err.response?.data?.error || "캠페인 수정에 실패했습니다."
    warningStore.open(errorMsg)
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
  font-size: 14px;
  font-weight: 500;
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
  color: #333;
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
  font-size: 14px;
  font-weight: 500;
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
