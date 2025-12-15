<template>
  <div>
    <CreatorSettings :creatorId="creatorId" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import CreatorSettings from "@/components/creator/CreatorSettings.vue"

const route = useRoute()
const creatorId = computed(() => Number(route.params.creator_id))
</script>
