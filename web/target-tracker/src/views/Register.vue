<template>
  <el-card class="register-card">
    <h2>注册账号</h2>
    <el-form :model="form" label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" v-model="form.password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
        <el-button @click="goLogin">返回登录</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = reactive({
  username: '',
  password: ''
})

const handleRegister = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('用户名和密码不能为空')
  }
  try {
    await axios.post('http://localhost:3000/api/register', form)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '注册失败')
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-card {
  width: 360px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
}
</style>
