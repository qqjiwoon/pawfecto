<template>
    <header class="pf-header">
      <!-- <div class="pf-container"> -->
        <nav class="pf-left-menu">
            <router-link to="/brand">Brand</router-link>
            <router-link to="/creator">Creator</router-link>
            <router-link to="/dashboard">Dashboard</router-link>
        </nav>
      

        <router-link to="/" class="pf-logo">
            Pawfecto
        </router-link>


        <nav class="pf-right=menu">
            <router-link to="/login">Login</router-link>
        </nav>
      <!-- </div> -->
    </header>
</template>

<script setup>
</script>

<style scoped>
.pf-header {
  /* max-width: 1200px; */
  height: 70px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  /* border-bottom: 1px solid #f2f2f2; */
  position: relative;
}

.pf-left-menu,
.pf-right-menu {
  display: flex;
  gap: 32px;
}

.pf-left-menu a,
.pf-right-menu a {
  font-size: 16px; 
  color: #9F9F9F;
  text-decoration: none;
}

.pf-left-menu a:hover,
.pf-right-menu a:hover { 
  text-decoration: underline;
}

.pf-logo {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Rubik Bubbles', sans-serif;
  font-size: 28px;
  color: #000;
  text-decoration: none;
}

</style>