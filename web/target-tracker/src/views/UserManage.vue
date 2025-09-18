<template>
  <div>
    <!-- 顶部导航栏 -->
    <el-header class="header-bar">
      <span class="app-title">超级管理员</span>
      <div class="header-right">
        <span>欢迎, {{ username }}</span>
        <el-button type="primary" size="small" @click="goLogin">视频追踪</el-button>
        <el-button
          v-if="role==='admin'"
          type="success"
          size="small"
          @click="fetchUsers"
        >刷新用户列表</el-button>
        <el-button type="danger" size="small" @click="logout">退出登录</el-button>
      </div>
    </el-header>

    <!-- 用户表格 -->
    <el-main>
      <h2 v-if="role==='admin'">用户管理（管理员）</h2>
      <h2 v-else>我的信息（普通用户）</h2>

      <el-table :data="displayUsers" style="width:100%">
        <el-table-column prop="username" label="用户名"/>
        <el-table-column prop="role" label="角色"/>
        <el-table-column prop="password" label="密码"/>
        <el-table-column prop="email" label="邮箱"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editPassword(scope.row)">修改密码</el-button>
            <el-button size="small" @click="editEmail(scope.row)">修改邮箱</el-button>
            <el-button
              v-if="role==='admin'"
              :disabled="user.id === 3"
              size="small"
              type="danger"
              @click="deleteUser(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <!-- 修改密码弹窗（放在最外层） -->
    <el-dialog v-model="dialogVisible" title="修改密码">
      <el-input v-model="newPassword" placeholder="请输入新密码"/>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="confirmChange">确定</el-button>
      </span>
    </el-dialog>
        <el-dialog v-model="dialogVisible1" title="修改邮箱">
      <el-input v-model="newEmail" placeholder="请输入新邮箱"/>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible1=false">取消</el-button>
        <el-button type="primary" @click="confirmChange2">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import user from '@/store/user'

const store = useStore()
const router = useRouter()

const username = computed(()=>store.getters['user/getUsername'])
const role = computed(()=>store.getters['user/getRole'])
const userId = computed(()=>store.getters['user/getUserId'])
const email = computed(()=>store.getters['user/getEmail'])

const users = ref([])
const dialogVisible = ref(false)
const dialogVisible1 = ref(false)
const editUser = ref(null)
const newPassword = ref('')
const newEmail = ref('')

// 获取用户列表
const fetchUsers = async ()=>{
  try{
    if(role.value==='admin'){
      const res = await axios.get('http://localhost:3000/api/users')
      users.value = res.data
    } else {
      const res = await axios.get(`http://localhost:3000/api/users/${userId.value}`)
      users.value = [res.data]
    }
  }catch(err){
    ElMessage.error('获取用户失败')
  }
}

onMounted(fetchUsers)
const displayUsers = computed(()=>users.value)

// 修改密码
const editPassword = (user)=>{
  editUser.value = user
  newPassword.value = ''
  dialogVisible.value = true
}

const editEmail = (user)=>{
  editUser.value = user
  newEmail.value = ''
  dialogVisible1.value = true
}

const confirmChange = async ()=>{
  if(!newPassword.value) return ElMessage.warning('请输入新密码')
  try{
    await axios.put(`http://localhost:3000/api/users/${editUser.value.id}/password`, { password:newPassword.value })
    ElMessage.success('修改成功')
    dialogVisible.value = false
    fetchUsers()
  }catch(err){
    ElMessage.error(err.response?.data?.message || '修改失败')
  }
}
const confirmChange2 = async ()=>{
  if(!newEmail.value) return ElMessage.warning('请输入新邮箱')
  try{
    await axios.put(`http://localhost:3000/api/users/${editUser.value.id}/email`, { email:newEmail.value })
    ElMessage.success('修改成功')
    dialogVisible1.value = false
    fetchUsers()
  }catch(err){
    ElMessage.error(err.response?.data?.message || '修改失败')
  }
}


// 删除用户（管理员）
const deleteUser = async (user)=>{
  try{
    await axios.delete(`http://localhost:3000/api/users/${user.id}`)
    ElMessage.success('删除成功')
    fetchUsers()
  }catch(err){
    ElMessage.error(err.response?.data?.message || '删除失败')
  }
}

// 返回主页
const goLogin = ()=> router.push('/home')

// 退出登录 → 返回主页
const logout = () => {
  // 清空 Vuex 状态
  store.commit('user/logout')

  // 清空 localStorage
  localStorage.removeItem('user')

  // 退出后跳转到登录页
  router.push('/login')
}
</script>

<style scoped>
.header-bar {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:10px 20px;
  background:#409eff;
  color:#fff;
}
.header-right .el-button{ margin-left:10px; }
.app-title{ font-size:20px; font-weight:bold; }
</style>
