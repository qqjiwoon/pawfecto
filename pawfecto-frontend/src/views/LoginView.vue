<template>
  <div class="pf-login">

    <!-- Hero -->
    <section class="pf-login-hero">
      <div class="pf-login-hero-overlay"></div>

      <h1 class="pf-login-hero-title">Pawfecto</h1>

      <div class="pf-login-breadcrumb">
        <p>Home</p>
        <span> &gt; </span>
        <p>Login</p>
      </div>
    </section>

    <!-- 로그인 폼 영역 -->
    <section class="pf-login-form-section">

      <h2 class="pf-login-title">로그인</h2>
      <p class="pf-login-desc">
        협찬, 이제는 복잡하지 않게<br />
        반려동물 인플루언서를 위한 완벽한 매칭 — Pawfecto
      </p>

      <form class="pf-login-form">
        <label>아이디</label>
        <input type="text" placeholder="Abc1234" v-model="username" />

        <label>비밀번호</label>
        <input type="password" placeholder="Abc1234" v-model="password" />

        <!-- 로그인 버튼 -->
        <button class="pf-login-submit" @click.prevent="handleLogin">로그인</button>

        <div class="pf-login-signup">
          계정이 없으신가요?
          <router-link to="/signup/brand">회원가입 하러가기</router-link>
        </div>

        <button class="pf-login-instagram">
          <img src="@/assets/instagram-icon.png" alt="instagram" />
          Log in with Instagram
        </button>
      </form>

    </section>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

const username = ref('')
const password = ref('')

const handleLogin = () => {
  if (!username.value.trim()) {
    alert('아이디를 입력해주세요.')
    return
  }

  if (!password.value.trim()) {
    alert('비밀번호를 입력해주세요.')
    return
  }

  // 로그인 성공 → 홈으로 이동
  router.push('/')
}
</script>



<style scoped>
/* 전체 페이지 */
.pf-login {
  width: 100%;
  background-color: #ffffff;
}

/* ----------------- Hero 영역 ----------------- */
.pf-login-hero {
  width: 100%;
  height: 45vh;
  background-image: url('@/assets/login-hero.png');
  background-size: cover;
  background-position: center;
  position: relative;
}

.pf-login-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
}

.pf-login-hero-title {
  position: absolute;
  bottom: 110px;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
}

.pf-login-breadcrumb {
  position: absolute;
  bottom: 70px;
  left: 50%;
  transform: translateX(-50%);
  color: #fff;
  font-size: 14px;
  display: flex;
  gap: 6px;

  font-family: inherit; /* Rubik Bubbles 상속 방지 */
}

.pf-login-breadcrumb p,
.pf-login-breadcrumb span {
  margin: 0;
  padding: 0;
}

/* ----------------- Form 영역 ----------------- */
.pf-login-form-section {
  width: 100%;
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pf-login-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.pf-login-desc {
  text-align: center;
  color: #888;
  line-height: 1.6;
  margin-bottom: 40px;
}

.pf-login-form {
  width: 360px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pf-login-form label {
  color: #444;
  font-size: 14px;
  margin-top: 12px;
}

.pf-login-form input {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box; /* 입력창도 정확한 360px 유지 */
}

/* 로그인 버튼 */
.pf-login-submit {
  width: 100%;
  padding: 14px;
  background-color: #333;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 400;
  cursor: pointer;
  margin-top: 16px;
}

.pf-login-signup {
  text-align: right;
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 16px;
}

.pf-login-signup a {
  color: #ff7f00;
  text-decoration: none;
}

/* Instagram 로그인 버튼 */
.pf-login-instagram {
  margin-top: 12px;
  width: 100%;
  box-sizing: border-box; /* 버튼 폭 = 360px로 정확히 통일 */
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
}

.pf-login-instagram img {
  width: 20px;
  height: 20px;
}
</style>
