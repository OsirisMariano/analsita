import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CamerasView from '../views/CamerasView.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
  path: '/cameras',
  name: 'cameras',
  component: CamerasView
    }
  ],
})

export default router