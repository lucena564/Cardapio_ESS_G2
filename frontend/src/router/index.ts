import { createRouter, createWebHistory } from 'vue-router'
import Mesa from '@/views/Mesa.vue'
import CardapioView from '@/views/CardapioView.vue'
import AdminView from '@/views/adminView.vue'

const routes = [
  {
    path: '/',
    name: 'Mesa',
    component: Mesa
  },
  {
    path: '/cardapio/:categoria',
    name: 'Cardapio',
    component: CardapioView
  },
  {
    path: '/historico',
    name: 'Historico',
    component: () => import('@/views/HistoricoView.vue')
  },
  {
    path: '/admin/items',
    name: 'AdminItems',
    component: AdminView
  },
  // Qualquer rota inválida redireciona para /
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
