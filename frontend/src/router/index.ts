import { createRouter, createWebHistory } from 'vue-router'
import Categoria from '../components/Cardapio.vue'
import Mesa from '@/views/Mesa.vue'
const routes = [
  {
    path: '/',
    name: 'Mesa',
    component: Mesa,
  },
  {
    path: '/cardapio/:categoria',
    name: 'Categoria',
    component: Categoria
  },
  {
    path: '/',
    redirect: '/cardapio'
  },
  {
      path: "/historico",
      name: "historico",
      component: () => import("../views/HistoricoView.vue"),
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;
