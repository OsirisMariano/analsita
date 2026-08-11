import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CamerasView from '../views/CamerasView.vue'
import ValidacaoArquivosView from '../views/ValidacaoArquivosView.vue'
import ValidacaoDadosView from '../views/ValidacaoDadosView.vue'
import LeitorasView from '@/views/LeiturasView.vue'

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
    },
    {
      path: '/validacao-dados',
      name: 'validacao-dados',
      component: ValidacaoDadosView
    },
    { 
      path: '/leitoras', 
      name: 'leitoras', 
      component: LeitorasView 
    }
  ],
})

export default router