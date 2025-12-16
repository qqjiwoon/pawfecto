<template>
    <header class="pf-header">
        <nav class="pf-left-menu">
            <router-link to="/brand">Brand</router-link>
            <router-link to="/creator">Creator</router-link>
            <router-link to="/dashboard" @click.prevent="goDashboard">
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
// 로그인 상태 동기화 (Header 전용)
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const me = ref(null)

// 로그인 사용자 정보 조회
const fetchMe = async () => {
  const token = localStorage.getItem('access')
  if (!token) {
    me.value = null
    return
  }

  try {
    const res = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/accounts/me/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    me.value = res.data
  } catch (err) {
    localStorage.removeItem('access')
    me.value = null
  }
}

// 최초 마운트 시 로그인 상태 확인
onMounted(fetchMe)

// 라우트 변경 시 로그인 상태 재확인
watch(
  () => route.fullPath,
  () => fetchMe()
)

// 로그아웃
const logout = () => {
  localStorage.removeItem('access')
  me.value = null
  router.push('/login')
}

// Dashboard 이동
const goDashboard = async () => {
  const token = localStorage.getItem('access')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const res = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/accounts/me/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const user = res.data

    if (user.account_type === 'creator') {
      router.push(`/dashboard/creator/${user.id}`)
    } else if (user.account_type === 'brand') {
      router.push(`/dashboard/brand/${user.id}`)
    }
  } catch (err) {
    localStorage.removeItem('access')
    me.value = null
    router.push('/login')
  }
}
</script>



<style scoped>
.pf-header {
  /* max-width: 1200px; */
  height: 70px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  /* border-bottom: 1px solid #f2f2f2; */
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