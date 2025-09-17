<template>
  <div>
    <!-- 顶部导航 -->
    <el-header class="header-bar">
      <span class="app-title">视频管理系统</span>
      <div class="header-right">
        <el-button type="primary" size="small" @click="goHome">返回主页</el-button>
        <el-button type="danger" size="small" @click="logout">退出登录</el-button>
      </div>
    </el-header>

    <!-- 用户信息 -->
    <el-card class="user-card">
      <h2>我的信息</h2>
      <el-form>
        <el-form-item label="用户名">
          <el-input v-model="user.username" disabled/>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="user.password"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updatePassword">修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()

const user = reactive({
  id: store.getters['user/getUserId'],
  username: store.getters['user/getUsername'],
  password: ''
})

// 获取用户密码
onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:3000/api/users')
    const me = res.data.find(u => u.id === user.id)
    if(me) user.password = me.password
  } catch(err) {
    ElMessage.error('加载失败')
  }
})

const updatePassword = async () => {
  try {
    await axios.put(`http://localhost:3000/api/users/${user.id}/password`, { password: user.password })
    ElMessage.success('修改成功')
  } catch(err) {
    ElMessage.error('修改失败')
  }
}

const goHome = () => {
  router.push('/home')
}

const logout = () => {
  store.commit('user/setLoggedIn', false)
  store.commit('user/setUsername', '')
  store.commit('user/setRole', '')
  store.commit('user/setUserId', null)
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  padding: 10px 20px;
  background: #409eff;
  color: #fff;
  align-items: center;
}

.header-right .el-button {
  margin-left: 8px;
}

.user-card {
  width: 400px;
  margin: 50px auto;
  padding: 20px;
}
</style>
