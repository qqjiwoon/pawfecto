<template>
  <header class="pf-header">
    <nav class="pf-left-menu">
      <router-link to="/brand">Brand</router-link>
      <router-link to="/creator">Creator</router-link>
      <router-link to="/dashboard">
        Dashboard
      </router-link>
    </nav>

    <router-link to="/" class="pf-logo">
      Pawfecto
    </router-link>

    <nav class="pf-right-menu">
      <!-- 로그인 안 된 상태 -->
      <router-link v-if="!me" to="/login">Login</router-link>

      <!-- 로그인 된 상태 -->
      <a v-else href="#" @click.prevent="logout">Logout</a>
    </nav>
  </header>
</template>

<script setup>
/* ---------------------------------
   Header 로그인 상태 관리
--------------------------------- */
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/plugins/axios'

const router = useRouter()
const route = useRoute()

const me = ref(null)

/* 내 정보 조회 */
const fetchMe = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    me.value = null
    return
  }

  try {
    const res = await api.get('/accounts/me/')
    me.value = res.data
    console.log('[Header] current user', {
      id: res.data?.id,
      username: res.data?.username,
      name: res.data?.name,
      account_type: res.data?.account_type,
      route: route.fullPath,
      fullUser: res.data,
    })
  } catch (err) {
    console.error('[Header] failed to fetch /accounts/me/', err)
    localStorage.removeItem('access_token')
    me.value = null
  }
}

/* 최초 로드 */
onMounted(fetchMe)

/* 라우트 변경 시 상태 동기화 */
watch(
  () => route.fullPath,
  () => fetchMe()
)

/* 로그아웃 */
const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  me.value = null
  router.push('/login')
}

/* 대시보드 이동 */
</script>

<style scoped>
.pf-header {
  height: 70px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  position: relative;
}

.pf-left-menu,
.pf-right-menu {
  display: flex;
  gap: 32px;
}

.pf-left-menu a,
.pf-right-menu a {
  font-size: 16px;
  color: #9F9F9F;
  text-decoration: none;
}

.pf-left-menu a:hover,
.pf-right-menu a:hover {
  text-decoration: underline;
}

.pf-logo {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 28px;
  color: #000;
  text-decoration: none;
}
</style>
