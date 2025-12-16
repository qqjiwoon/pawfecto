<template>
  <div class="settings-container">

    <!-- 브랜드 설정 정보 수정 -->

    <!-- 아이디 (수정 불가) -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ user.username }}</p>
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
      SAVE
    </button>

  </div>
</template>

<script setup>
// 브랜드 설정 수정 (PUT)
import { onMounted, reactive, computed } from "vue"
import { useRouter } from "vue-router"
import api from "@/plugins/axios"
import { brand, isBrandLoaded, loadBrand } from "@/stores/brand"

const router = useRouter()

// 최초 진입 시 브랜드 정보 로드
onMounted(async () => {
  if (!isBrandLoaded.value) {
    await loadBrand()
  }

  // 초기값 세팅
  Object.assign(form, {
    name: brand.value.name,
    email: brand.value.email,
    phone_number: brand.value.phone_number,
    pet_type: brand.value.pet_type,
    profile_image_url: brand.value.profile_image_url,
  })
})

// 브랜드 정보
const user = computed(() => brand.value)

// 수정 폼
const form = reactive({
  name: "",
  email: "",
  phone_number: "",
  pet_type: "",
  profile_image_url: "",
})

// 프로필 수정 요청
const updateProfile = async () => {
  try {
    await api.put("/accounts/update-profile/", form)

    // 최신 정보 다시 로드
    await loadBrand()

    router.push({ name: "brand-settings" })
  } catch (err) {
    console.error(err)
    alert("프로필 수정에 실패했습니다.")
  }
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
