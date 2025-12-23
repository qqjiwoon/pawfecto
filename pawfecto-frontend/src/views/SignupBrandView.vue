<template>
  <section class="pf-signup-hero">
    <div class="pf-signup-hero-overlay"></div>
    <h1 class="pf-signup-hero-title pf-logo">Pawfecto</h1>
    <div class="pf-signup-breadcrumb">
      <p>Home</p>
      <span> &gt; </span>
      <p>Signup</p>
    </div>
  </section>

  <div class="signup-container">
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
        <input type="text" class="input-field" v-model="form.signupId" placeholder="사용할 아이디를 입력하세요" required />
      </div>

      <div class="form-group">
        <label>비밀번호</label>
        <input type="password" class="input-field" v-model="form.password" placeholder="8자 이상, 영문/숫자 포함" required />
      </div>

      <div class="form-group">
        <label>비밀번호 확인</label>
        <input type="password" class="input-field" v-model="form.passwordConfirm" placeholder="비밀번호를 한번 더 입력하세요" required />
      </div>

      <div class="form-group">
        <label>브랜드 명</label>
        <input type="text" class="input-field" v-model="form.brandName" placeholder="브랜드명을 입력하세요" required />
      </div>

      <div class="form-group">
        <label>이메일 주소</label>
        <input type="email" class="input-field" v-model="form.email" placeholder="example@pawfecto.com" required />
      </div>

      <div class="form-group">
        <label>전화번호</label>
        <input type="text" class="input-field" v-model="form.phoneNumber" placeholder="010-0000-0000" required />
      </div>

      <div class="form-group">
        <label>주력 반려 동물</label>
        <select class="input-field" v-model="form.petType">
          <option value="">선택하세요</option>
          <option value="dog">강아지</option>
          <option value="cat">고양이</option>
        </select>
      </div>

      <div class="form-group">
        <label>프로필 이미지</label>
        <input type="file" class="input-field file-input-box" @change="handleFileUpload" accept="image/*" />
      </div>

      <button type="submit" class="submit-btn">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  accountType: 'brand',
  signupId: '',
  password: '',
  passwordConfirm: '',
  brandName: '',
  email: '',
  phoneNumber: '',
  petType: '',
  profileImageFile: null // 1. 파일 객체를 저장할 공간 추가
})

const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.profileImageFile = file // 2. 선택된 파일을 state에 저장
    console.log('Selected file:', file)
  }
}

const handleSignup = async () => {
  // 비밀번호 확인
  if (form.value.password !== form.value.passwordConfirm) {
    alert("비밀번호가 일치하지 않습니다.")
    return
  }

  // 3. FormData 객체 생성 (파일 업로드를 위해 필수!)
  const formData = new FormData()
  
  // 백엔드 Serializer 필드명에 맞춰서 append
  formData.append('username', form.value.signupId)
  formData.append('password', form.value.password)
  formData.append('email', form.value.email)
  formData.append('name', form.value.brandName)
  formData.append('phone_number', form.value.phoneNumber)
  formData.append('account_type', 'brand')
  
  if (form.value.petType) {
    formData.append('pet_type', form.value.petType)
  }

  // ★ 핵심: 이미지 파일이 있을 때만 추가 (키 이름은 백엔드 필드명인 'profile_image')
  if (form.value.profileImageFile) {
    formData.append('profile_image', form.value.profileImageFile)
  }

  try {
    await axios.post(
      "https://127.0.0.1:8000/accounts/signup/",
      formData, // 4. JSON 대신 formData 전송
      {
        headers: {
          "Content-Type": "multipart/form-data", // 5. 헤더 변경
        },
      }
    )

    alert("회원가입이 완료되었습니다.")
    router.push("/login")

  } catch (err) {
    console.error(err)
    if (err.response?.data) {
      // 에러 메시지가 객체인 경우 첫 번째 메시지 출력
      const firstErrorKey = Object.keys(err.response.data)[0]
      const firstErrorValue = err.response.data[firstErrorKey]
      alert(`${firstErrorKey}: ${firstErrorValue}`)
    } else {
      alert("회원가입 중 오류가 발생했습니다.")
    }
  }
}

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
/* Hero Section */
.pf-signup-hero {
  width: 100%;
  height: 45vh;
  background-image: url('@/assets/login-hero.png');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.pf-signup-hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.25);
  z-index: 1;
}

.pf-signup-hero-title {
  position: relative;
  z-index: 2;
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 54px;
  color: #fff;
  margin: 0;
}

.pf-signup-breadcrumb {
  position: relative;
  z-index: 2;
  margin-top: 10px;
  color: #fff;
  font-size: 14px;
  display: flex;
  gap: 6px;
}

/* Container & Typography */
.signup-container {
  max-width: 480px;
  margin: 60px auto;
  padding: 0 20px;
  font-family: 'Pretendard', sans-serif;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
  text-align: center;
}

.subtitle {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 40px;
  text-align: center;
}

/* Account Type Selector */
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

/* Form Groups & Inputs (From updatesettings) */
.form-group {
  margin-bottom: 25px; /* 약간 조정하여 가독성 확보 */
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.input-field {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  background: #fff;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #3A3A3A;
}

/* File Input Customization (From updatesettings) */
.file-input-box {
  display: flex;
  align-items: center;
  line-height: 44px;
  cursor: pointer;
}

.file-input-box::-webkit-file-upload-button {
  height: 28px;
  margin-right: 12px;
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

/* Submit Button (From updatesettings update-btn style) */
.submit-btn {
  display: block;
  width: 65%; /* updatesettings의 60%보다 가입 페이지 특성상 조금 더 넓게 조정 */
  padding: 16px;
  background: #3A3A3A;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  margin: 60px auto;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: #252525;
}
</style>
