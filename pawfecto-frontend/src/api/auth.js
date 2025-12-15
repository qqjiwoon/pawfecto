// src/api/auth.js
import api from "@/plugins/axios"

// 로그인
export function login(data) {
  return api.post("/accounts/login/", data)
}

// 로그아웃 (있다면)
export function logout() {
  return api.post("/accounts/logout/")
}
