<template>
  <div>
    <CreatorSettings :creatorId="creatorId" />
  </div>
</template>

<script setup>

import CreatorSettings from "@/components/creator/CreatorSettings.vue"

// const route = useRoute()
const props = defineProps({
  creatorId: {
    type: Number,
    required: true,
  },
})
</script>
