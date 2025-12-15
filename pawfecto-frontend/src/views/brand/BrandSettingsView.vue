<template>
  <div>
    <BrandSettings :brandId="brandId" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import BrandSettings from "@/components/brand/BrandSettings.vue"

const route = useRoute()
const brandId = computed(() => Number(route.params.brand_id))
</script>
