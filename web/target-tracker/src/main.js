import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vue3videoPlay from 'vue3-video-play'
import 'vue3-video-play/dist/style.css'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(vue3videoPlay)
app.mount('#app')
