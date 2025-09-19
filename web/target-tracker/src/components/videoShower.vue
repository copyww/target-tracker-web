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
      ws: null,
      mp4_path: null,
      roi: null,
      sendInterval: null
    }
  },
  mounted() {
    this.videoEl = this.$refs.videoRef

    // 初始化 HLS
    this.hls = new Hls()
    this.hls.attachMedia(this.videoEl)
    this.hls.on(Hls.Events.ERROR, (event, data) => console.error('[HLS ERROR]', data))

    // WebSocket
    this.ws = new WebSocket('ws://127.0.0.1:8000/ws/track')
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.drawTrackedBox(data)
    }

    // bus 播放视频
    bus.on('playvideo', (video) => {
      if (!video?.path?.trim()) return console.error('video.path is empty!', video)
      this.videoUrl = video.path
      this.mp4_path = video.mp4_path
      this.roi = null
      if (Hls.isSupported()) {
        this.hls.loadSource(video.path)
        this.hls.startLoad()
      } else {
        this.videoEl.src = video.path
      }
      this.videoEl.poster = video.thumbnail
      this.videoKey += 1
      this.videoEl.play()
      this.clearSendLoop()
    })

    window.addEventListener('keydown', this.handleKeydown)
    this.videoEl.addEventListener('pause', () => this.isPaused = true)
    this.videoEl.addEventListener('play', () => {
      this.isPaused = false
      if (this.roi) this.startSendLoop()
    })

    this.resizeCanvas()
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeydown)
    if (this.hls) this.hls.destroy()
    this.clearSendLoop()
  },
  methods: {
    resizeCanvas() {
      const canvas = this.$refs.overlayCanvas
      canvas.width = 1000
      canvas.height = 562
    },
    handleKeydown(e) {
      if (e.code === 'Space') {
        e.preventDefault()
        e.stopPropagation()
        if (!this.videoEl) return
        if (this.videoEl.paused) this.videoEl.play()
        else this.videoEl.pause()
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

  // 计算视频原始像素坐标
  const canvas = this.$refs.overlayCanvas
  const videoWidth = this.videoEl.videoWidth
  const videoHeight = this.videoEl.videoHeight
  const scaleX = videoWidth / canvas.width
  const scaleY = videoHeight / canvas.height

  const x = Math.round(this.startX * scaleX)
  const y = Math.round(this.startY * scaleY)
  const width = Math.round((this.currentX - this.startX) * scaleX)
  const height = Math.round((this.currentY - this.startY) * scaleY)

  // 保存 ROI
  this.roi = { x, y, width, height }

  // 清掉红框
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // --- 发送初始化消息 ---
  if (this.ws && this.ws.readyState === WebSocket.OPEN) {
    const data = {
      type: "init",
      roi: this.roi,
      time: this.videoEl.currentTime,
      mp4_path: this.mp4_path
    }
    this.ws.send(JSON.stringify(data))
  }

  // 播放视频并开始循环追踪
  this.videoEl.play()
  this.startSendLoop()
},
startSendLoop() {
  if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return
  this.clearSendLoop()
  this.sendInterval = setInterval(() => {
    if (this.videoEl.paused) return
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return
    const data = {
      type: "track",
      time: this.videoEl.currentTime,
      mp4_path: this.mp4_path
    }
    this.ws.send(JSON.stringify(data))
  }, 40) // ~25fps
},
    clearSendLoop() {
      if (this.sendInterval) {
        clearInterval(this.sendInterval)
        this.sendInterval = null
      }
    },
    drawTrackedBox(box) {
      const canvas = this.$refs.overlayCanvas
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // 绘制时将视频原始像素缩放到 canvas 显示尺寸
      const scaleX = canvas.width / this.videoEl.videoWidth
      const scaleY = canvas.height / this.videoEl.videoHeight

      ctx.strokeStyle = 'lime'
      ctx.lineWidth = 2
      ctx.strokeRect(box.x * scaleX, box.y * scaleY, box.width * scaleX, box.height * scaleY)
    }
  }
}
</script>

<style scoped>
.video-box {
  position: relative;
  width: 1000px;
  height: 562px;
  background: black;
  flex-shrink: 0;
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
