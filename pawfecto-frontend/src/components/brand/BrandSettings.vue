<template>
  <div class="settings-container" v-if="user">

    <!-- 아이디 -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ user.username }}</p>
    </div>

    <!-- 브랜드명 -->
    <div class="form-group">
      <label>브랜드명</label>
      <p class="readonly-field">{{ user.name }}</p>
    </div>

    <!-- 이메일 주소 -->
    <div class="form-group">
      <label>이메일 주소</label>
      <p class="readonly-field">{{ user.email }}</p>
    </div>

    <!-- 전화번호 -->
    <div class="form-group">
      <label>전화번호</label>
      <p class="readonly-field">{{ user.phone_number }}</p>
    </div>

    <!-- 주력 동물 종류 -->
    <div class="form-group">
      <label>주력 동물 종류</label>
      <p class="readonly-field">{{ user.pet_type }}</p>
    </div>

    <!-- 프로필 이미지 -->
    <div class="form-group">
      <label>프로필 이미지</label>
      <p class="readonly-field">
        {{ user.profile_image_url || "등록된 이미지 없음" }}
      </p>
    </div>

    <!-- 설정 수정 버튼 -->
    <button class="update-btn" @click="goToUpdate">
      수정
    </button>

  </div>

  <div v-else class="not-found">
    <p>브랜드 정보를 찾을 수 없습니다.</p>
  </div>
</template>



<script setup>
// 브랜드 설정 조회 (store 통일)
import { onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { useBrandStore } from "@/stores/brand"

const router = useRouter()
const brandStore = useBrandStore()

// 브랜드 정보
const user = computed(() => brandStore.brand)

// 최초 로드
onMounted(async () => {
  await brandStore.loadBrand()
})

// 수정 페이지 이동
const goToUpdate = () => {
  router.push({ name: "brand-settings-update" })
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

/* 읽기 전용 필드 */
.readonly-field {
  width: 100%;
  min-height: 46px;
  padding: 0 12px;

  display: flex;
  align-items: center;

  background: #f5f5f5;
  border-radius: 8px;
  color: #555;
  font-size: 14px;
  box-sizing: border-box;

  /* 긴 URL 대응 핵심 설정 */
  word-break: break-all; /* 영문/기호가 공백 없이 길어도 강제로 줄바꿈 */
  line-height: 1.5;      /* 줄 간격 조절로 가독성 향상 */
  white-space: pre-wrap; /* 공백 및 줄바꿈 유지 (필요 시) */
}

/* 수정 버튼 */
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
