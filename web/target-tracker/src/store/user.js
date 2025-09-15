import { createStore } from 'vuex'

export default {
  namespaced: true,
  state: () => ({
    username: '',
    role: '',
    loggedIn: false,
  }),
  getters: {
    getUsername: state => state.username,
    getRole: state => state.role,
    isLoggedIn: state => state.loggedIn,
  },
  mutations: {
    setUsername(state, username) {
      state.username = username
    },
    setRole(state, role) {
      state.role = role
    },
    setLoggedIn(state, value) {
      state.loggedIn = value
    },
  },
  actions: {
    login({ commit }, { username, password, role }) {
      return new Promise((resolve, reject) => {
        // 模拟账号验证
        const validAccounts = {
          admin: { password: '123456', role: 'admin' },
          user1: { password: '123456', role: 'user' },
          user2: { password: '123456', role: 'user' },
        }
        const account = validAccounts[username]
        if (account && account.password === password && account.role === role) {
          commit('setUsername', username)
          commit('setRole', role)
          commit('setLoggedIn', true)
          resolve()
        } else {
          reject(new Error('账号或密码错误'))
        }
      })
    },
    logout({ commit }) {
      commit('setUsername', '')
      commit('setRole', '')
      commit('setLoggedIn', false)
    }
  }
}
