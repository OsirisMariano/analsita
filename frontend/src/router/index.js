import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CamerasView from '../views/CamerasView.vue'
import ValidacaoArquivosView from '../views/ValidacaoArquivosView.vue'

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
    },
    {
      path: '/validacao-arquivos',
      name: 'validacao-arquivos',
      component: ValidacaoArquivosView
    }

  ],
})

export default router