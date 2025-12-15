<template>
  <div>
    <BrandUpdateSettings :brandId="brandId" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import BrandUpdateSettings from "@/components/brand/BrandUpdateSettings.vue"

const route = useRoute()
const brandId = computed(() => Number(route.params.brand_id))
</script>
