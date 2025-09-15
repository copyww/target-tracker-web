

<template>
  <div class="common-layout">
    <el-container>
      <el-header></el-header>
      <el-main>
        <div class="app-container flex">
          <videoShower class="flex-1"/>
          <VideoSidebar class="w-1/3"/>
        </div>
      </el-main>
      <el-footer>
        <FixedBottomActions />
      </el-footer>
    </el-container>
  </div>



</template>


<script setup>
import videoShower from './components/videoShower.vue'
import VideoSidebar from './components/VideoSidebar.vue'
import FixedBottomActions from './components/FixedBottomActions.vue'
import UploadModals from './components/UploadModals.vue'


</script>
<style lang="scss">

.app-container {
  display: flex;
  height: 100%;
  width: 100%;
}

.main {
  flex: 1;       /* 自动占满剩余空间 */
  min-width: 0;  /* 防止子元素撑开 */
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}


.common-layout,
.el-container {
  height: 100vh;   /* 占满整个屏幕高度 */
  display: flex;
  flex-direction: column;
}

.el-main {
  flex: 1;         /* 自动填充中间 */
  overflow: auto;  /* 内容过多时滚动 */
}

.el-footer {
  height: 60px;    /* 自定义 footer 高度 */
  line-height: 60px;
  text-align: center;
  background: #f2f2f2;
}

// 整体背景为灰色

</style>