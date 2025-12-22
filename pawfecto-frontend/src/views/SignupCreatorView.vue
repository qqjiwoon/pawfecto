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
        <label>이메일 주소</label>
        <input type="email" class="input-field" v-model="form.email" placeholder="example@pawfecto.com" required />
      </div>

      <div class="form-group">
        <label>전화번호</label>
        <input type="text" class="input-field" v-model="form.phoneNumber" placeholder="010-0000-0000" required />
      </div>

      <div class="form-group">
        <label>이름</label>
        <input type="text" class="input-field" v-model="form.name" placeholder="이름을 입력하세요" required />
      </div>

      <div class="form-group">
        <label>주소</label>
        <input type="text" class="input-field" v-model="form.address" placeholder="주소를 입력하세요" required />
      </div>

      <div class="form-group">
        <label>반려동물 종류</label>
        <select class="input-field" v-model="form.petType">
          <option value="">선택하세요</option>
          <option value="dog">강아지</option>
          <option value="cat">고양이</option>
        </select>
      </div>

      <div class="form-group">
        <label>SNS 계정명</label>
        <input type="text" class="input-field" v-model="form.snsHandle" placeholder="puppy_ssafy" />
      </div>

      <div class="form-group">
        <label>SNS 계정 URL</label>
        <input type="text" class="input-field" v-model="form.snsUrl" placeholder="https://instagram.com/..." />
      </div>

      <div class="form-group">
        <label>SNS 스타일</label>
        <div class="tag-container">
          <div
            v-for="tag in styleTags"
            :key="tag"
            class="tag"
            :class="{ active: selectedTags.includes(tag) }"
            @click="toggleTag(tag)"
          >
            #{{ tag }}
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>프로필 이미지</label>
        <input type="file" class="file-input-box" @change="handleFileUpload" />
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
  accountType: 'creator',
  signupId: '',
  password: '',
  passwordConfirm: '',
  email: '',
  phoneNumber: '',
  name: '',
  address: '',
  petType: '',
  snsHandle: '',
  snsUrl: '',
  styleTags: [],
  profileImage: null,
})

const handleFileUpload = (e) => {
  form.value.profileImage = e.target.files[0]
}

const styleTags = [
  '활발한', '야외감성', '차분한', '웃긴', '힐링되는', '포근한',
  '감동적인', '감각적인', '깔끔한'
]

const selectedTags = ref([])

function toggleTag(tag) {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter(t => t !== tag)
  } else {
    selectedTags.value.push(tag)
  }
}

const handleSignup = async () => {
  if (form.value.password !== form.value.passwordConfirm) {
    alert("비밀번호가 일치하지 않습니다.")
    return
  }

  const formData = new FormData()
  formData.append('username', form.value.signupId)
  formData.append('password', form.value.password)
  formData.append('email', form.value.email)
  formData.append('name', form.value.name)
  formData.append('phone_number', form.value.phoneNumber)
  formData.append('account_type', 'creator')

  if (form.value.petType) {
    formData.append('pet_type', form.value.petType)
  }

  if (form.value.profileImage) {
    formData.append('profile_image', form.value.profileImage)
  }

  formData.append()

  try {
    await axios.post(
      "http://127.0.0.1:8000/accounts/signup/",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    )

    alert("회원가입이 완료되었습니다.")
    router.push("/login")
  } catch (err) {
    console.error(err)
    if (err.response?.data) {
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
    if (newValue === 'brand') {
      router.push('/signup/brand')
    }
  }
)
</script>

<style scoped>
/* Styling matching SignupBrand */
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

.form-group input,
.form-group select {
  width: 100%;
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

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 8px 16px;
  border-radius: 10px;
  background: #f7f7f7;
  border: 1px solid #ddd;
  cursor: pointer;
  font-size: 14px;
}

.tag.active {
  background: #7E6B5A;
  color: white;
  border-color: #7E6B5A;
}

.submit-btn {
  width: 100%;
  padding: 14px;
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
