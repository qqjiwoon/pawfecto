<template>
    <div class="creator-header">

        <!-- Hero 영역 -->
        <section class="creator-hero">
          <div class="creator-hero-overlay"></div>

          <!-- 프로필 이미지 -->
          <div class="profile-image-wrap">
            <img
              class="profile-img"
              :src="creator.profile_image_url || defaultProfileImage"
              alt="profile image"
              @click="goDashboard"
            />
          </div>

        </section>


        <!-- 텍스트 -->
        <div class="text-wrap">
            <h2 class="creator-name">{{ creator.name }}</h2>
            <p class="creator-role">Creator</p>
            <!-- <p class="creator-desc">{{ creator.bio || '소개 문구가 없습니다.' }}</p> -->

            <!-- Instagram 연동 버튼 -->
            <button
              v-if="!creator.instagram_id"
              class="instagram-connect-btn"
              @click="connectInstagram"
            >
              <img src="@/assets/instagram-icon.png" alt="instagram" />
              Instagram 계정 연동
            </button>
            <p
              v-else
              class="instagram-connected"
            >
              Instagram 연동 완료
            </p>
        </div>

    </div>


    <!-- 인스타그램 통계 -->
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
    `&scope=${encodeURIComponent(scope)}` +
    `&force_reauth=true` 

  // Instagram 로그인 페이지로 리디렉션
  window.location.href = loginUrl
}

</script>

<style scoped>
.creator-header {
  position: relative;
  text-align: center;
  margin-bottom: 60px; /* 이미지가 걸쳐 보이도록 여백 */
}

/* ----------------- Hero 영역 ----------------- */
/* Hero 영역 */
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
  background-color: rgba(255, 255, 255, 0.25); /* 검은색에서 흰색으로 변경 */
}

/* Hero 하단에 정확히 걸쳐지는 프로필 이미지 */
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
  margin-top: 80px; /* 140px에서 감소 - 프로필 이미지 크기에 맞춰 조정 */
}

.creator-name {
  font-size: 22px;
  font-weight: 700;
}


/* 인스타그램 통계 영역 */
.creator-stats {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr; /* stat-div-stat-div-stat */
  align-items: center;

  max-width: 500px;  /* 화면 크기와 상관없이 고정 폭 */
  margin: 28px auto 0 auto; /* 가운데 정렬 */
  column-gap: 40px; /* stat-item 간 일정 간격 유지 */
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


/* 세로 구분선 */
.divider {
  width: 1px;
  height: 100%;   /* grid에서 stat-item 높이에 자동 맞춤 */
  background-color: #ccc;
}

.instagram-connect-btn {
  margin-top: 12px;
  width: 30%;
  box-sizing: border-box;
  background-color: #ffffff;
  border: 1px solid #ddd;
  padding: 14px;
  border-radius: 8px;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  cursor: pointer;
  /* [추가] 부드러운 호버 효과를 위한 트랜지션 */
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* [추가] 인스타그램 버튼 호버 효과 */
.instagram-connect-btn:hover {
  background-color: #f9f9f9; /* 아주 연한 회색 배경 */
  border-color: #ccc; /* 약간 진한 테두리 */
}


.instagram-connect-btn img {
  width: 20px;
  height: 20px;
}


</style>