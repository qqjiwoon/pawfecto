<template>
    <div class="creator-header">

        <!-- Hero 영역 -->
        <section class="creator-hero">
          <div class="creator-hero-overlay"></div>

          <!-- 프로필 이미지 -->
          <div class="profile-image-wrap">
            <img
              class="profile-img"
              :src="creator.profile_image_url"
              alt="creator profile"
              @click="goDashboard"
            />
          </div>

        </section>


        <!-- 텍스트 -->
        <div class="text-wrap">
            <h2 class="creator-name">{{ creator.name }}</h2>
            <p class="creator-role">Creator</p>
            <!-- <p class="creator-desc">{{ creator.bio || '소개 문구가 없습니다.' }}</p> -->
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
  bottom: -70px;       /* 걸쳐 보이도록 음수 */
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
}

.profile-img {
  width: clamp(90px, 18vw, 160px);
  height: clamp(90px, 18vw, 160px);
  border-radius: 50%;
  object-fit: cover;
  border: 5px solid #5D4B3E;
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

</style>