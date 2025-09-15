<template>
<div>
<h2>用户管理</h2>
<el-table :data="users">
<el-table-column prop="username" label="用户名" />
<el-table-column prop="role" label="角色" />
<el-table-column v-if="isAdmin" label="操作">
<template #default="scope">
<el-button @click="editUser(scope.row)">编辑</el-button>
<el-button type="danger" @click="deleteUser(scope.row.id)">删除</el-button>
</template>
</el-table-column>
</el-table>
</div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/store/user'


const store = useUserStore()
const users = ref([])
onMounted(() => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (user.role !== 'admin') {
    alert('只有管理员可以查看此页面')
    router.push('/dashboard')
    return
  }

  // 假数据，后面接后端
  users.value = [
    { id: 1, username: 'admin' },
    { id: 2, username: 'user1' }
  ]
})
const isAdmin = computed(() => store.role === 'admin')


const fetchUsers = async () => {
const res = await axios.get('/api/users')
users.value = res.data
}


const deleteUser = async (id) => {
await axios.delete(`/api/users/${id}`)
fetchUsers()
}


onMounted(fetchUsers)
</script>