import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import BackerHomeView from '../views/BackerHomeView.vue'
import ProjectView from '../views/ProjectView.vue'
import CreatorHomeView from '@/views/CreatorHomeView.vue'
import CreateProjectView from '@/views/CreateProjectView.vue'
import CheckoutSuccessView from '@/views/CheckoutSuccessView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/backer',
      name: 'backerhome',
      component: BackerHomeView
    },
     {
      path: '/creator',
      name: 'creatorhome',
      component: CreatorHomeView
    },
    {
      path: '/project/:project_id',
      name: 'project',
      component: ProjectView
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
