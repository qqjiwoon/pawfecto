// src/stores/brand.js
import { ref } from "vue"
import api from "@/plugins/axios"

export const brand = ref(null)
export const isBrandLoaded = ref(false)

export const loadBrand = async () => {
  const res = await api.get("/accounts/me/")
  brand.value = res.data
  isBrandLoaded.value = true
}
