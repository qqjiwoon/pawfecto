<template>
  <div class="settings-container">

    <!-- 아이디 -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ user.username }}</p>
    </div>

    <!-- 이름 -->
    <div class="form-group">
      <label>이름</label>
      <p class="readonly-field">{{ user.name }}</p>
    </div>

    <!-- 이메일 -->
    <div class="form-group">
      <label>이메일 주소</label>
      <p class="readonly-field">{{ user.email }}</p>
    </div>

    <!-- 전화번호 -->
    <div class="form-group">
      <label>전화번호</label>
      <p class="readonly-field">{{ user.phone_number }}</p>
    </div>

    <!-- 주소 -->
    <div class="form-group">
      <label>주소</label>
      <p class="readonly-field">{{ user.address }}</p>
    </div>

    <!-- 반려동물 종류 -->
    <div class="form-group">
      <label>반려동물 종류</label>
      <p class="readonly-field">
        {{ user.pet_type === 'dog' ? '강아지' : '고양이' }}
      </p>
    </div>

    <!-- SNS 계정명 -->
    <div class="form-group">
      <label>SNS 계정명</label>
      <p class="readonly-field">{{ user.sns_handle }}</p>
    </div>

    <!-- SNS URL -->
    <div class="form-group">
      <label>SNS 계정 URL</label>
      <p class="readonly-field">{{ user.sns_url }}</p>
    </div>

    <!-- SNS 스타일 -->
    <div class="form-group">
      <label>SNS 스타일</label>
      <div class="tag-options readonly-tags">
        <span
          v-for="tag in styleOptions"
          :key="tag.value"
          class="tag-chip"
          :class="{ selected: user.style_tags.includes(tag.value) }"
        >
          #{{ tag.label }}
        </span>
      </div>
    </div>

    <!-- 프로필 이미지 -->
    <div class="form-group">
      <label>프로필 이미지</label>
      <p class="readonly-field">
        {{ user.profileImageName || '등록된 이미지 없음' }}
      </p>
    </div>

    <!-- UPDATE 버튼 -->
    <button class="update-btn" @click="goToUpdate">
      UPDATE
    </button>

  </div>
</template>


<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  creatorId: Number
})

const router = useRouter()

// store에서 creator 찾기
const user = computed(() =>
  creators.value.find(c => c.id === props.creatorId)
)

// UPDATE 이동
const goToUpdate = () => {
  router.push({
    name: "creator-settings-update",
    params: { creator_id: props.creatorId }
  })
}

// 스타일 옵션 그대로 유지
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

.form-group label {
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
  font-size: 13px;
}

/* 선택된 스타일 태그 */
.tag-chip.selected {
  background-color: #65481F;
  border-color: #65481F;
  color: white;
}

/* 조회 페이지에서는 클릭 못하도록 */
.readonly-tags .tag-chip {
  cursor: default;
}

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
  margin: 80px auto 80px;
}

.update-btn:hover {
  background: #3A3A3A;
}

</style>
