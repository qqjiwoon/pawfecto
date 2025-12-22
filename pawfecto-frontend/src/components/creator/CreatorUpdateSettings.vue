<template>
  <div v-if="isLoaded" class="settings-container">

    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ form.loginId }}</p>
    </div>

    <div class="form-group">
      <label>비밀번호</label>
      <input 
        type="password" 
        class="input-field" 
        v-model="form.password" 
        placeholder="새 비밀번호 입력" 
      />
    </div>

    <div class="form-group">
      <label>비밀번호 확인</label>
      <input 
        type="password" 
        class="input-field" 
        v-model="form.passwordConfirm" 
        placeholder="비밀번호 재입력" 
      />
    </div>

    <div class="form-group">
      <label>이름</label>
      <input type="text" class="input-field" v-model="form.name" />
    </div>

    <div class="form-group">
      <label>이메일 주소</label>
      <input type="email" class="input-field" v-model="form.email" />
    </div>

    <div class="form-group">
      <label>전화번호</label>
      <input type="text" class="input-field" v-model="form.phoneNumber" />
    </div>

    <div class="form-group">
      <label>주소</label>
      <input type="text" class="input-field" v-model="form.address" />
    </div>

    <div class="form-group">
      <label>반려동물 종류</label>
      <select class="input-field" v-model="form.petType">
        <option value="dog">강아지</option>
        <option value="cat">고양이</option>
      </select>
    </div>

    <div class="form-group">
      <label>SNS 계정명</label>
      <input type="text" class="input-field" v-model="form.snsHandle" />
    </div>

    <div class="form-group">
      <label>SNS 계정 URL</label>
      <input type="text" class="input-field" v-model="form.snsUrl" />
    </div>

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

    <button class="update-btn" @click="updateProfile">저장</button>
  </div>
  
  <div v-else class="settings-container">
    <p>불러오는 중...</p>
  </div>
</template>

<script setup>
import api from "@/plugins/axios"
import { onMounted, ref } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useCreatorStore } from "@/stores/creator"
import { useWarningStore } from "@/stores/warning"

const route = useRoute()
const router = useRouter()
const creatorStore = useCreatorStore()
const warningStore = useWarningStore()

const isLoaded = ref(false)
const imageFile = ref(null)

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
  profile_image_url: "",
})

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
    profile_image_url: data.profile_image_url,
  })
  isLoaded.value = true
})

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    form.value.profile_image_url = URL.createObjectURL(file)
  }
}

const toggleTag = (tag) => {
  const idx = form.value.styleTags.indexOf(tag)
  if (idx === -1) form.value.styleTags.push(tag)
  else form.value.styleTags.splice(idx, 1)
}

/* 저장 (Brand 로직과 통일) */
const updateProfile = async () => {
  // 1. 비밀번호 일치 확인
  if (form.value.password && form.value.password !== form.value.passwordConfirm) {
    warningStore.open("비밀번호가 일치하지 않습니다.")
    return
  }

  // 2. 저장 의사 확인
  const isConfirmed = await warningStore.confirm("변경사항을 저장하시겠습니까?")
  if (!isConfirmed) return

  // 3. FormData 생성 (이미지 처리를 위해)
  const formData = new FormData()
  formData.append("name", form.value.name)
  formData.append("email", form.value.email)
  formData.append("phone_number", form.value.phoneNumber)
  formData.append("address", form.value.address)
  formData.append("pet_type", form.value.petType)
  formData.append("sns_handle", form.value.snsHandle)
  formData.append("sns_url", form.value.snsUrl)
  
  // 스타일 태그 전송
  form.value.styleTags.forEach(tag => {
    formData.append("style_tag_codes", tag)
  })

  if (imageFile.value) {
    formData.append("profile_image", imageFile.value)
  }
  if (form.value.password) {
    formData.append("password", form.value.password)
  }

  try {
    await api.put("/accounts/me/", formData)

    // 4. 성공 처리 (V표시 모달)
    await warningStore.open("정보가 성공적으로 수정되었습니다.", true)

    creatorStore.isLoaded = false
    await creatorStore.loadCreator()
    
    router.push({
      name: "creator-settings",
      params: { creator_id: Number(route.params.creator_id) },
    })
  } catch (err) {
    const errorMsg = err.response?.data?.error || "정보 수정에 실패했습니다."
    warningStore.open(errorMsg, false)
  }
}
</script>

<style scoped>
/* Brand와 동일한 레이아웃 유지 */
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

/* 입력 필드 통일 */
.input-field {
  width: 100%;
  height: 46px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  background: #fff;
}

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

/* 스타일 태그 (Creator 전용) */
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
  transition: all 0.2s;
}
.tag-chip.selected {
  background-color: #65481F;
  border-color: #65481F;
  color: white;
}

/* 저장 버튼 통일 */
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

/* 파일 선택창 스타일 통일 */
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
</style>
