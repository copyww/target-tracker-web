<template>
  <!-- <el-button @click="add">Add Item</el-button>
  <el-button @click="onDelete">Delete Item</el-button> -->
  <el-scrollbar max-height="400px" class="video-sidebar">
    <el-card class="scrollbar-demo-item"   shadow="hover" v-for="video in videos":key="video.id">
      <div class="card-item" >
          <img class="thumbnail" src="https://cdn.jsdelivr.net/gh/xdlumia/files/video-play/ironMan.jpg" alt="Video Thumbnail" >
        <div class="video-info">
          <p>{{ video.id }}</p>
          <small>{{ video.title }}</small>
        </div>
        </div>
    </el-card>
  </el-scrollbar>
</template>

<script setup>
import { ref } from 'vue'

const videos = ref([
  { id: 1, title: 'Video 1' },
  { id: 2, title: 'Video 2' },
  { id: 3, title: 'Video 3' },
  { id: 4, title: 'Video 4' },
  { id: 5, title: 'Video 5' },
  { id: 6, title: 'Video 6' },
  { id: 7, title: 'Video 7' },
  { id: 8, title: 'Video 8' },
  { id: 9, title: 'Video 9' },
  { id: 10, title: 'Video 10' },
])

const add = () => {
  count.value++
}
const onDelete = () => {
  if (count.value > 0) {
    count.value--
  }
}
</script>

<style scoped>


.video-sidebar {
  padding-left: 110px;
  box-sizing: border-box;
  height: 100%;
  /* background-color: #f5f5f5; */
  /* border-left: 1px solid #ddd; */
}

.scrollbar-demo-item {
  width: 480px;
  display: flex;
  /* align-items: center; */
  /* justify-content: center; */
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.card-item {
  display: flex;
  align-items: center;
  /* justify-content: center; */
  height: 100%;
  padding: 10px;
}

.thumbnail {
  width: 80px;
  height: 45px;
  margin-right: 20px;
  border-radius: 4px;
  object-fit: cover;
}

.video-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* align-items: flex-start; */
}
</style>