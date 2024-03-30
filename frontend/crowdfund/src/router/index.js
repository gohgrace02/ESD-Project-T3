import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import BackerHomeView from '../views/BackerHomeView.vue'
import ProjectView from '../views/ProjectView.vue'
import BackProjectView from '../views/BackProjectView.vue'
import CreatorHomeView from '@/views/CreatorHomeView.vue'
import CreateProjectView from '@/views/CreateProjectView.vue'
import CheckoutSuccessView from '@/views/CheckoutSuccessView.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/backer',
      name: 'backerhome',
      component: BackerHomeView
    },
    {
      path: '/project/:project_id',
      name: 'project',
      component: ProjectView
    },
    {
      path: '/project/:project_id/back',
      name: 'back',
      component: BackProjectView
    },
    {
      path: '/creator',
      name: 'creatorhome',
      component: CreatorHomeView
    },
    {
      path: '/creator/create',
      name: 'create',
      component: CreateProjectView
    },
    {
      path: '/success',
      name: 'checkoutsuccess',
      component: CheckoutSuccessView
    },
  ]
})

export default router
