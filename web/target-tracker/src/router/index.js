import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import UserManage from '@/views/UserManage.vue'
import { useUserStore } from '@/store/user'
import Dashboard from '@/views/Dashboard.vue'


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/users', component: UserManage }
]


const router = createRouter({
history: createWebHistory(),
routes
})


router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (!user && to.path !== '/login') {
    return next('/login')
  }
  next()
})

export default router