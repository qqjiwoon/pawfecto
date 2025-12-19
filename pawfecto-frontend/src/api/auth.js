import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, logout as logoutApi } from '@/api/auth'
import api from '@/plugins/axios'

export const useAuthStore = defineStore('auth', () => {
  const me = ref(null) // 현재 로그인한 유저 정보

  // 1. 로그인
  const login = async (credentials) => {
    const res = await loginApi(credentials)
    const { access, refresh } = res.data
    
    // 토큰 저장
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    
    // 즉시 내 정보 가져오기
    await fetchMe()
  }

  // 2. 내 정보 조회
  const fetchMe = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      const res = await api.get('/accounts/me/')
      me.value = res.data
    } catch (err) {
      clearAuth()
    }
  }

  // 3. 로그아웃
  const logout = async () => {
    try {
      await logoutApi() // 백엔드 세션 종료 (선택 사항)
    } finally {
      clearAuth()
      window.location.href = '/login' // 메모리 및 잔상 완전 제거
    }
  }

  // 4. 인증 정보 초기화 내부 함수
  const clearAuth = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    me.value = null
    delete api.defaults.headers.common['Authorization']
  }

  return { me, login, fetchMe, logout }
})
