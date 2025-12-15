<template>

  <div id="app">
    <!-- 공통 헤더 -->
    <Header />

    <!-- 페이지 내용 -->
    <main class="pf-container">
      <RouterView />
    </main>

    <!-- 공통 푸터 -->
    <Footer />

  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
.pf-container {
  /* max-width: 1200px;    /* 전체 페이지 공통 폭 */ 
  /* margin: 0 auto;       /* 가운데 정렬 */
  /* padding: 0 32px;      /* 좌우 여백 통일 */
  width: 100%;
}

</style>
