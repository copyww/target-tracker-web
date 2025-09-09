<template>
  <div class="bg-red-300 w-2/3 h-auto relative flex-col mx-auto">
    <!-- 顶部标题开始 -->
    <!-- <titleCard>视频</titleCard> -->
    <!-- 顶部标题结束 -->
 
    <!-- 主体开始 -->
    <div class="mt-2">
      <div>视频ID: {{ videoId }}</div>
      <div>
        <vue3VideoPlay
          class="vue3VideoPlay"
          v-bind="options"
          poster="https://cdn.jsdelivr.net/gh/xdlumia/files/video-play/ironMan.jpg"
        />
      </div>
    </div>
    <!-- 主体结束 -->
  </div>
</template>
 
<script setup>
import { useRoute } from "vue-router";
// import titleCard from "./components/title.vue";
import { reactive } from "vue";
 
const route = useRoute();
const videoId = route.params.id;
 
const options = reactive({
  width: "800px", //播放器宽度
  height: "450px", //播放器高度
  color: "#409eff", //主题色
  title: "", //视频名称
  src: "https://cdn.jsdelivr.net/gh/xdlumia/files/video-play/IronMan.mp4", //视频源
  muted: false, //静音
  webFullScreen: false,
  speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
  autoPlay: false, //自动播放
  loop: false, //循环播放
  mirror: false, //镜像画面
  ligthOff: false, //关灯模式
  volume: 0.3, //默认音量大小
  control: true, //是否显示控制
  controlBtns: [
    "audioTrack",
    "quality",
    "speedRate",
    "volume",
    "setting",
    "pip",
    "pageFullScreen",
    "fullScreen",
  ], //显示所有按钮,
});
</script>
 
<style scoped></style>