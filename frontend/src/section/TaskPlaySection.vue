<template>
  <div class="text-align-left margin-bottom-20">
    <el-select v-model="model_id" class="m-2" placeholder="选择模型">
      <el-option
        v-for="model in model_selections"
        :key="model.id"
        :label="model.file_path"
        :value="model.id"
      />
    </el-select>  
  </div>
  
  <el-tabs
    v-model="activeTab"
    type="card"
    class="play-tabs"
  >
    <el-tab-pane label="单样本" name="first" v-loading="sample_loading">
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
          :headers="uploadHeader"
          :limit="1"
          :on-exceed="handleExceed"
          :action="uploadActionUrl"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :on-change="handleOnChange"
          :on-remove="handleRemove"
          :before-upload="beforeImageUpload"
          :data="uploadData"
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
            <el-button v-if="imageUrl" @click="submitUpload" round>识别</el-button>
            
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
import {useCookies} from 'vue3-cookies'
import { Plus } from '@element-plus/icons-vue'
import requests from '../common/api';
import type { UploadInstance, UploadFile, UploadRawFile, UploadFiles } from 'element-plus'
import globalConfig from '../common/config'
import { ElMessage, } from 'element-plus'
import {genFileId} from 'element-plus'
import { ref } from 'vue'
const {cookies} = useCookies()

export default {
  props:['task_prop'],
  components: {
    Plus: Plus
  },
  setup(){
    const model_id = ref()
    return {
      model_id
    }
  },
  data() {
    return {
      model_selections: [],
      activeTab: 'first',
      imageUrl: '',
      predict: '',
      unknown_likelihood: '',
      sample_check_id: '',
      uploadActionUrl: globalConfig.backend_service_url + '/task/play/inference/sample',
      uploadData: {},
      uploadHeader: {Authorization: 'Bearer '+cookies.get('access_token'),},
      sample_loading: false,
      sample_check_timer: null,
    }
  },
  methods:{
    getModelSelection(){
      // 下拉框 加载可选的 预训练模型
      requests.GetReadyTaskModelSelection(this.$route.params.taskId, this).then(res => {
        this.model_selections = res.data.selections
      });
    },

    beforeImageUpload(rawFile: UploadRawFile){
      if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
        ElMessage.error('Picture must be JPG or PNG format!')
        return false
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Picture size can not exceed 2MB!')
        return false
      }

      return true
    },

    handleUploadSuccess(response, uploadFile: UploadFile){
      console.log(response)
      this.sample_check_id = response.check_id
      this.sample_loading = true;
      
      // 上传成功后， 循环等待 推理结果
      this.sample_check_timer = setInterval(() => {
        requests.CheckSampleInferenceResult(this.sample_check_id, this).then(res => {
          if (res.data.state == 'SUCCESS'){
            this.sample_loading = false;
            this.predict = res.data.predict_class
            this.unknown_likelihood = res.data.likelihood
            this.end_timer()
          } else if (res.data.state == 'ERROR'){
            this.sample_loading = false;
            this.end_timer()
            this.$notify.error({
              title: '错误',
              message: '模型运行失败',
            })
          }
        });
      }, 1000);
    },

    handleUploadError(error, uploadFile: UploadFile){
      console.log(error)
      this.sample_loading = false;
      this.$notify.error({
        title: '错误',
        message: error.detail
      })
    },

    handleRemove(uploadFile: UploadFile, uploadFiles: UploadFiles){
      this.imageUrl = ''
    },

    handleOnChange(uploadFile: UploadFile, uploadFiles: UploadFiles){
        if (uploadFiles.length === 1 && this.beforeImageUpload(uploadFile.raw)){
          this.imageUrl = URL.createObjectURL(uploadFile.raw!)
        }else if (uploadFiles.length === 1) {
          this.$refs['uploadRef'].clearFiles()
          this.imageUrl = ''
        }
    },

    handleExceed(files) {
      this.$refs['uploadRef'].clearFiles()
      let file = files[0] as UploadRawFile
      file.uid = genFileId()
      this.$refs['uploadRef'].handleStart(file)
    },

    submitUpload() {

      if (this.model_id == null) {
        ElMessage.error('请选择用于推理的模型!')
        return
      }
      
      this.uploadData = {'model_id': this.model_id, 'task_id': this.$route.params.taskId}

      this.$refs['uploadRef'].submit()
    },

    clear (){
      this.$refs['uploadRef'].clearFiles()
      this.imageUrl = ''
      this.predict = ''
      this.unknown_likelihood = ''
    },
    end_timer(){
      clearInterval(this.sample_check_timer);
      this.sample_check_timer = null // 这里最好清除一下，回归默认值
    },
  },

  created(){
    this.getModelSelection()
  },
  beforeDestroy() {
    // js提供的clearInterval方法用来清除定时器
    clearInterval(this.sample_check_timer);
  },
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
