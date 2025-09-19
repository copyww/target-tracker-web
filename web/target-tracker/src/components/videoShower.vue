<template>
  <section class="video-box">
    <video
      ref="videoRef"
      class="video-player"
      playsinline
      controls
    ></video>
    <canvas
      ref="overlayCanvas"
      class="overlay-canvas"
      :style="{ pointerEvents: isPaused ? 'auto' : 'none' }"
      @mousedown="startDraw"
    ></canvas>
  </section>
</template>

<script>
import Hls from 'hls.js'
import { bus } from '@/utils/bus'

export default {
  data() {
    return {
      videoEl: null,
      hls: null,
      isPaused: false,
      isDrawing: false,
      startX: 0,
      startY: 0,
      currentX: 0,
      currentY: 0,
      videoUrl: '',
      videoKey: 0,
      ws: null
    }
  },
  mounted() {
    this.videoEl = this.$refs.videoRef

    // 初始化 HLS
    this.hls = new Hls()
    this.hls.attachMedia(this.videoEl)

    this.hls.on(Hls.Events.ERROR, (event, data) => {
      console.error('[HLS ERROR]', data)
    })

    // WebSocket
    this.ws = new WebSocket('ws://127.0.0.1:8000/ws-tracking')
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.drawTrackedBox(data)
    }

    // bus 播放视频
    bus.on('playvideo', (video) => {
      this.videoUrl = video.path
      if (Hls.isSupported()) {
        this.hls.loadSource(video.path)
        this.hls.startLoad()
      } else {
        this.videoEl.src = video.path
      }
      this.videoEl.poster = video.thumbnail
      this.videoKey += 1
      this.videoEl.play()
    })

    // 空格键控制播放
    window.addEventListener('keydown', this.handleKeydown)

    // video 播放/暂停监听
    this.videoEl.addEventListener('pause', () => { this.isPaused = true })
    this.videoEl.addEventListener('play', () => { this.isPaused = false; this.isDrawing = false })

    // 初始化 canvas 固定大小
    this.resizeCanvas()
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeydown)
    if (this.hls) this.hls.destroy()
  },
  methods: {
    resizeCanvas() {
      const canvas = this.$refs.overlayCanvas
      // 🔒固定宽高（和 video-box 保持一致）
      canvas.width = 1000
      canvas.height = 562
    },
    handleKeydown(e) {
      if (e.code === 'Space') {
        e.preventDefault()
        e.stopPropagation()
        if (!this.videoEl) return
        if (this.videoEl.paused) {
          this.videoEl.play()
        } else {
          this.videoEl.pause()
        }
      }
    },
    startDraw(e) {
      if (!this.isPaused) return
      this.isDrawing = true
      const rect = this.$refs.overlayCanvas.getBoundingClientRect()
      this.startX = e.clientX - rect.left
      this.startY = e.clientY - rect.top
      window.addEventListener('mousemove', this.drawing)
      window.addEventListener('mouseup', this.endDraw)
    },
    drawing(e) {
      if (!this.isDrawing) return
      const canvas = this.$refs.overlayCanvas
      const rect = canvas.getBoundingClientRect()
      this.currentX = e.clientX - rect.left
      this.currentY = e.clientY - rect.top
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.strokeStyle = 'red'
      ctx.lineWidth = 2
      ctx.strokeRect(this.startX, this.startY, this.currentX - this.startX, this.currentY - this.startY)
    },
    endDraw() {
      if (!this.isPaused) return
      this.isDrawing = false
      window.removeEventListener('mousemove', this.drawing)
      window.removeEventListener('mouseup', this.endDraw)

      const box = {
        x: this.startX,
        y: this.startY,
        width: this.currentX - this.startX,
        height: this.currentY - this.startY
      }
      console.log('框选区域：', box)

      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(box))
      }

      this.videoEl.play()
    },
    drawTrackedBox(box) {
      const canvas = this.$refs.overlayCanvas
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.strokeStyle = 'lime'
      ctx.lineWidth = 2
      ctx.strokeRect(box.x, box.y, box.width, box.height)
    }
  }
}
</script>

<style scoped>
.video-box {
  position: relative;
  width: 1000px;  /* 🔒固定宽度 */
  height: 562px;  /* 🔒固定高度（16:9 比例） */
  background: black;
  flex-shrink: 0; /* ✅避免把旁边列表挤没 */
}
.video-player {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
