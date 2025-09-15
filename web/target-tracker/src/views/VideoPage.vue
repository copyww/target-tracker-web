<template>
  <div class="common-layout">
    <el-container>
      <el-header></el-header>
      <el-main>
        <div class="app-container flex">
          <videoShower class="flex-1"/>
          <VideoSidebar class="w-1/3"/>
          <el-button type="primary" @click="$router.push('/users')">用户管理</el-button>
        </div>
      </el-main>
      <el-footer>
        <el-button @click="handleUpload" type="primary">
          Upload<el-icon class="el-icon--right"><Upload /></el-icon>
        </el-button>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import videoShower from '@/components/videoShower.vue'
import VideoSidebar from '@/components/VideoSidebar.vue'

const handleUpload = () => {
  ElMessage.success('Upload button clicked!')
}
</script>

<style lang="scss">
.app-container {
  display: flex;
  height: 100%;
  width: 100%;
}

.main {
  flex: 1;
  min-width: 0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.common-layout,
.el-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-main {
  flex: 1;
  overflow: auto;
}

.el-footer {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background: #f2f2f2;
}
</style>
