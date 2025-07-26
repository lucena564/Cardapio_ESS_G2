import { createRouter, createWebHistory } from 'vue-router'
import Bebidas from '../views/Bebidas.vue'
import Pizzas from '../views/Pizzas.vue'
import Cardapio from '../views/Cardapio.vue'

const routes = [
  {
    path: '/cardapio/bebidas',
    name: 'Bebidas',
    component: Bebidas
  },
  {
    path: '/cardapio/pizzas',
    name: 'Pizzas',
    component: Pizzas
  },
  {
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
