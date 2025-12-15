<template>
  <div class="pf-home">

    <!-- Hero 영역 -->
    <div class="pf-home-hero">
      <img src="@/assets/home-hero.png" alt="hero image" class="pf-home-hero-img" />
      <div class="pf-home-hero-overlay"></div>
    </div>

  </div>
</template>

<script setup>
</script>

<style scoped>
/* 전체 페이지 */
.pf-home {
  width: 100%;
  background-color: #ffffff;
}

/* ----------------- Hero 영역 ----------------- */
.pf-home-hero {
  width: 100%;
  position: relative;   /* overlay를 위해 필요 */
  overflow: hidden;     /* 확대될 때 넘침 방지 */
}

/* 이미지 원본 비율 유지 + 가로 꽉 채우기 */
.pf-home-hero-img {
  width: 100%;
  height: auto;         /* 이미지 실제 비율 유지 (핵심 포인트) */
  display: block;       /* 불필요한 하단 여백 제거 */
}

/* 밝기 조절 overlay */
.pf-home-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.2); /* 밝기 유지 */
  pointer-events: none; /* overlay가 클릭 막지 않도록 */
}
</style>
