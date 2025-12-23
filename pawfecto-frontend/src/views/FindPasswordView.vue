<template>
  <div class="pf-find-pw">

    <!-- Hero -->
    <section class="pf-find-pw-hero">
      <div class="pf-find-pw-hero-overlay"></div>

      <h1 class="pf-find-pw-hero-title pf-logo">Pawfecto</h1>

      <div class="pf-find-pw-breadcrumb">
        <p>Home</p>
        <span> &gt; </span>
        <p>Find Password</p>
      </div>
    </section>

    <!-- Form -->
    <section class="pf-find-pw-form-section">

      <h2 class="pf-find-pw-title">비밀번호 찾기</h2>
      <p class="pf-find-pw-desc">
        아이디와 가입 시 사용한 이메일을 입력해 주세요.<br />
        비밀번호 재설정 안내 메일을 보내드립니다.
      </p>

      <form class="pf-find-pw-form">
        <label>아이디</label>
        <input
          type="text"
          placeholder="pawfecto123"
          v-model="username"
        />

        <label>이메일</label>
        <input
          type="email"
          placeholder="pawfecto@email.com"
          v-model="email"
        />

        <button
          class="pf-find-pw-submit"
          @click.prevent="handleFindPassword"
          :disabled="loading"
        >
          {{ loading ? "메일 발송 중..." : "비밀번호 재설정 메일 보내기" }}
        </button>

        <!-- 결과 메시지 -->
        <p v-if="result" class="pf-find-pw-result">
          {{ result }}
        </p>

        <p v-if="error" class="pf-find-pw-error">
          {{ error }}
        </p>

        <div class="pf-find-pw-back">
          <router-link to="/login">로그인으로 돌아가기</router-link>
        </div>
      </form>

    </section>

  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const username = ref("")
const email = ref("")
const result = ref("")
const error = ref("")
const loading = ref(false)

const handleFindPassword = async () => {
  if (!username.value || !email.value) {
    error.value = "아이디와 이메일을 모두 입력해 주세요."
    return
  }

  loading.value = true
  result.value = ""
  error.value = ""

  try {
    await axios.post(
      "https://127.0.0.1:8000/accounts/password-reset/",
      {
        username: username.value,
        email: email.value,
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    )

    result.value =
      "비밀번호 재설정 안내 메일을 발송했습니다. 이메일을 확인해 주세요."
  } catch (err) {
    console.error(err)
    error.value = "입력한 정보와 일치하는 계정을 찾을 수 없습니다."
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ----------------- Hero 영역 ----------------- */
.pf-find-pw-hero {
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

.pf-find-pw-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
  z-index: 1; /* 오버레이가 아래로 가도록 설정 */
}

.pf-find-pw-hero-title {
  position: relative; 
  z-index: 2; /* 오버레이보다 위로 올림 */
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
  margin: 0; /* 기본 마진 제거 */
}

.pf-find-pw-breadcrumb {
  position: relative;
  z-index: 2; /* 오버레이보다 위로 올림 */
  margin-top: 10px; /* 타이틀과의 간격 조절 */
  color: #fff;
  font-size: 14px;
  display: flex;
  gap: 6px;
  font-family: inherit;
}

.pf-find-pw-breadcrumb p,
.pf-find-pw-breadcrumb span {
  margin: 0;
  padding: 0;
}

.pf-find-pw-form-section {
  max-width: 360px;
  margin: 0 auto;
  padding: 60px 20px;
  text-align: center;
}

.pf-find-pw-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.pf-find-pw-desc {
  font-size: 14px;
  color: #777;
  margin-bottom: 30px;
}

.pf-find-pw-form label {
  display: block;
  text-align: left;
  font-size: 14px;
  margin-bottom: 6px;
}

.pf-find-pw-form input {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.pf-find-pw-submit {
  width: 100%;
  padding: 12px;
  background: #222;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
}

.pf-find-pw-submit:disabled {
  background: #999;
}

.pf-find-pw-result {
  margin-top: 20px;
  color: #222;
  font-weight: 600;
}

.pf-find-pw-error {
  margin-top: 20px;
  color: #d9534f;
}

.pf-find-pw-back {
  margin-top: 30px;
  font-size: 14px;
  display: flex;
  justify-content: center;
}

.pf-find-pw-back a {
  color: #555;
  font-size: 13px;
  text-decoration: none;
}

.pf-find-pw-back a:hover {
  text-decoration: underline;
}
</style>
