<template>
    <el-button @click="handleUpload" type="primary">
        Upload<el-icon class="el-icon--right"><Upload /></el-icon>
    </el-button>

    <UploadModals ref="uploadModalRef" />
</template>


<script setup>
import{ref} from 'vue';
import UploadModals from './UploadModals.vue';
  const uploadModalRef = ref(null);


const handleUpload = () => {
  // 通过ref调用子组件的方法

  uploadModalRef.value.show();
};
</script>