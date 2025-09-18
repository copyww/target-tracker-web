<template>
<div class="cover">
  <el-upload
  class="upload-demo"
  drag
  action="http://127.0.0.1:8000/upload/"
  :headers="{ username: username }"
  :show-file-list="True"
  multiple>
  <i class="el-icon-upload"></i>
  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
  <div class="el-upload__tip" slot="tip">只能上传视频</div>
</el-upload>
</div>
</template>

<script setup>  
// import { computed } from 'vue';
// import { mapGetters } from 'vuex';

// 获取用户名
import { useStore } from 'vuex';
import { computed } from 'vue';
const store = useStore();
const username = computed(() => store.getters['user/getUsername']);

// show方法
const show = () => {
  document.querySelector('.cover').style.display = 'block';
};

// close方法
const close = () => {
  document.querySelector('.cover').style.display = 'none';
};

// 按esc键关闭弹窗
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    close();
  }
});

// 暴露show和close方法给父组件调用
defineExpose({
  show
});
</script>


<style scoped>

/* 弹窗总是在正中间，不被任何组件box影响 */
.upload-demo {
  position:fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}
/* 在文件上传的时候遮盖其他组件 */
.cover {
  display: none; /* 初始状态下隐藏遮罩 */
  /* 当上传弹窗显示时，设置 display 为 block 来显示遮罩 */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  z-index: 999; /* 确保遮盖在其他内容之上 */
}
</style>


