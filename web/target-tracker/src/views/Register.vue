<!-- <template>
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
</style> -->
<template>
  <el-card class="login-card">
    <h2>注册</h2>
    <el-form :model="form" label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="form.username" placeholder="请输入用户名"/>
      </el-form-item>

      <el-form-item label="密码">
        <el-input type="password" v-model="form.password" placeholder="请输入密码"/>
      </el-form-item>

      <el-form-item label="邮箱">
        <el-input v-model="form.email" placeholder="请输入邮箱"/>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="register" class="w-full">注册</el-button>
      </el-form-item>

      <!-- 返回登录 -->
      <el-form-item>
        <el-button type="text" class="w-full" @click="$router.push('/login')">已有账号？去登录</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  email: ''
})

async function register() {
  try {
    const res = await axios.post('http://localhost:3000/api/register', form)
    alert(res.data.message)
    router.push('/login')
  } catch (err) {
    alert(err.response?.data?.message || '注册失败')
  }
}
</script>

<style scoped>
.login-card {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
}
</style>
