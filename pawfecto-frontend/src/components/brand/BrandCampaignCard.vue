<template>
  <div class="card" @click="goDetail">
    <img
      :src="campaignImageUrl"
      class="card-img"
      alt="campaign"
    />

    <div class="card-body">
      <h3 class="card-title">{{ campaign.product_name }}</h3>
      <p class="card-subtitle">{{ shortDescription }}</p>
      <p class="card-detail"> → </p>
    </div>
  </div>
</template>



<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  campaign: {
    type: Object,
    required: true
  },
  brandId: {
    type: Number,
    required: true
  }
})

const router = useRouter()

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://127.0.0.1:8000"

const campaignImageUrl = computed(() => {
  const url = props.campaign.product_image_url

  if (!url) return ""

  // 이미 절대경로면 그대로 사용
  if (url.startsWith("http")) {
    return url
  }

  // /media/... 인 경우 backend 주소 붙이기
  return `${API_BASE_URL}${url}`
})

const shortDescription = computed(() => {
  const text = props.campaign.product_description || ""
  return text.length > 50 ? text.slice(0, 50) + "..." : text
})

function goDetail() {
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
