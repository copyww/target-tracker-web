import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import Personal from '@/views/Personal.vue'


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/home', component: Home, meta: { requiresAuth: true } },
  { path: '/personal', component: Personal, meta: { requiresAuth: true } },
  {path: '/register',component: () => import('@/views/Register.vue')},
  { path: '/user-manage', component: () => import('@/views/UserManage.vue'), meta: { requiresAuth: true } },
  { path: '/self-manage', component: () => import('@/views/SelfManage.vue'), meta: { requiresAuth: true } },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：支持刷新保持登录
router.beforeEach((to, from, next) => {
  if(!store.getters['user/isLoggedIn']){
    const user = JSON.parse(localStorage.getItem('user'))
    if(user){
      store.commit('user/setUserId', user.id)
      store.commit('user/setUsername', user.username)
      store.commit('user/setRole', user.role)
      store.commit('user/setLoggedIn', true)
    }
  }

  if(to.meta.requiresAuth && !store.getters['user/isLoggedIn']){
    next('/login')
  } else {
    next()
  }
})

export default router
