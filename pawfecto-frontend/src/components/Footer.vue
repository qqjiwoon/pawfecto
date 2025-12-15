<template>
    <footer class="pf-footer">
        <div class="pf-footer-left">
            <div class="pf-footer-logo">Pawfecto</div>
            <div class="pf-footer-address">
                212, Teheran-ro, Gangnam-gu,<br />
                Seoul, Republic of Korea
            </div>
        </div>

        <div class="pf-footer-right">
            <p>made by Pawfecto<br />
            email : pawfecto@gmail.com<br />
            Copyright 2025.Pawfecto.All Rights Reserved</p>
        </div>
    </footer>
</template>

<script setup>
</script>

<style scoped>
.pf-footer {
  /* max-width: 1200px; */
  margin: 0 auto;
  padding: 48px 32px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  background-color: #ffffff;
  border-top: 1px solid #eaeaea;
  position: relative;
}

.pf-footer-left {
  display: flex;
  flex-direction: column;
}

.pf-footer-logo {
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 28px;
  color: #000;
  margin-bottom: 12px;
}

.pf-footer-address {
  font-size: 14px;
  color: #9F9F9F;
  line-height: 1.6;
}

.pf-footer-right {
  color: #9F9F9F;
  font-size: 14px;
  line-height: 1.6;
}
</style>