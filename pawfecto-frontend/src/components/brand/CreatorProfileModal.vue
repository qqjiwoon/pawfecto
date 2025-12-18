<template>
  <div class="modal-overlay" @click.self="close">
    
    <div class="modal-container" v-if="creator">
      
      <button class="close-x" @click="close">&times;</button>

      <div class="profile-header">
        <img :src="creator.profileImg" class="profile-circle-img" alt="profile" />
        <div class="title-text">
          <h2 class="name">{{ creator.name }}</h2>
          <p class="handle">@{{ creator.handle }}</p>
        </div>
      </div>

      <div class="details-section">
        <div class="info-row">
          <span class="label">반려동물 종류</span>
          <div class="pet-tags">
            <span class="pet-badge" :class="creator.petType?.toLowerCase()">
              {{ creator.petType === 'dog' ? '강아지' : '고양이' }}
            </span>
          </div>
        </div>

        <div class="info-row">
          <span class="label">팔로워 수</span>
          <span class="value">{{ creator.followers?.toLocaleString() }} 명</span>
        </div>

        <div class="info-row">
          <span class="label">활동 스타일</span>
          <div class="tag-group">
            <span v-for="tag in creator.styleTags" :key="tag" class="style-tag">
              # {{ tag }}
            </span>
          </div>
        </div>

        <div class="info-row" v-if="creator.address">
          <span class="label">활동 지역</span>
          <span class="value">{{ creator.address }}</span>
        </div>
      </div>

      <div class="footer-action">
        <a 
          :href="'https://instagram.com/' + creator.handle" 
          target="_blank" 
          class="sns-btn"
        >
          인스타그램 방문하기
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  creator: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<style scoped>
/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

/* 모달 컨테이너 */
.modal-container {
  background: #fff;
  border-radius: 24px;
  padding: 32px;
  width: 450px; /* 1단 레이아웃에 적합한 너비 */
  max-width: 90%;
  position: relative; /* X 버튼 배치를 위해 */
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 우측 상단 X 버튼 */
.close-x {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  line-height: 1;
}

.close-x:hover {
  color: #333;
}

/* 상단 헤더: 원형 이미지 + 이름 */
.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.profile-circle-img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f5f1ec;
}

.name {
  font-size: 22px;
  font-weight: 700;
  color: #222;
  margin: 0;
}

.handle {
  font-size: 14px;
  color: #6495ff;
  margin: 2px 0 0;
}

/* 상세 정보 섹션 */
.details-section {
  background: #fcfaf8;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 32px;
}

.info-row {
  display: flex;
  margin-bottom: 16px;
  align-items: center;
}

.info-row:last-child {
  margin-bottom: 0;
}

.label {
  width: 100px;
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

.value {
  font-size: 14px;
  color: #333;
}

/* 반려동물 배지 */
.pet-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  background: #fff;
  color: #5D4B3E;
  border: 1px solid #e0d6cc;
}

/* 스타일 태그 */
.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.style-tag {
  background-color: #fff;
  color: #5D4B3E;
  padding: 4px 10px;
  font-size: 12px;
  border-radius: 6px;
  border: 1px solid #e0d6cc;
}

/* 푸터 액션: 버튼 가운데 정렬 */
.footer-action {
  display: flex;
  justify-content: center;
}

.sns-btn {
  width: 100%;
  max-width: 240px;
  text-align: center;
  padding: 12px;
  background: #C4B199;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 400;
  font-size: 15px;
  transition: all 0.2s;
}

.sns-btn:hover {
  background: #b3a088;
  transform: translateY(-2px);
}
</style>
