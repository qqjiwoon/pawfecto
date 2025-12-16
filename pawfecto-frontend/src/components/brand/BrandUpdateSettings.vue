<template>
  <div class="settings-container">

    <!-- 아이디 (읽기 전용) -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ form.loginId }}</p>
    </div>

    <!-- 비밀번호 -->
    <div class="form-group">
      <label>비밀번호</label>
      <input type="password" v-model="form.password" placeholder="비밀번호" />
    </div>

    <!-- 비밀번호 확인 -->
    <div class="form-group">
      <label>비밀번호 확인</label>
      <input type="password" v-model="form.passwordConfirm" placeholder="비밀번호 확인" />
    </div>

    <!-- 브랜드명 -->
    <div class="form-group">
      <label>브랜드명</label>
      <input type="text" v-model="form.name" placeholder="브랜드명" />
    </div>

    <!-- 이메일 주소 -->
    <div class="form-group">
      <label>이메일 주소</label>
      <input type="email" v-model="form.email" placeholder="이메일 주소" />
    </div>

    <!-- 전화번호 -->
    <div class="form-group">
      <label>전화번호</label>
      <input type="text" v-model="form.phoneNumber" placeholder="전화번호" />
    </div>

    <!-- 주력 동물 종류 -->
    <div class="form-group">
      <label>주력 동물 종류</label>
      <input type="text" v-model="form.brandPetFocus" placeholder="강아지 / 고양이 등" />
    </div>

    <!-- 프로필 이미지 -->
    <div class="form-group">
      <label>프로필 이미지</label>

      <div class="image-box">
        <p>{{ form.profileImage ? form.profileImage.name : '첨부파일' }}</p>

        <label class="file-btn">
          파일 선택
          <input type="file" @change="handleFileUpload" />
        </label>
      </div>
    </div>

    <!-- SAVE 버튼 -->
    <button class="save-btn" @click="handleSave">SAVE</button>

  </div>
</template>


<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"

// props
const props = defineProps({
  brandId: Number
})

const router = useRouter()

// 현재 브랜드 찾기
const currentBrand = computed(() =>
  brands.value.find(b => b.id === props.brandId)
)

// form 초기값 세팅
const form = ref({
  loginId: currentBrand.value?.username || "",
  password: "",
  passwordConfirm: "",
  name: currentBrand.value?.name || "",
  email: currentBrand.value?.email || "",
  phoneNumber: currentBrand.value?.phone_number || "",
  brandPetFocus: currentBrand.value?.brand_pet_focus || "",
  profileImage: null
})

// 파일 업로드
const handleFileUpload = (e) => {
  form.value.profileImage = e.target.files[0]
}

// 저장
const handleSave = () => {
  const target = brands.value.find(b => b.id === props.brandId)

  if (target) {
    target.name = form.value.name
    target.email = form.value.email
    target.phone_number = form.value.phoneNumber
    target.brand_pet_focus = form.value.brandPetFocus
  }

  alert("저장되었습니다.")
  router.push({
    name: "brand-settings",
    params: { brand_id: props.brandId }
  })
}
</script>


<style scoped>
.settings-container {
  max-width: 480px;
  margin: 130px auto;
  padding: 0 10px;
  font-family: 'Pretendard', sans-serif;
}

.form-group {
  margin-bottom: 35px;
}

.form-group label:not(.file-btn) {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
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
}

/* 공통 input 스타일 */
input {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
  box-sizing: border-box;
}

.image-box {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
}

.image-box p {
  margin: 0;
  font-size: 14px;
  color: #555;
  flex: 1;  /* 추가: 텍스트 영역이 남은 공간 차지 */
}

.file-btn {
  background: #eee;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  white-space: nowrap;
  flex-shrink: 0;
  display: inline-block;
}

.file-btn input {
  display: none;
}

/* SAVE 버튼 */
.save-btn {
  display: block;
  width: 60%;
  padding: 16px;
  margin: 80px auto;
  background: #3A3A3A;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  border: none;
  cursor: pointer;
}
</style>
