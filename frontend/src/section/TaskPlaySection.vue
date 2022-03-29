<script lang="ts" setup>
import {ref} from 'vue'
import { Plus, UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {genFileId} from 'element-plus'
import type { UploadProps, UploadInstance, UploadUserFile, UploadRawFile } from 'element-plus'

const activeTab = ref('first')
const imageUrl = ref('')
const predict = ref('Unknown')
const unknown_likelihood = ref('83.389')
const uploadActionUrl = "https://jsonplaceholder.typicode.com/posts/"
// 上传器实例
const uploadRef = ref<UploadInstance>()

const beforeImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('Avatar picture must be JPG or PNG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

const handleUploadSuccess: UploadProps['onSuccess'] = (
  response,
  uploadFile
) => {
  console.log(response)
}

const handleUploadError: UploadProps['onError'] = (
  error,
  uploadFile
) => {
  console.log(error)
}

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  // uploadFiles === 0
  imageUrl.value = ''
}

const handleOnChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  if (uploadFiles.length === 1){
    imageUrl.value = URL.createObjectURL(uploadFile.raw!)
  }
}


const handleExceed: UploadProps['onExceed'] = (files) => {
  uploadRef.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  uploadRef.value!.handleStart(file)
}

const submitUpload = () => {
  uploadRef.value!.submit()
}

</script>
<template>
  <el-tabs
    v-model="activeTab"
    type="card"
    class="play-tabs"
  >
    <el-tab-pane label="单样本" name="first">
      <!-- 上传图片，和第一个版本的界面一样 -->
      <div>
        <!-- 内容样式由.play-tabs > .el-tabs__content控制 -->
        单样本识别
      </div>
      <el-card class="bg-gray-light" shadow="never">
        <el-upload
          ref="uploadRef"
          class="avatar-uploader"
          :auto-upload="false"
          :limit="1"
          :on-exceed="handleExceed"
          :action="uploadActionUrl"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :on-change="handleOnChange"
          :on-remove="handleRemove"
          :before-upload="beforeImageUpload"
        >
          <div v-if="imageUrl" class="image-predict-tag-holder">
            <img  :src="imageUrl" class="uploader-image">
            <div style="position: absolute;max-width: 400px;">
              <el-tag  v-if="predict" class="predict-tag" size="large" effect="dark" type="danger" >{{predict}}</el-tag>
              <el-tag  v-if="unknown_likelihood && predict" class="predict-tag" size="large" type="warning" >未知类可能性：{{unknown_likelihood}}%</el-tag>
            </div>
            
          </div>
          
          <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">只能上传jpg/png文件，且不超过2MB</div>
          </template>
        </el-upload>
        <el-row class="row-bg" justify="center" :gutter="20">
          <el-col :span="3">
            <el-button v-if="imageUrl" @click="analyse" round>识别</el-button>
            
          </el-col>
          <el-col :span="3">
            <el-button v-if="imageUrl" @click="clear" round>清除</el-button>
          </el-col>
        </el-row>
        
      </el-card>
    </el-tab-pane>
    <el-tab-pane label="数据集" name="second">
      <div>
        标注数据集
      </div>
    </el-tab-pane>
  </el-tabs>
</template>
<script lang="ts">
export default {
  methods:{
    analyse(){
      console.log('analyse!')
      this.uploadRef.submit()
    },
    clear() {
      this.uploadRef.clearFiles()
      this.imageUrl = ''
    }
  }
}
</script>
<style>
.play-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}
.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}
.el-icon.image-uploader-icon{
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
.uploader-image {
  max-width: 400px;
  min-width: 48px;
  display: block;
}
.image-predict-tag-holder{
  display: flex;
}
.predict-tag{ 
  font-family: 'BoingSemiBold', Helvetica, Arial, sans-serif;
  font-size: 15px;
  margin-left: 20px;
}
</style>
