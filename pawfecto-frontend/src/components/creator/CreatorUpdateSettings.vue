<template>
  <div v-if="isLoaded" class="settings-container">

    <!-- 아이디 (읽기 전용) -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ form.loginId }}</p>
    </div>

    <!-- 비밀번호 -->
    <div class="form-group">
      <label>비밀번호</label>
      <input type="password" v-model="form.password" placeholder="새 비밀번호 입력" />
    </div>

    <!-- 비밀번호 확인 -->
    <div class="form-group">
      <label>비밀번호 확인</label>
      <input type="password" v-model="form.passwordConfirm" placeholder="비밀번호 재입력" />
    </div>

    <!-- 이름 -->
    <div class="form-group">
      <label>이름</label>
      <input type="text" v-model="form.name" />
    </div>

    <!-- 이메일 -->
    <div class="form-group">
      <label>이메일 주소</label>
      <input type="email" v-model="form.email" />
    </div>

    <!-- 전화번호 -->
    <div class="form-group">
      <label>전화번호</label>
      <input type="text" v-model="form.phoneNumber" />
    </div>

    <!-- 주소 -->
    <div class="form-group">
      <label>주소</label>
      <input type="text" v-model="form.address" />
    </div>

    <!-- 반려동물 종류 -->
    <div class="form-group">
      <label>반려동물 종류</label>
      <select v-model="form.petType">
        <option value="dog">강아지</option>
        <option value="cat">고양이</option>
      </select>
    </div>

    <!-- SNS 계정명 -->
    <div class="form-group">
      <label>SNS 계정명</label>
      <input type="text" v-model="form.snsHandle" />
    </div>

    <!-- SNS URL -->
    <div class="form-group">
      <label>SNS 계정 URL</label>
      <input type="text" v-model="form.snsUrl" />
    </div>

    <!-- SNS 스타일 -->
    <div class="form-group">
      <label>SNS 스타일</label>

      <div class="tag-options">
        <span
          v-for="tag in styleOptions"
          :key="tag.value"
          class="tag-chip"
          :class="{ selected: form.styleTags.includes(tag.value) }"
          @click="toggleTag(tag.value)"
        >
          # {{ tag.label }}
        </span>
      </div>
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

    <!-- 저장 버튼 -->
    <button class="save-btn" @click="handleSave">SAVE</button>
  </div>
  <div v-else class="settings-container">
    <p>불러오는 중...</p>
  </div>

  <div v-if="showToast" class="toast">
    {{ toastMessage }}
  </div>

</template>

<script setup>
import api from "@/plugins/axios"
import { onMounted, ref } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useCreatorStore } from "@/stores/creator"

const router = useRouter()
const route = useRoute()

const creatorStore = useCreatorStore()
const isLoaded = ref(false)

// 스타일 옵션
const styleOptions = [
  { value: "energetic", label: "활발한" },
  { value: "calm", label: "차분한" },
  { value: "funny", label: "웃긴" },
  { value: "wholesome", label: "힐링되는" },
  { value: "cozy", label: "포근한" },
  { value: "heartfelt", label: "감동적인" },
  { value: "aesthetic", label: "감각적인" },
  { value: "minimal", label: "깔끔한" },
  { value: "outdoor", label: "야외감성" },
  { value: "no_preference", label: "상관없음" },
]


const form = ref({
  loginId: "",
  password: "",
  passwordConfirm: "",
  name: "",
  email: "",
  phoneNumber: "",
  address: "",
  petType: "dog",
  snsHandle: "",
  snsUrl: "",
  styleTags: [],
})

/* 최초 로드 */
onMounted(async () => {
  await creatorStore.loadCreator()

  const data = creatorStore.creator
  if (!data) return

  Object.assign(form.value, {
    loginId: data.username,
    name: data.name,
    email: data.email,
    phoneNumber: data.phone_number,
    address: data.address,
    petType: data.pet_type,
    snsHandle: data.sns_handle,
    snsUrl: data.sns_url,
    styleTags: data.style_tags.map(t => t.code),
  })

  isLoaded.value = true
})

/* 스타일 토글 */
const toggleTag = (tag) => {
  const idx = form.value.styleTags.indexOf(tag)
  if (idx === -1) form.value.styleTags.push(tag)
  else form.value.styleTags.splice(idx, 1)
}

/* 저장 */
const toastMessage = ref('')
const showToast = ref(false)

const openToast = (message) => {
  toastMessage.value = message
  showToast.value = true

  remindTimeout && clearTimeout(remindTimeout)
  remindTimeout = setTimeout(() => {
    showToast.value = false
  }, 2500)
}

let remindTimeout = null

const handleSave = async () => {
  console.log("styleTags payload:", form.value.styleTags)
  if (form.value.password && form.value.password !== form.value.passwordConfirm) {
    alert("비밀번호가 일치하지 않습니다.")
    return
  }

  const payload = {
    name: form.value.name,
    email: form.value.email,
    phone_number: form.value.phoneNumber,
    address: form.value.address,
    pet_type: form.value.petType,
    sns_handle: form.value.snsHandle,
    sns_url: form.value.snsUrl,
    style_tag_codes: form.value.styleTags,
  }

  if (form.value.password) {
    payload.password = form.value.password
  }

  await api.put("/accounts/me/", payload)

  // 👉 수정 후 store 갱신
  creatorStore.isLoaded = false
  await creatorStore.loadCreator()
  openToast("정보가 성공적으로 수정되었습니다.")

  setTimeout(() => {
    router.push({
      name: "creator-settings",
      params: { creator_id: Number(route.params.creator_id) },
    })
  }, 1500)
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

/* 공통 input 스타일 */
input,
.form-group select {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
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
  margin: 0;
}

/* 태그 영역 */
.tag-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-chip {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: #fafafa;
  cursor: pointer;
  font-size: 13px;
}

/* 선택된 스타일 태그 */
.tag-chip.selected {
  background-color: #65481F;
  border-color: #65481F;
  color: white;
}

/* 파일 업로드 박스 */
.image-box {
  width: 100%;
  height: 46px;
  padding: 0 12px;  /* 10px → 12px로 변경 */
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
  background: #3A3A3A;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  margin: 80px auto 80px;
}

.save-btn:hover {
  background: #3A3A3A;
}
.toast {
  position: fixed;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  background: #3A3A3A;
  color: white;
  padding: 12px 24px;
  border-radius: 24px;
  font-size: 14px;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

</style>