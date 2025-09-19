<template>
  <div class="personal-page">
    <div class="profile-card">
      <div class="avatar-container">
        <img :src="user.avatar" class="avatar" @click="changeAvatar" title="点击更换头像"/>
      </div>
      <h2 class="username">{{ user.username }}</h2>
      <p class="email">邮箱：{{ user.email || '未绑定' }}</p>
      <p class="coins">
        <span class="coin-icon">💰</span> {{ user.coins }}
      </p>

      <div class="actions">
        <button class="btn recharge" @click="recharge">充值金币</button>
        <button class="btn recharge" @click="home">目标追踪</button>
        <button class="btn logout" @click="logout">退出登录</button>
      </div>

      <input type="file" ref="fileInput" @change="uploadAvatar" style="display:none"/>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from "vue-router"; // ✅ 这里导入 useRouter
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'


const router = useRouter(); // ✅ 初始化 router 实例
const store = useStore()
const user = ref({ username:'', email:'', coins:0, avatar:'' })
const defaultAvatar = '/default-avatar.png'
const fileInput = ref(null)
const userId = store.getters['user/getUserId']
const home = () => router.push('/home')
onMounted(async ()=>{
  try{
    const res = await axios.get(`http://localhost:3000/api/personal/${userId}`)
    user.value = res.data
  }catch(err){
    ElMessage.error('加载个人信息失败')
  }
})

function changeAvatar(){ fileInput.value.click() }

async function uploadAvatar(e){
  const file = e.target.files[0]
  if(!file) return
  const form = new FormData()
  form.append('avatar', file)
  try{
    const res = await axios.post(`http://localhost:3000/api/personal/${userId}/avatar`, form, {
      headers: {'Content-Type':'multipart/form-data'}
    })
    user.value.avatar = res.data.avatar
    ElMessage.success('头像上传成功')
  }catch(err){
    ElMessage.error('头像上传失败')
  }
}

function recharge(){
  const amount = prompt('请输入充值金币数量')
  if(!amount) return
  axios.post(`http://localhost:3000/api/personal/${userId}/recharge`, { coins: Number(amount) })
    .then(()=> {
      user.value.coins += Number(amount)
      ElMessage.success('充值成功')
      store.commit('user/setCoins',user.value.coins)
      localStorage.setItem('user', JSON.stringify(user.value))
    }).catch(()=> ElMessage.error('充值失败'))
}

function logout(){
  store.commit('user/logout')
  localStorage.removeItem('user')
  window.location.href = '/login'
}


</script>

<style scoped>
.personal-page {
  /* background: url('/background.jpg') no-repeat center/cover; */
  min-height: 100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.profile-card{
  background: rgba(255,255,255,0.9);
  padding: 50px;
  border-radius: 20px;
  text-align:center;
  width: 450px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  transition: transform 0.2s;
}
.profile-card:hover {
  transform: translateY(-5px);
}

.avatar-container{
  position: relative;
  margin-bottom: 20px;
}
.avatar{
  width: 130px;
  height: 130px;
  border-radius: 50%;
  cursor:pointer;
  border: 3px solid #ffd700;
  transition: transform 0.2s;
}
.avatar:hover{
  transform: scale(1.1);
}

.username{
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.email{
  font-size: 16px;
  margin-bottom: 10px;
}

.coins{
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 25px;
}
.coin-icon{
  margin-right: 8px;
  color: #ffb400;
}

.actions{
  display:flex;
  justify-content: center;
  gap: 20px;
}

.btn{
  padding: 10px 25px;
  border:none;
  border-radius: 10px;
  font-size: 16px;
  cursor:pointer;
  transition: all 0.2s;
}

.btn.recharge{
  background: linear-gradient(to right, #4caf50, #81c784);
  color: white;
}
.btn.recharge:hover{
  background: linear-gradient(to right, #388e3c, #66bb6a);
}

.btn.logout{
  background: linear-gradient(to right, #f44336, #e57373);
  color: white;
}
.btn.logout:hover{
  background: linear-gradient(to right, #d32f2f, #ef5350);
}
</style>
