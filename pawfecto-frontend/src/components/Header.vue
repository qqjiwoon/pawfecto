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


        <nav class="pf-right=menu">
            <router-link to="/login">Login</router-link>
        </nav>

    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const me = ref(null)

// 로그인한 사용자 정보 가져오기
onMounted(async () => {
  const token = localStorage.getItem('access')
  if (!token) return

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
})

// Dashboard 클릭 시 동작
const goDashboard = async () => {
  const token = localStorage.getItem('access')

  // 토큰 자체가 없으면 로그인 페이지
  if (!token) {
    router.push('/login')
    return
  }

  try {
    // ⭐️ 클릭 시점에 다시 me 조회
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
    // 토큰 만료 / 인증 실패
    localStorage.removeItem('access')
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