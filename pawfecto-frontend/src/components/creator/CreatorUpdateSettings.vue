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
          #{{ tag.label }}
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
</template>


<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  creatorId: Number
})

const router = useRouter()

// store에서 creator 찾기
const currentCreator = computed(() =>
  creators.value.find(c => c.id === props.creatorId)
)

// 폼 초기값 설정
const form = ref({
  loginId: currentCreator.value?.username || "",
  password: "",
  passwordConfirm: "",
  name: currentCreator.value?.name || "",
  email: currentCreator.value?.email || "",
  phoneNumber: currentCreator.value?.phone_number || "",
  address: currentCreator.value?.address || "",
  petType: currentCreator.value?.pet_type || "dog",
  snsHandle: currentCreator.value?.sns_handle || "",
  snsUrl: currentCreator.value?.sns_url || "",
  styleTags: currentCreator.value?.style_tags
    ? [...currentCreator.value.style_tags]
    : [],
  profileImage: null
})

// 스타일 옵션 그대로
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
  { value: "no_preference", label: "상관없음" }
]

// 태그 선택/해제
const toggleTag = (tagValue) => {
  const idx = form.value.styleTags.indexOf(tagValue)
  if (idx === -1) form.value.styleTags.push(tagValue)
  else form.value.styleTags.splice(idx, 1)
}

// 파일 업로드
const handleFileUpload = (e) => {
  form.value.profileImage = e.target.files[0]
}

// 저장
const handleSave = () => {
  const target = creators.value.find(c => c.id === props.creatorId)
  if (target) {
    target.name = form.value.name
    target.email = form.value.email
    target.phone_number = form.value.phoneNumber
    target.address = form.value.address
    target.pet_type = form.value.petType
    target.sns_handle = form.value.snsHandle
    target.sns_url = form.value.snsUrl
    target.style_tags = [...form.value.styleTags]
  }

  alert("저장되었습니다.")
  router.push({
    name: "creator-settings",
    params: { creator_id: props.creatorId }
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
</style>