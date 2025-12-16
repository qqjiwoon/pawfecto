<template>
  <div class="settings-container">

    <!-- 아이디 -->
    <div class="form-group">
      <label>아이디</label>
      <p class="readonly-field">{{ user.loginId }}</p>
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
      <p class="readonly-field">{{ user.phoneNumber }}</p>
    </div>

    <!-- 주소 -->
    <div class="form-group">
      <label>주소</label>
      <p class="readonly-field">{{ user.address }}</p>
    </div>

    <!-- 주력 동물 종류 -->
    <div class="form-group">
      <label>주력 동물 종류</label>
      <p class="readonly-field">{{ user.brandPetFocus }}</p>
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
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  brandId: Number
})

const router = useRouter()

// store에서 brand 찾기
const user = computed(() =>
  brands.value.find(b => b.id === props.brandId)
)

// UPDATE 이동
const goToUpdate = () => {
  router.push({
    name: "brand-settings-update",
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

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
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
</style>
