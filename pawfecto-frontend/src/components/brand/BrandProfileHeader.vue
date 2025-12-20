<template>
    <div class="brand-header">

        <!-- Hero 영역 -->
        <section class="brand-hero">
          <div class="brand-hero-overlay"></div>

          <!-- 프로필 이미지 -->
          <div class="profile-image-wrap">
            <img
              class="profile-img"
              :src="fullProfileImageUrl"
              alt="profile image"
              @click="goDashboard"
            />
          </div>

        </section>


        <!-- 텍스트 -->
        <div class="text-wrap">
            <h2 class="brand-name">{{ brand.name }}</h2>
            <p class="brand-role">Brand</p>
            <!-- <p class="brand-desc">{{ brand.bio || '소개 문구가 없습니다.' }}</p> -->
        </div>

    </div>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
import defaultProfileImage from "@/assets/defalut-profile-image.jpg"

// props
const props = defineProps({
  brand: {
    type: Object,
    required: true
  }
})

// router
const router = useRouter()
const goDashboard = () => {
  router.push(`/dashboard/brand/${props.brand.id}`)
}

// backend base url (env 기준)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"

// profile image url
const fullProfileImageUrl = computed(() => {
  const url = props.brand.profile_image_url

  if (!url) {
    return defaultProfileImage
  }

  // absolute url
  if (url.startsWith("http")) {
    return url
  }

  // relative media url
  return `${API_BASE_URL}${url}`
})
</script>


<style scoped>
.brand-header {
  position: relative;
  text-align: center;
  margin-bottom: 60px; /* 이미지가 걸쳐 보이도록 여백 */
}

/* ----------------- Hero 영역 ----------------- */
/* Hero 영역 */
.brand-hero {
  position: relative;
  width: 100%;
  height: 45vh;
  background-image: url('@/assets/dashboard-hero.jpg');
  background-size: cover;
  background-position: center;
}

.brand-hero-overlay {
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

.brand-name {
  font-size: 22px;
  font-weight: 700;
}

</style>
