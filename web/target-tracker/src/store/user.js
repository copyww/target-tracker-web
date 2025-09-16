import { createStore } from 'vuex'

export default {
  namespaced: true,
  state: {
    loggedIn: false,
    userId: null,
    username: '',
    role: ''
  },
  mutations: {
    setLoggedIn(state,status){ state.loggedIn=status },
    setUserId(state,id){ state.userId=id },
    setUsername(state,username){ state.username=username },
    setRole(state,role){ state.role=role },
  },
  getters:{
    isLoggedIn: state => state.loggedIn,
    getUserId: state => state.userId,
    getUsername: state => state.username,
    getRole: state => state.role
  }
}
