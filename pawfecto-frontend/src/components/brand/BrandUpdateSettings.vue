<template>
  <div class="settings-container">

    <!-- 브랜드 설정 정보 수정 -->

    <!-- 아이디 (수정 불가) -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ form.username }}</p>
    </div>

    <!-- 비밀번호 -->
    <div class="form-group">
      <label>비밀번호</label>
      <input
        class="input-field"
        type="password"
        v-model="form.password"
        placeholder="새 비밀번호 입력"
      />
    </div>

    <!-- 비밀번호 확인 -->
    <div class="form-group">
      <label>비밀번호 확인</label>
      <input
        class="input-field"
        type="password"
        v-model="form.passwordConfirm"
        placeholder="비밀번호 재입력"
      />
    </div>

    <!-- 브랜드명 -->
    <div class="form-group">
      <label>브랜드명</label>
      <input class="input-field" v-model="form.name" />
    </div>

    <!-- 이메일 주소 -->
    <div class="form-group">
      <label>이메일 주소</label>
      <input class="input-field" v-model="form.email" />
    </div>

    <!-- 전화번호 -->
    <div class="form-group">
      <label>전화번호</label>
      <input class="input-field" v-model="form.phone_number" />
    </div>

    <!-- 주력 동물 종류 -->
    <div class="form-group">
      <label>주력 동물 종류</label>
      <select class="input-field" v-model="form.pet_type">
        <option value="dog">dog</option>
        <option value="cat">cat</option>
      </select>
    </div>

    <!-- 프로필 이미지 URL -->
    <div class="form-group">
      <label>프로필 이미지 URL</label>
      <input class="input-field" v-model="form.profile_image_url" />
    </div>

    <!-- 저장 버튼 -->
    <button class="update-btn" @click="updateProfile">
      저장
    </button>

  </div>
</template>

<script setup>
// 브랜드 설정 수정 (PUT)
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/plugins/axios"
import { useBrandStore } from "@/stores/brand"

const router = useRouter()
const brandStore = useBrandStore()
 
const isLoaded = ref(false)

const form = ref({
  username: "",
  password: "",
  passwordConfirm: "",
  name: "",
  email: "",
  phone_number: "",
  pet_type: "dog",
  profile_image_url: "",
})

/* 최초 로드 */
onMounted(async () => {
  await brandStore.loadBrand()

  const data = brandStore.brand
  if (!data) return

  Object.assign(form.value, {
    username: data.username,
    name: data.name,
    email: data.email,
    phone_number: data.phone_number,
    pet_type: data.pet_type,
    profile_image_url: data.profile_image_url,
  })

  isLoaded.value = true
})

/* 저장 */
const updateProfile = async () => {
  if (form.value.password && form.value.password !== form.value.passwordConfirm) {
    alert("비밀번호가 일치하지 않습니다.")
    return
  }

  const payload = {
    name: form.value.name,
    email: form.value.email,
    phone_number: form.value.phone_number,
    pet_type: form.value.pet_type,
    profile_image_url: form.value.profile_image_url,
  }

  if (form.value.password) {
    payload.password = form.value.password
  }

  await api.put("/accounts/update-profile/", payload)

  // store 갱신
  brandStore.isLoaded = false
  await brandStore.loadBrand()

  router.push({ name: "brand-settings" })
}
</script>

<style scoped>
/* 브랜드 설정 페이지 레이아웃 */
.settings-container {
  max-width: 480px;
  margin: 130px auto;
  padding: 0 10px;
  font-family: 'Pretendard', sans-serif;
}

.form-group {
  margin-bottom: 35px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

/* 입력 필드 */
.input-field {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

/* 읽기 전용 필드 */
.readonly-field {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  background: #f5f5f5;
  border-radius: 8px;
  color: #555;
  font-size: 14px;
  box-sizing: border-box;
}

/* 저장 버튼 */
.update-btn {
  display: block;
  width: 60%;
  padding: 16px;
  background: #3A3A3A;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  margin: 80px auto;
}
</style>
