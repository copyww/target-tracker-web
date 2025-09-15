import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import UserManage from '@/views/UserManage.vue'
import store from '@/store'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { 
    path: '/home', 
    component: Home,
    meta: { requiresAuth: true }
  },
  { 
    path: '/user-manage', 
    component: UserManage,
    meta: { requiresAuth: true }
  },
  {
  path: '/user-manage/:username?',
  name: 'UserManage',
  component: () => import('@/views/UserManage.vue'),
  meta: { requiresAuth: true }
}

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const loggedIn = store.getters['user/isLoggedIn']
  if (to.meta.requiresAuth && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
