<template>
  <el-scrollbar max-height="400px" class="video-sidebar">
    <el-card
      class="scrollbar-demo-item"
      shadow="hover"
      v-for="video in videos"
      :key="video.id"
      @click="playVideo(video)"
    >
      <div class="card-item">
        <!-- 用后端返回的缩略图 -->
        <img class="thumbnail" :src="video.thumbnail" alt="Video Thumbnail" />
        <div class="video-info">
          <p>{{ video.id }}</p>
          <small>{{ video.title }}</small>
        </div>
      </div>
    </el-card>
  </el-scrollbar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'
import { computed } from 'vue'
import { bus } from '@/utils/bus'

const store = useStore()
const username = computed(() => store.getters['user/getUsername'])



// 视频列表
const videos = ref([])

// 从后端获取视频列表
async function fetchVideos() {
  console.log('Fetching videos for user:', username.value)
  try {
    const response = await axios.post('http://127.0.0.1:8000/videos/', {
      username: username.value
    })
    console.log('Fetched videos:', response.data)

    // 只保留 id、title、thumbnail 三个字段
    videos.value = response.data.map(video => ({
      id: video.id,
      title: video.title,
      thumbnail: video.thumbnail,
      path: video.path // 添加视频路径
    }))
  } catch (error) {
    console.error('Error fetching videos:', error)
    videos.value = []
  }
}

const playVideo = (video) => {
  // 这里可以添加播放视频的逻辑
 bus.emit("playvideo",video)
}

defineExpose({
  playVideo
})

// 组件挂载时请求
onMounted(fetchVideos)
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