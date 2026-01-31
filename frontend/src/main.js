import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css' // O Tailwind v4 deve estar aqui dentro

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')