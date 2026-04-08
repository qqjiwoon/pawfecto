<template>
  <div class="pf-find-id">

    <!-- Hero -->
    <section class="pf-find-id-hero">
      <div class="pf-find-id-hero-overlay"></div>

      <h1 class="pf-find-id-hero-title pf-logo">Pawfecto</h1>

      <div class="pf-find-id-breadcrumb">
        <p>Home</p>
        <span> &gt; </span>
        <p>Find ID</p>
      </div>
    </section>

    <!-- Form -->
    <section class="pf-find-id-form-section">

      <h2 class="pf-find-id-title">아이디 찾기</h2>
      <p class="pf-find-id-desc">
        가입 시 사용한 이메일을 입력해 주세요.<br />
        아이디 일부를 안내해 드립니다.
      </p>

      <form class="pf-find-id-form">
        <label>이메일</label>
        <input
          type="email"
          placeholder="pawfecto@email.com"
          v-model="email"
        />

        <button
          class="pf-find-id-submit"
          @click.prevent="handleFindId"
          :disabled="loading"
        >
          {{ loading ? "확인 중..." : "아이디 찾기" }}
        </button>

        <!-- 결과 메시지 -->
        <p v-if="result" class="pf-find-id-result">
          {{ result }}
        </p>

        <p v-if="error" class="pf-find-id-error">
          {{ error }}
        </p>

        <div class="pf-find-id-back">
          <router-link to="/login">로그인으로 돌아가기</router-link>
        </div>
      </form>

    </section>

  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const email = ref("")
const result = ref("")
const error = ref("")
const loading = ref(false)

const handleFindId = async () => {
  if (!email.value) {
    error.value = "이메일을 입력해 주세요."
    return
  }

  loading.value = true
  result.value = ""
  error.value = ""

  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/accounts/find-id/",
      { email: email.value },
      { headers: { "Content-Type": "application/json" } }
    )

    result.value = `회원님의 아이디는 ${res.data.username_hint} 입니다.`
  } catch (err) {
    console.error(err)
    error.value = "일치하는 계정을 찾을 수 없습니다."
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ----------------- Hero 영역 ----------------- */
.pf-find-id-hero {
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

.pf-find-id-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
  z-index: 1; /* 오버레이가 아래로 가도록 설정 */
}

.pf-find-id-hero-title {
  position: relative; 
  z-index: 2; /* 오버레이보다 위로 올림 */
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
  margin: 0; /* 기본 마진 제거 */
}

.pf-find-id-breadcrumb {
  position: relative;
  z-index: 2; /* 오버레이보다 위로 올림 */
  margin-top: 10px; /* 타이틀과의 간격 조절 */
  color: #fff;
  font-size: 14px;
  display: flex;
  gap: 6px;
  font-family: inherit;
}

.pf-find-id-breadcrumb p,
.pf-find-id-breadcrumb span {
  margin: 0;
  padding: 0;
}

.pf-find-id-form-section {
  max-width: 360px;
  margin: 0 auto;
  padding: 60px 20px;
  text-align: center;
}

.pf-find-id-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.pf-find-id-desc {
  font-size: 14px;
  color: #777;
  margin-bottom: 30px;
}

.pf-find-id-form label {
  display: block;
  text-align: left;
  font-size: 14px;
  margin-bottom: 6px;
}

.pf-find-id-form input {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.pf-find-id-submit {
  width: 100%;
  padding: 12px;
  background: #222;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
}

.pf-find-id-submit:disabled {
  background: #999;
}

.pf-find-id-result {
  margin-top: 20px;
  color: #222;
  font-weight: 600;
}

.pf-find-id-error {
  margin-top: 20px;
  color: #d9534f;
}

.pf-find-id-back {
  margin-top: 30px;
  font-size: 14px;
  display: flex;
  justify-content: center;
}

.pf-find-id-back a {
  color: #555;
  text-decoration: none;
}

.pf-find-id-back a:hover {
  text-decoration: underline;
}
</style>
