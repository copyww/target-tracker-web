import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vue3videoPlay from 'vue3-video-play'
import 'vue3-video-play/dist/style.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入图标
import { Upload } from '@element-plus/icons-vue'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(vue3videoPlay)
app.use(ElementPlus)
app.component('Upload', Upload)
app.mount('#app')
