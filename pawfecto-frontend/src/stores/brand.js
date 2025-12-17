import { defineStore } from "pinia"
import api from "@/plugins/axios"

export const useBrandStore = defineStore("brand", {
  state: () => ({
    brand: null,
    isLoaded: false,
  }),

  actions: {
    async loadBrand() {
      if (this.isLoaded) return

      const res = await api.get("/accounts/me/")
      this.brand = res.data
      this.isLoaded = true
    },
  },
})
