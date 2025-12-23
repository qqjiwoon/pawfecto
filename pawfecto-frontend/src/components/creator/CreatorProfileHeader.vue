<template>
    <div class="creator-header">

        <section class="creator-hero">
          <div class="creator-hero-overlay"></div>

          <div class="profile-image-wrap">
            <img
              class="profile-img"
              :src="creator.profile_image_url || defaultProfileImage"
              alt="profile image"
              @click="goDashboard"
            />
          </div>

        </section>


        <div class="text-wrap">
            <h2 class="creator-name">{{ creator.name }}</h2>
            <p class="creator-role">Creator</p>
            <button
              v-if="!creator.instagram_id"
              class="instagram-connect-btn"
              @click="connectInstagram"
            >
              <img src="@/assets/instagram-icon.png" alt="instagram" />
              <span>Instagram 계정 연동</span>
            </button>
            <p
              v-else
              class="instagram-connected"
            >
              <i class="check-icon">✓</i> Instagram 연동 완료
            </p>
        </div>

    </div>


    <div class="creator-stats">
      <div class="stat-item">
        <p class="number">{{ Number(creator.total_post_count).toLocaleString() }}</p>
        <span>Posts</span>
      </div>

      <div class="divider"></div>

      <div class="stat-item">
        <p class="number">{{ Number(creator.follower_count).toLocaleString() }}</p>
        <span>Followers</span>
      </div>

      <div class="divider"></div>

      <div class="stat-item">
        <p class="number">{{ Number(creator.following_count).toLocaleString() || 0 }}</p>
        <span>Following</span>
      </div>
    </div>

</template>

<script setup>
import { useRouter } from 'vue-router'
import defaultProfileImage from '@/assets/defalut-profile-image.jpg'

const props = defineProps({
  creator: {
    type: Object,
    required: true
  }
})

// 프로필 이미지 클릭 시 대시보드 메인페이지로 이동
const router = useRouter()
const goDashboard = () => {
  router.push(`/dashboard/creator/${props.creator.id}`)
}


// Instagram 연동 버튼 클릭 
const connectInstagram = () => {
  const clientId = import.meta.env.VITE_INSTAGRAM_CLIENT_ID  // Instagram 개발자 대시보드에서 제공된 클라이언트 ID
  const redirectUri = 'https://localhost:5173/callback/instagram'  // 리디렉션 URI
    const scope = [
      'instagram_business_basic',
      'instagram_business_manage_messages',
      'instagram_business_manage_comments',
      'instagram_business_content_publish',
      'instagram_business_manage_insights'
    ].join(',')
    
  const responseType = 'code'  // 인증 코드 받기

  // Instagram OAuth 인증 URL 생성
  const loginUrl =
    `https://www.instagram.com/oauth/authorize` +
    `?client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&response_type=${responseType}` +
    `&scope=${encodeURIComponent(scope)}`
    // `&force_reauth=true` 

  // Instagram 로그인 페이지로 리디렉션
  window.location.href = loginUrl
}

</script>

<style scoped>
.creator-header {
  position: relative;
  text-align: center;
  margin-bottom: 60px;
}

/* ----------------- Hero 영역 ----------------- */
.creator-hero {
  position: relative;
  width: 100%;
  height: 45vh;
  background-image: url('@/assets/dashboard-hero.jpg');
  background-size: cover;
  background-position: center;
}

.creator-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
}

.profile-image-wrap {
  position: absolute;
  bottom: -70px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  width: clamp(90px, 18vw, 160px);
  height: clamp(90px, 18vw, 160px);
  border-radius: 50%;
  overflow: hidden;
  border: 5px solid #5D4B3E;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.text-wrap {
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.creator-name {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 4px;
}

.creator-role {
  color: #888;
  margin-bottom: 16px;
}

/* ----------------- 인스타그램 버튼 디자인 수정 ----------------- */
.instagram-connect-btn {
  margin-top: 16px;
  width: fit-content;
  min-width: 180px;
  background-color: #ffffff;
  border: 1px solid #dbdbdb; /* 인스타그램 기본 테두리 컬러 */
  padding: 10px 20px;
  border-radius: 4px; /* 살짝 각진 형태가 더 심플함 */
  font-size: 14px;
  font-weight: 600;
  color: #262626;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.instagram-connect-btn:hover {
  background-color: #fafafa;
  border-color: #aeaeae;
}

.instagram-connect-btn:active {
  transform: translateY(0);
}

.instagram-connect-btn img {
  width: 18px;
  height: 18px;
  opacity: 0.8; /* 아이콘이 너무 튀지 않게 조절 */
}

/* 연동 완료 텍스트 스타일 */
.instagram-connected {
  margin-top: 16px;
  font-size: 14px;
  color: #8e8e8e; /* 차분한 그레이 */
  font-weight: 500;
}

/* ----------------- 통계 영역 ----------------- */
.creator-stats {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  max-width: 500px;
  margin: 28px auto 0 auto;
  column-gap: 40px;
}

.stat-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-item .number {
  font-size: 26px;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.stat-item span {
  font-size: 14px;
  color: #777;
  margin-bottom: 10px;
}

.divider {
  width: 1px;
  height: 24px;
  background-color: #ccc;
}
</style>
