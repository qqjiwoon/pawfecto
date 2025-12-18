import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 전역 스타일 파일 임포트
import '@/assets/css/global.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

