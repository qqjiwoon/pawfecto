<template>
  <div class="loading-container">
    <p>인스타그램 정보를 연동 중입니다...</p>
    <div class="spinner"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const code = route.query.code;

  if (code) {
    try {
      // 인스타그램 버그 문자(#_) 제거 
      const cleanCode = code.replace(/#_$/, '');
      
      // [핵심] 로그인된 유저이므로 Header에 토큰 포함
      const token = localStorage.getItem('access_token'); // 저장된 JWT 토큰

      // 백엔드로 코드 전송
      const response = await axios.post(
        'https://localhost:8000/api/instagram/update/', // URL 확인 필요
        { code: cleanCode },
        {
          headers: {
            Authorization: `Bearer ${token}` // [중요] 이게 없으면 401 에러 남
          }
        }
      );

      console.log('연동 성공:', response.data);
      alert('인스타그램 연동이 완료되었습니다!');

      // 성공 후 대시보드나 프로필 설정 페이지로 이동
      // response에 username이 있다면 해당 경로로 이동 가능
      router.push(`/dashboard/creator/${response.data.username}`); 

    } catch (error) {
      console.error('연동 실패:', error.response?.data || error);
      alert('연동에 실패했습니다. 다시 시도해주세요.');
      router.push('/'); // 실패 시 홈으로
    }
  } else {
    // 코드가 없으면 잘못된 접근
    router.push('/');
  }
});
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.2rem;
}
/* 간단한 스피너 스타일 */
.spinner {
  margin-top: 20px;
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>