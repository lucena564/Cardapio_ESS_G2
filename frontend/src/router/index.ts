import { createRouter, createWebHistory } from 'vue-router'
import Bebidas from '../views/Bebidas.vue'

const routes = [
  {
    // http://localhost:5173/cardapio
    path: '/cardapio/bebidas',
    name: 'Bebidas',
    component: Bebidas
  },
  {
    path: '/cardapio/pizzas',
    name: 'Pizzas',
    component: () => import('../views/Pizzas.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
