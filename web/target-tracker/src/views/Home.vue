<template>
  <div class="common-layout">
    <el-container>
      <!-- 顶部 Header -->
      <el-header class="header-bar">
        <div class="header-left">
          <span class="app-title">目标追踪</span>
        </div>
        <div class="header-right">
          <span>欢迎, {{ username }}</span>
          <!-- 管理员显示用户管理按钮 -->
          <el-button
            v-if="role === 'admin'"
            type="primary"
            size="small"
            @click="goUserManage"
          >
            用户管理
          </el-button>
          <!-- 普通用户显示个人管理按钮 -->
          <el-button
            v-if="role === 'user'"
            type="primary"
            size="small"
            @click="goSelfManage"
          >
            我的信息
          </el-button>
          <el-button type="danger" size="small" @click="logout">退出</el-button>
        </div>
      </el-header>

      <!-- 主体视频内容 -->
      <el-main>
        <div class="app-container flex">
          <videoShower class="flex-1" />
          <VideoSidebar class="w-1/3" />
        </div>
      </el-main>

      <!-- 底部操作 -->
      <el-footer>
        <FixedBottomActions />
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import videoShower from '@/components/videoShower.vue'
import VideoSidebar from '@/components/VideoSidebar.vue'
import FixedBottomActions from '@/components/FixedBottomActions.vue'

const store = useStore()
const router = useRouter()

const username = computed(() => store.getters['user/getUsername'] || JSON.parse(localStorage.getItem('user') || '{}').username)
const role = computed(() => store.getters['user/getRole'] || JSON.parse(localStorage.getItem('user') || '{}').role)


// 管理员跳转用户管理
const goUserManage = () => router.push('/user-manage')

// 普通用户跳转自我管理
const goSelfManage = () => {
  router.push('/self-manage')
}
// 退出登录
const logout = () => {
  store.commit('user/setLoggedIn', false)
  store.commit('user/setUsername','')
  store.commit('user/setRole','')
  store.commit('user/setUserId', null)
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
/* 顶部 Header 美化 */
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  padding: 0 30px;
  background: linear-gradient(90deg, #409eff, #66b1ff);
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  border-bottom-left-radius: 6px;
  border-bottom-right-radius: 6px;
}

/* 左侧标题 */
.header-left .app-title {
  font-size: 22px;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

/* 右侧按钮和欢迎语 */
.header-right {
  display: flex;
  align-items: center;
}

.header-right span {
  margin-right: 15px;
  font-weight: 500;
}

/* 按钮样式优化 */
.header-right .el-button {
  margin-left: 8px;
  border-radius: 20px;
  font-size: 14px;
  padding: 5px 15px;
}

.header-right .el-button[type="primary"][v-if="role === 'user']"] {
  background-color: #67c23a;
  border-color: #67c23a;
  color: #fff;
}

.header-right .el-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  transition: all 0.2s;
}

/* 主体容器 */
.app-container {
  display: flex;
  height: 100%;
  width: 100%;
  padding: 15px;
  background-color: #f0f2f5;
}

/* 底部 footer */
.el-footer {
  background-color: #fff;
  border-top: 1px solid #e0e0e0;
  height: 60px;
  line-height: 60px;
  text-align: center;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}

/* 视频侧边栏 */
.VideoSidebar {
  padding-left: 15px;
}
</style>
