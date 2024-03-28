import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomeView from '../views/HomeView.vue'
import ProjectView from '../views/ProjectView.vue'
import BackProjectView from '../views/BackProjectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
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
  ]
})

export default router
