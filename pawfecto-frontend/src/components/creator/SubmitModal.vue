<template>
  <div class="submit-modal-overlay">
    <div class="submit-modal-container">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2 class="modal-title">Campaign Submission</h2>

      <div class="modal-content">
        <div class="image-section">
          <img :src="defaultImg" alt="Campaign Image" class="submit-img" />
          <!-- <img :src="`http://localhost:8000/media/deliverables/${item.image}`" alt="Campaign Image" class="submit-img" /> -->

        </div>
        <div class="text-section">
          <h3 class="product-name">{{ item.campaign_acceptance.campaign.product_name }}</h3>
          <p class="product-description">{{ item.content }}</p>
        </div>
      </div>

      <a :href="item.post_url" target="_blank" class="submit-button">
        Instagram으로 제출하기
      </a>
    </div>
  </div>
</template>

<script setup>
import defaultImg from '@/assets/campaign1_test.jpg';

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.submit-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.submit-modal-container {
  background: white;
  padding: 40px;
  border-radius: 10px;
  max-width: 800px;
  width: 100%;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.submit-modal-container:hover {
  transform: scale(1.03);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  color: #333;
  cursor: pointer;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
}

.modal-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
  margin-bottom: 30px;
}

.image-section {
  flex: 1;
}

.submit-img {
  max-width: 200px;
  height: auto;
  border-radius: 8px;
}

.text-section {
  flex: 2;
  text-align: left;
}

.product-name {
  font-size: 22px;
  font-weight: 600;
  color: #444;
  margin-bottom: 10px;
}

.product-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.submit-button {
  display: inline-block;
  background-color: #4CAF50;
  color: white;
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 25px;
  text-decoration: none;
  text-align: center;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #45a049;
}

.submit-button:focus {
  outline: none;
}

.submit-button:active {
  background-color: #388e3c;
}
</style>
