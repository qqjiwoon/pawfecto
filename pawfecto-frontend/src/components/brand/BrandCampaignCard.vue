<template>
  <div class="card" @click="goDetail">
    <img :src="campaign.product_image_url" class="card-img" alt="campaign">

    <div class="card-body">
      <h3 class="card-title">{{ campaign.product_name }}</h3>
      <p class="card-subtitle">{{ shortDescription }}</p>
      <p class="card-detail"> → </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  campaign: Object,
  brandId: Number
})

const router = useRouter()

const shortDescription = computed(() => {
  if (!props.campaign.product_description) return ""
  const text = props.campaign.product_description
  return text.length > 50 ? text.slice(0, 50) + "..." : text
})

function goDetail() {
  console.log("brandId:", props.brandId)
  console.log("campaign_id:", props.campaign.campaign_id)

  router.push({
    name: "campaign-recommendations",
    params: {
      brand_id: props.brandId,
      campaign_id: props.campaign.campaign_id,
    }
  })
}
</script>


<style scoped>
.card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: 0.2s;
  position: relative; 
}

.card:hover {
  transform: translateY(-3px);
}

.card-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.card-body {
  padding: 14px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
}

.card-subtitle {
  font-size: 13px;
  margin-top: 5px;
  color: #333;
}

.card-detail {
  position: absolute;
  bottom: 10px;
  right: 10px;    
  font-size: 18px;
  color: #333;
  cursor: pointer;
}
</style>
