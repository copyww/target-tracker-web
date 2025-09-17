<template>
  <el-card class="login-card">
    <h2>登录</h2>
    <el-form :model="form" label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="form.username"/>
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" v-model="form.password"/>
      </el-form-item>
      <el-form-item label="角色">
        <el-radio-group v-model="form.role">
          <el-radio label="admin">管理员</el-radio>
          <el-radio label="user">普通用户</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
        <el-button @click="goRegister">注册</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useStore()

const form = reactive({ username:'', password:'', role:'user' })

const handleLogin = async ()=>{
  try{
    const res = await axios.post('http://localhost:3000/api/login', form)
    const user = res.data.user
    if(user.role !== form.role) return ElMessage.error('角色选择不匹配')

    store.commit('user/setLoggedIn', true)
    store.commit('user/setUserId', user.id)
    store.commit('user/setUsername', user.username)
    store.commit('user/setRole', user.role)

    localStorage.setItem('user', JSON.stringify(user))
    ElMessage.success('登录成功')
    router.push('/home')
  }catch(err){
    ElMessage.error(err.response?.data?.message || '登录失败')
  }
}

const goRegister = ()=>{ router.push('/register') }
</script>

<style scoped>
.login-card { width:360px; margin:100px auto; padding:20px; text-align:center; }
</style>
