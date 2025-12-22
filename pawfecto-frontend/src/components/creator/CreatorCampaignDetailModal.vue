<template>
  <div class="modal-overlay" @click.self="close">

    <div class="modal-container" v-if="campaign">

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
            <button class="close-btn" @click="close">닫기</button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  campaign: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

/* 백엔드 베이스 URL */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"

/* 이미지 URL 처리 로직 (브랜드와 동일) */
const campaignImageUrl = computed(() => {
  const url = props.campaign?.product_image_url
  if (!url) return ""
  return url.startsWith("http") ? url : `${API_BASE_URL}${url}`
})

/* 스타일 태그 파싱 로직 (브랜드와 동일하게 정규식 적용) */
const parsedStyles = computed(() => {
  const tags = props.campaign?.style_tags
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

const close = () => {
  emit('close')
}
</script>

<style scoped>
/* 모달 레이아웃 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-container {
  background: #fff;
  border-radius: 20px;
  padding: 60px;
  max-width: 1100px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

/* 캠페인 정보 레이아웃 (브랜드 상세 페이지 스타일 적용) */
.campaign-info {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 80px;
}

.product-img {
  width: 400px;
  height: 500px;
  object-fit: cover;
  border-radius: 12px;
  flex-shrink: 0;
}

.content-box {
  flex: 1;
  max-width: 500px;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #333;
}

.desc {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 40px;
}

/* Creator Preferences 스타일 */
.pref h3 {
  font-size: 18px;
  margin-bottom: 24px;
  color: #333;
}

.pref .row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.row.items-start {
  align-items: flex-start;
}

.label {
  width: 160px;
  font-size: 14px;
  color: #888;
}

.value {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.value.date {
  color: #555;
}

/* 펫 타입 버튼 */
.pet-btn {
  border: 1px solid #ddd;
  background: #fff;
  padding: 6px 18px;
  border-radius: 6px;
  cursor: default;
  margin-right: 8px;
  color: #777;
  font-size: 14px;
}

.pet-btn.active {
  background: #C4B199;
  border-color: #C4B199;
  color: white;
}

/* 스타일 태그 */
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

/* AI 검증 조건 (Brand 버전 이식) */
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

/* 닫기 버튼 그룹 */
.button-group {
  margin-top: 40px;
}

.close-btn {
  width: 100%;
  padding: 14px;
  background: #695845;
  color: white;
  border: 1px solid #695845;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #564839;
}

/* 스크롤바 커스텀 */
.modal-container::-webkit-scrollbar {
  width: 8px;
}
.modal-container::-webkit-scrollbar-thumb {
  background: #eee;
  border-radius: 4px;
}
</style>
