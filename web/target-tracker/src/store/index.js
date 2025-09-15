// import { createStore } from 'vuex'

// export default createStore({
//   state: {
//     username : 'user1',
//   },
//   getters: {
//     getUsername: state => state.username,
//   },
//   mutations: {
//     setUsername(state, newUsername) {
//       state.username = newUsername;
//     }
//   },
//   actions: {
//   },
//   modules: {
//   }
// })
// src/store/index.js
// src/store/user.js
// src/store/index.js
import { createStore } from 'vuex'
import user from './user'  // 引入 user 模块

export default createStore({
  modules: {
    user
  }
})
