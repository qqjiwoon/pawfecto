import axios from "axios"

const instance = axios.create({
  baseURL: "http://127.0.0.1:8000",  // Django API 주소로 변경
  withCredentials: true
})

export default instance
