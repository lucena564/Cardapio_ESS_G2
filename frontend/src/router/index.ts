import { createRouter, createWebHistory } from 'vue-router'
import Cardapio from '../views/Cardapio.vue'

const routes = [
  {
    // http://localhost:5173/cardapio
    path: '/cardapio',
    name: 'Cardapio',
    component: Cardapio
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
