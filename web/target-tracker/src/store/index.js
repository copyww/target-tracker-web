import { createStore } from 'vuex'

export default createStore({
  state: {
    username : 'usr1',
  },
  getters: {
    getUsername: state => state.username,
  },
  mutations: {
    setUsername(state, newUsername) {
      state.username = newUsername;
    }
  },
  actions: {
  },
  modules: {
  }
})
