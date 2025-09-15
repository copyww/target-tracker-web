<template>
  <el-card class="login-card">
    <h2>登录</h2>
    <el-form :model="form" label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" v-model="form.password" />
      </el-form-item>
      <el-form-item label="角色">
        <el-radio-group v-model="form.role">
          <el-radio label="admin">管理员</el-radio>
          <el-radio label="user">普通用户</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useStore()

const form = reactive({
  username: '',
  password: '',
  role: 'user'
})

const handleLogin = async () => {
  try {
    await store.dispatch('user/login', form)
    ElMessage.success('登录成功！')
    router.push('/home')
  } catch (err) {
    ElMessage.error(err.message)
  }
}
</script>

<style scoped>
.login-card {
  width: 360px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
}
</style>
