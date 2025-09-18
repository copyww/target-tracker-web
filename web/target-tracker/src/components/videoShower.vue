<template>
  <section class="video-box">
    <videoPlayer
      ref="videoPlayer"
      :key="videoKey"
      :src="videoUrl"
      :options="videoOptions"
      class="vjs-custom-skin videoPlayer"
      :playsinline="true"
    />
    <div class="controls">
  <button @click="startSelectTarget">选择目标并追踪</button>
</div>
  </section>
</template>

<script >
import 'video.js/dist/video-js.css'
import { videoPlayer } from 'vue-video-player'
import { bus } from '@/utils/bus'

export default {
  components: { videoPlayer },
  data () {
    return {
        videoKey: 0,          // 必须初始化
        videoUrl: '',          // 当前播放 URL
      videoOptions: {

        playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
        autoplay: false,
        controls: true,
        preload: 'auto',
        aspectRatio: '16:9',
        language: 'zh-CN',
        sources: [
          {
            type: 'application/x-mpegURL', // HLS 播放
            src: ''  // 初始为空，等 bus 事件来设置
          }
        ],
        poster: '',
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true
        }
      }
    }
  },
    computed: {
    player() {
      return this.$refs.videoPlayerRef?.player
    }
  },
  mounted () {
bus.on('playvideo', (video) => {
  console.log(111111)
  const newSrc = video.path

    // 更新 videoOptions
    this.videoOptions['sources'][0]['src'] = newSrc
    console.log(this.videoOptions['sources'][0]['src'])
    console.log(22222)
    this.videoOptions.poster = video.thumbnail
    this.videoKey += 1  // 强制重新渲染组件
    this.videoUrl = newSrc
    console.log(this.videoKey)
})
},

 methods: {
    startSelectTarget() {
      console.log('clicked')
      // 暂停视频
      if (this.player) {this.player.pause()
        console.log('aaaaaaaaa')
      }

      // 启动框选模式
      console.log('进入框选模式，视频已暂停')
    }
  }


}
</script>

<style scoped>
.video-box {
  width: 1000px;
  padding: 20px;
}
</style>
