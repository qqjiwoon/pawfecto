<template>
  <div class="pf-login">

    <section class="pf-login-hero">
      <div class="pf-login-hero-overlay"></div>

      <h1 class="pf-login-hero-title pf-logo">Pawfecto</h1>

      <div class="pf-login-breadcrumb">
        <p>Home</p>
        <span> &gt; </span>
        <p>Login</p>
      </div>
    </section>

    <section class="pf-login-form-section">

      <h2 class="pf-login-title">로그인</h2>
      <p class="pf-login-desc">
        협찬, 이제는 복잡하지 않게<br />
        반려동물 인플루언서를 위한 완벽한 매칭 — Pawfecto
      </p>

      <form class="pf-login-form">
        <label>아이디</label>
        <input type="text" placeholder="Pawfecto 아이디 입력" v-model="username" />

        <label>비밀번호</label>
        <input type="password" placeholder="Pawfecto 비밀번호 입력" v-model="password" />

        <button class="pf-login-submit" @click.prevent="handleLogin">로그인</button>

        <button type="button" class="pf-login-instagram" @click="loginWithInstagram">
          <img src="@/assets/instagram-icon.png" alt="instagram" />
          Log in with Instagram
        </button>

        <div class="pf-login-find">
          <router-link to="/find-id">아이디 찾기</router-link>
          <span>|</span>
          <router-link to="/find-password">비밀번호 찾기</router-link>
        </div>

        <div class="pf-login-signup">
          계정이 없으신가요?
          <router-link to="/signup/brand">회원가입 하러가기</router-link>
        </div>
        
      </form>

    </section>

  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const password = ref('')


// 인스타그램 로그인 기능 구현
// const loginWithInstagram = () => {
//   const clientId = import.meta.env.VITE_INSTAGRAM_CLIENT_ID  // Instagram 개발자 대시보드에서 제공된 클라이언트 ID
//   const redirectUri = 'https://localhost:5173/callback/instagram'  // 리디렉션 URI
//     const scope = [
//       'instagram_business_basic',
//       'instagram_business_manage_messages',
//       'instagram_business_manage_comments',
//       'instagram_business_content_publish',
//       'instagram_business_manage_insights'
//     ].join(',')
//   const responseType = 'code'  // 인증 코드 받기

//   // Instagram OAuth 인증 URL 생성
//   const loginUrl =
//     `https://api.instagram.com/oauth/authorize` +
//     `?client_id=${clientId}` +
//     `&redirect_uri=${encodeURIComponent(redirectUri)}` +
//     `&response_type=${responseType}` +
//     `&scope=${encodeURIComponent(scope)}` +
//     `&force_reauth=true` 
//   // Instagram 로그인 페이지로 리디렉션
//   window.location.href = loginUrl
// }

const handleLogin = async () => {
  try {
    const res = await axios.post(
      "https://127.0.0.1:8000/accounts/login/",
      {
        username: username.value,
        password: password.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )

    // 토큰 저장
    localStorage.setItem("access_token", res.data.access)
    localStorage.setItem("refresh_token", res.data.refresh)

    
    // 로그인 성공 → 메인
    router.push("/")
  } catch (err) {
    console.error(err)
    alert("아이디 또는 비밀번호가 올바르지 않습니다.")
  }
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

  /* 중앙 정렬을 위한 Flexbox 추가 */
  display: flex;
  flex-direction: column;
  justify-content: center; /* 세로 중앙 */
  align-items: center;     /* 가로 중앙 */
  text-align: center;
}

.pf-login-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
  z-index: 1; /* 오버레이가 아래로 가도록 설정 */
}

.pf-login-hero-title {
  position: relative;
  z-index: 2; /* 오버레이보다 위로 올림 */
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
  margin: 0; /* 기본 마진 제거 */
}

.pf-login-breadcrumb {
  position: relative;
  z-index: 2; /* 오버레이보다 위로 올림 */
  margin-top: 10px; /* 타이틀과의 간격 조절 */
  color: #fff;
  font-size: 14px;
  display: flex;
  gap: 6px;
  font-family: inherit;
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
  /* [수정] 가독성을 위해 색상을 약간 더 진하게 변경 */
  color: #666;
  line-height: 1.6;
  /* [수정] 폼과의 간격을 더 넓힘 (40px -> 60px) */
  margin-bottom: 60px;
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
  font-size: 14px; /* 폰트 사이즈 약간 키움 */
  box-sizing: border-box;
  /* [추가] 부드러운 색상 전환을 위한 트랜지션 */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
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
  /* [추가] 부드러운 호버 효과를 위한 트랜지션 */
  transition: background-color 0.3s ease;
}

/* [추가] 로그인 버튼 호버 효과 */
.pf-login-submit:hover {
  background-color: #555; /* 약간 밝아짐 */
}


.pf-login-signup {
  text-align: center;
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 16px;
}

.pf-login-signup a {
  color: #ff7f00;
  text-decoration: none;
  /* [추가] 링크 호버 트랜지션 */
  transition: color 0.2s ease;
}

/* [추가] 회원가입 링크 호버 효과 */
.pf-login-signup a:hover {
  color: #e67300; /* 약간 진해짐 */
  text-decoration: underline;
}

.pf-login-find {
  margin-top: 12px;
  text-align: center;
  font-size: 14px;
}

.pf-login-find a {
  color: #666;
  text-decoration: none;
  transition: color 0.2s ease;
}

.pf-login-find a:hover {
  color: #333;
  text-decoration: underline;
}

.pf-login-find span {
  margin: 0 8px;
  color: #aaa;
}

/* Instagram 로그인 버튼 */
.pf-login-instagram {
  margin-top: 12px;
  width: 100%;
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
.pf-login-instagram:hover {
  background-color: #f9f9f9; /* 아주 연한 회색 배경 */
  border-color: #ccc; /* 약간 진한 테두리 */
}


.pf-login-instagram img {
  width: 20px;
  height: 20px;
}
</style>