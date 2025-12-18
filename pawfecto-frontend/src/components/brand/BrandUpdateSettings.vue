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
      <label>프로필 이미지</label>
      
      <div v-if="form.profile_image_url" style="margin-bottom: 10px;">
        <img :src="form.profile_image_url" width="100" height="100" style="border-radius: 50%; object-fit: cover;" />
      </div>

      <input 
        type="file" 
        @change="onFileChange" 
        accept="image/*" 
        class="input-field file-input-box" 
      />
    </div>

    <!-- 저장 버튼 -->
    <button class="update-btn" @click="updateProfile">
      저장
    </button>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/plugins/axios"
import { useBrandStore } from "@/stores/brand"

const router = useRouter()
const brandStore = useBrandStore()
const isLoaded = ref(false)

// 선택된 파일 자체를 담을 변수
const imageFile = ref(null)

const form = ref({
  username: "",
  password: "",
  passwordConfirm: "",
  name: "",
  email: "",
  phone_number: "",
  pet_type: "dog",
  // 프로필 이미지 URL은 초기 로드 시 정보 확인용으로만 유지
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

/* 파일 선택 핸들러 */
function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    form.value.profile_image_url = URL.createObjectURL(file)
  }
}

/* 저장 */
const updateProfile = async () => {
  if (form.value.password && form.value.password !== form.value.passwordConfirm) {
    alert("비밀번호가 일치하지 않습니다.")
    return
  }

  // 파일을 전송하기 위해 FormData 생성
  const formData = new FormData()
  formData.append("name", form.value.name)
  formData.append("email", form.value.email)
  formData.append("phone_number", form.value.phone_number)
  formData.append("pet_type", form.value.pet_type)

  // 새 이미지가 선택되었다면 FormData에 추가
  if (imageFile.value) {
    // 백엔드 모델 필드명(profile_image)에 맞춰 전송
    formData.append("profile_image", imageFile.value)
  }

  if (form.value.password) {
    formData.append("password", form.value.password)
  }

  try {
    // PUT 요청 시 payload 대신 formData 전송
    await api.put("/accounts/update-profile/", formData)

    alert("프로필 정보가 수정되었습니다.")
    brandStore.isLoaded = false
    await brandStore.loadBrand()
    router.push({ name: "brand-settings" })
  } catch (err) {
    console.error(err)
    alert("정보 수정에 실패했습니다.")
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
  border: 1px solid #ddd; /* 회색 실선 테두리 */
  border-radius: 8px;     /* 둥근 모서리 */
  font-size: 14px;
  box-sizing: border-box;
  background: #fff;
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

/* 파일 입력창 스타일 */
.file-input {
  width: 100%;
  padding: 8px 0;
  font-size: 14px;
  border: none;
  background: transparent;
}

/* 파일 선택창을 위한 전용 정렬 스타일 */
.file-input-box {
  display: flex;
  align-items: center; /* 버튼과 텍스트를 세로 중앙으로 */
  line-height: 44px;   /* 테두리 안에서 텍스트 높이 확보 */
  cursor: pointer;
}

/* 브라우저 기본 '파일 선택' 버튼 스타일 조정 */
.file-input-box::-webkit-file-upload-button {
  height: 28px;
  margin-right: 12px;
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  color: #333;
}
</style>
