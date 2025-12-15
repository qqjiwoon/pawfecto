<template>
  <div>
    <CreatorUpdateSettings :creatorId="creatorId" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import CreatorUpdateSettings from "@/components/creator/CreatorUpdateSettings.vue"

const route = useRoute()
const creatorId = computed(() => Number(route.params.creator_id))
</script>
