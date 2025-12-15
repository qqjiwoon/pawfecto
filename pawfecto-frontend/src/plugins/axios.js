import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
})

api.interceptors.request.use(config => {
  try {
    const access = localStorage.getItem("access")
    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }
  } catch (e) {
    // storage 접근 불가 컨텍스트에서는 그냥 통과
  }

  return config
})

export default api
