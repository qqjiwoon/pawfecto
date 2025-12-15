<template>
  <section class="pf-signup-hero">
    <div class="pf-signup-hero-overlay"></div>

    <h1 class="pf-signup-hero-title">Pawfecto</h1>

    <div class="pf-signup-breadcrumb">
      <p>Home</p>
      <span> &gt; </span>
      <p>Signup</p>
    </div>
  </section>
  <div class="signup-container">
    <h1>Brand Signup</h1>

    <h2 class="title">회원 가입</h2>
    <p class="subtitle">
      협찬, 이제는 복잡하지 않게
      <br />반려동물 인플루언서를 위한 완벽한 매칭 - Pawfecto
    </p>

    <div class="account-type">
      <label>
        <input type="radio" value="brand" v-model="form.accountType" />
        Brand
      </label>
      <label>
        <input type="radio" value="creator" v-model="form.accountType" />
        Creator
      </label>
    </div>

    <form @submit.prevent="handleSignup">
      <div class="form-group">
        <label>아이디</label>
        <input type="text" v-model="form.signupId" required />
      </div>

      <div class="form-group">
        <label>비밀번호</label>
        <input type="password" v-model="form.password" required />
      </div>

      <div class="form-group">
        <label>비밀번호 확인</label>
        <input type="password" v-model="form.passwordConfirm" required />
      </div>

      <div class="form-group">
        <label>브랜드 명</label>
        <input type="text" v-model="form.brandName" required />
      </div>

      <div class="form-group">
        <label>이메일 주소</label>
        <input type="email" v-model="form.email" required />
      </div>

      <div class="form-group">
        <label>전화번호</label>
        <input type="text" v-model="form.phoneNumber" required />
      </div>

      <div class="form-group">
        <label>주력 반려 동물</label>
        <select v-model="form.petType">
          <option value="">선택하세요</option>
          <option value="dog">강아지</option>
          <option value="cat">고양이</option>
        </select>
      </div>

      <div class="form-group">
        <label>프로필 이미지</label>
        <input type="file" @change="handleFileUpload" />
      </div>

      <button type="submit" class="submit-btn">가입하기</button>
    </form>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
    accountType: 'brand',
    signupId: '',
    password: '',
    passwordConfirm: '',
    brandName: '',
    email: '',
    phoneNumber: '',
})

const handleSignup = (() =>{
    console.log('form.value')
    console.log('form submitted!!!')
})

watch(
  () => form.value.accountType,
  (newValue) => {
    if (newValue === 'creator') {
      router.push('/signup/creator')
    }
  }
)


</script>

<style scoped>

.pf-signup-hero {
  width: 100%;
  height: 45vh;
  background-image: url('@/assets/login-hero.png');
  background-size: cover;
  background-position: center;
  position: relative;
}

.pf-signup-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
}

.pf-signup-hero-title {
  position: absolute;
  bottom: 110px;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
}

.pf-signup-breadcrumb {
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

.pf-signup-breadcrumb p,
.pf-signup-breadcrumb span {
  margin: 0;
  padding: 0;
}


.signup-container {
  max-width: 480px;
  margin: 60px auto;
  text-align: center;
  padding: 0 20px;
  font-family: 'Pretendard', sans-serif;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.subtitle {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 35px;
}

.account-type {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 35px;
  font-size: 15px;
  font-weight: 500;
}

.account-type input {
  margin-right: 6px;
}

.form-group {
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

.form-group input{
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.form-group select {
  width: 105%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #000;
}

.submit-btn {
  width: 105%;
  padding: 12px;
  margin-top: 50px;
  background: #7b7b7b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.2s;
}

.submit-btn:hover {
  background: #3A3A3A;
}

</style>