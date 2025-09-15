import { defineStore } from 'pinia'
import axios from 'axios'


export const useUserStore = defineStore('user', {
state: () => ({
token: '',
role: '', // 'admin' | 'user'
userInfo: {}
}),
getters: {
isAuthenticated: (state) => !!state.token
},
actions: {
async login(username, password) {
const res = await axios.post('/api/login', { username, password })
this.token = res.data.token
this.role = res.data.role
this.userInfo = res.data.user
axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
},
logout() {
this.token = ''
this.role = ''
this.userInfo = {}
delete axios.defaults.headers.common['Authorization']
}
}
})