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
  const REDIRECT_URI = 'https://localhost:5173/callback/instagram';
  
  // ⭐ 핵심: query string의 code + hash의 #_ 조합
  let code = route.query.code;
  const hash = window.location.hash; // "#_" 가져오기
  
  console.log('🔗 [3단계] 토큰 교환 시 Redirect URI:', REDIRECT_URI);
  console.log('현재 전체 URL:', window.location.href);
  console.log('📝 Query에서 받은 코드:', code);
  console.log('📝 Hash 값:', hash);
  
  if (!code) {
    alert('인증 코드가 없습니다.');
    router.push('/');
    return;
  }

  // hash가 있으면 코드에 붙이기
  if (hash) {
    code = code + hash;
    console.log('📝 최종 코드 (hash 포함):', code);
  }

  try {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      alert('로그인이 필요합니다.');
      router.push('/login');
      return;
    }

    const requestData = { 
      code: code,  // hash가 포함된 code
      redirect_uri: REDIRECT_URI
    };

    console.log('📤 백엔드로 전송할 데이터:', requestData);

    const response = await axios.post(
      'https://localhost:8000/api/instagram/update/', 
      requestData,
      { 
        headers: { 
          Authorization: `Bearer ${token}` 
        } 
      }
    );
    
    console.log('✅ 연동 성공:', response.data);
    alert('인스타그램 연동이 완료되었습니다!');

    // 성공 후 대시보드로 이동
    if (response.data.internal_id) {
      router.push(`/dashboard/creator/${response.data.internal_id}`);
    } else {
      router.push('/dashboard');
    }

  } catch (error) {
    console.error('❌ 연동 실패:', error);
    
    // 에러 상세 정보 표시
    if (error.response) {
      const errorData = error.response.data;
      console.error('에러 상세:', errorData);
      console.error('에러 status:', error.response.status);
      console.error('전체 response:', error.response);
      
      const errorMsg = errorData?.details?.error_message || 
                       errorData?.details || 
                       errorData?.error || 
                       '알 수 없는 오류';
      
      alert(`연동 실패: ${errorMsg}`);
    } else if (error.request) {
      console.error('서버 응답 없음:', error.request);
      alert('서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인하세요.');
    } else {
      console.error('요청 생성 오류:', error.message);
      alert('요청 생성 중 오류가 발생했습니다.');
    }
    
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