<template>
  <!-- 모달 오버레이 -->
  <div class="modal-overlay" @click.self="close">

    <!-- 모달 컨테이너 -->
    <div class="modal-container" v-if="campaign">

      <!-- 캠페인 상세 영역 -->
      <div class="campaign-info">

        <!-- 상품 이미지 -->
        <img
          :src="campaign.product_image_url"
          class="product-img"
        />

        <!-- 우측 콘텐츠 -->
        <div class="content-box">

          <!-- 상품명 -->
          <h2>{{ campaign.product_name }}</h2>

          <!-- 상품 설명 -->
          <p class="desc" v-html="campaign.product_description"></p>

          <!-- 크리에이터 조건 -->
          <div class="pref">
            <h3>Creator Preferences</h3>

            <!-- 대상 동물 -->
            <div class="row">
              <span class="label">캠페인 대상 동물 종류</span>
              <div class="pet-type">
                <button
                  class="pet-btn"
                  :class="{ active: campaign.target_pet_type === 'cat' }"
                >
                  Cat
                </button>
                <button
                  class="pet-btn"
                  :class="{ active: campaign.target_pet_type === 'dog' }"
                >
                  Dog
                </button>
              </div>
            </div>

            <!-- 최소 팔로워 수 -->
            <div class="row">
              <span class="label">최소 팔로워 수</span>
              <span class="value">
                {{ campaign.min_follower_count.toLocaleString() }}
              </span>
            </div>

            <!-- 필요 크리에이터 수 -->
            <div class="row">
              <span class="label">필요 크리에이터 수</span>
              <span class="value">
                {{ campaign.required_creator_count }}
              </span>
            </div>

            <!-- 스타일 -->
            <div class="row">
              <span class="label">스타일</span>
              <div class="style-tags">
                <span
                  v-for="tag in parsedStyles"
                  :key="tag"
                  class="style-tag"
                >
                  # {{ tag.code }}
                </span>
              </div>
            </div>
          </div>

          <!-- 닫기 버튼 -->
          <button class="close-btn" @click="close">
            닫기
          </button>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

/* Props */
const props = defineProps({
  campaign: {
    type: Object,
    required: true
  }
})

/* Emits */
const emit = defineEmits(['close'])

/* 스타일 태그 파싱 */
const parsedStyles = computed(() => {
  const styles = props.campaign?.style_tags

  if (!styles) return []

  if (typeof styles === 'string') {
    return styles.split(',')
  }

  if (Array.isArray(styles)) {
    return styles
  }

  return []
})

/* 닫기 */
const close = () => {
  emit('close')
}
</script>

<style scoped>
/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* 모달 컨테이너 */
.modal-container {
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  max-width: 1000px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
}

/* 캠페인 레이아웃 */
.campaign-info {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 60px;
  position: relative;
}

/* 상품 이미지 */
.product-img {
  width: 420px;
  height: 520px;
  object-fit: cover;
  border-radius: 12px;
}

/* 우측 콘텐츠 */
.content-box {
  width: 500px;
}

/* 설명 */
.desc {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 45px;
}

/* 조건 행 */
.pref .row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.label {
  width: 250px;
  /* font-weight: 600; */
}

.value {
  font-size: 15px;
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

/* 닫기 버튼 */
.close-btn {
  position: absolute;
  bottom: 0;
  right: 0;

  width: 500px;   /* content-box와 동일한 폭 */
  padding: 14px;
  background: #695845;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
}

</style>
