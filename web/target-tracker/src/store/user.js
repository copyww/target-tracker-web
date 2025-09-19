import { createStore } from 'vuex'

export default {
  namespaced: true,
  state: {
    loggedIn: false,
    userId: null,
    username: '',
    role: '',
    coins: 0,
  },
  mutations: {
    setLoggedIn(state,status){ state.loggedIn=status },
    setUserId(state,id){ state.userId=id },
    setUsername(state,username){ state.username=username },
    setRole(state,role){ state.role=role },
    setEmail(state,email){ state.email=email },
    setCoins(state, coins) {
    state.coins = coins
  },
  },
  getters:{
    isLoggedIn: state => state.loggedIn,
    getUserId: state => state.userId,
    getUsername: state => state.username,
    getCoins: (state) => state.coins,
    getRole: state => state.role,
    getEmail: state => state.email
  }
}
