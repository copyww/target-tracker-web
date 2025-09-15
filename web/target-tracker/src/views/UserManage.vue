<template>
  <el-card>
    <h2>用户管理</h2>
    <el-table :data="displayUsers" style="width: 100%">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="role" label="角色" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button
            size="mini"
            type="primary"
            @click="editUser(scope.row)"
            :disabled="role !== 'admin' && scope.row.username !== username"
          >
            编辑
          </el-button>
          <el-button
            size="mini"
            type="danger"
            @click="deleteUser(scope.row)"
            v-if="role === 'admin'"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const username = computed(() => store.getters['user/getUsername'])
const role = computed(() => store.getters['user/getRole'])

const allUsers = ref([
  { username: 'admin', role: 'admin' },
  { username: 'user1', role: 'user' },
  { username: 'user2', role: 'user' }
])

const displayUsers = computed(() => {
  return role.value === 'admin'
    ? allUsers.value
    : allUsers.value.filter(u => u.username === username.value)
})

const editUser = (user) => {
  ElMessage.info(`编辑用户: ${user.username}`)
}

const deleteUser = (user) => {
  ElMessage.warning(`删除用户: ${user.username}`)
}
</script>
