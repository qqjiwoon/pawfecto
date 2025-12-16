import { defineStore } from "pinia"
import api from "@/plugins/axios"

export const useCreatorStore = defineStore("creator", {
  state: () => ({
    creator: null,
    isLoaded: false,
  }),

  actions: {
    async loadCreator() {
      if (this.isLoaded) return

      const res = await api.get("/accounts/me/")
      this.creator = res.data
      this.isLoaded = true
    },
  },
})
