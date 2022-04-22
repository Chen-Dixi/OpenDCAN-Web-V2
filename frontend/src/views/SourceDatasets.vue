<template>
    <el-main class="datasets-main-wrapper">
      <el-container class="datasets-container-page">
        <el-aside class="datasets-sidebar" width="280px">
          <el-affix :offset="20">
            <content-filter class="box-card" title="根据任务类型过滤" :contents="tasks"/>
          </el-affix>
            
        </el-aside>
        <el-main class="datasets-main-list">
          <div style="padding-bottom: 40px">
            <el-dropdown class="float-right" trigger="click" ref="dropdown_import">
              <el-button>导入</el-button>
              <template #dropdown>
                <upload-dataset-dropdown-menu @command="import_dataset"/>
              </template>
            </el-dropdown>
            <el-upload
              ref="sourceDatasetUploadRef"
              :limit="1"
              :headers="uploadHeader"
              :action="sourceDatasetUploadUrl"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :on-exceed="handleExceed"
              :before-upload="beforeUpload"
              :show-file-list="false"
            >
              <div ref="inner-upload"></div>
            </el-upload>
          </div>
          <dataset-cell v-for="dataset in datasets" :dataset="dataset" link_prefix="/dataset/source/" :key="dataset.id"/>
          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="6"
            :page-count="maxPage"
            background
            layout="prev, pager, next">
          </el-pagination>
        </el-main>
        
      </el-container>
  </el-main>
</template>
<script lang='ts'>
// @ts-ignore
import DatasetListCell from '../components/DatasetListCell.vue'

import globalConfig from '../common/config'
import type {UploadInstance, UploadFile, UploadFiles, UploadRawFile} from 'element-plus'
import {genFileId} from 'element-plus'
import {ref} from 'vue'
import {useCookies} from 'vue3-cookies'
import requests from '../common/api';
const {cookies} = useCookies()

export default {
  setup(){
    const sourceDatasetUploadRef = ref<UploadInstance>()
    return {
      sourceDatasetUploadRef
    }
  },
  components: {
    DatasetCell: DatasetListCell
  },
  data() {
    return {
      tasks: [
        { name: 'Image Classification', badge:'3' },
        { name: 'Action Recognition', badge:'1' },
      ],
      currentPage: 1,
      maxPage: 1,
      ipp: 6,
      // datasets: [
      //   {id:1, title:'手写数字体', description:'自己的手写数字体，用来训练能识别自己手写数字的模型', imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000000001-f66c5dc9_UOPLOsj.jpg'},
      //   {
      //     id:2, 
      //     title:'实验室物品', 
      //     description:'从实验室收集的办公室物品，包括Office31的所有类别',
      //     imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000000862-18b92295_QcdVuiG.jpg'},
      //   {
      //     id:3, 
      //     title:'手势', 
      //     description:'自己收集的手势图片，希望通过已有的数据集进行辅助标注',
      //     imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000003668-ac1bf57d_vhxwilG.jpg'
      //   }
      // ],
      datasets: [],
      sourceDatasetUploadUrl: globalConfig.backend_service_url+'/dataset/source/upload',
      uploadHeader: {Authorization: 'Bearer '+cookies.get('access_token'),}
    }
  },
  mounted(){
    // emit
    this.$emit('didSelectTab', 'datasets')
  },
  methods: {
    import_dataset(datatype){
      if (datatype=='dataset'){
        // this.$refs['sourceDatasetUploadRef'].$refs['invoker'].handleClick()
        // hack el-upload，触发文件选择器的 元素在 el-upload 外面。
        this.$refs['inner-upload'].click()
      }
    },
    beforeUpload(rawFile: UploadRawFile) {
      if (!rawFile.name.endsWith('.zip') && !rawFile.name.endsWith('.tar.gz') && !rawFile.name.endsWith('.tar')){
      //  ['.zip', '.tar.gz', '.tar']
        this.$message.error('File must ends with one of [.zip .tar.gz, .tar]!')
        return false
      }
      return true

    },
    handleUploadSuccess(response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) {
      // console.log(response) // {filename: '头图.png'}
      this.$notify.success({
        title: '成功',
        message: '上传成功',});
      this.$refs['dropdown_import'].handleClose();
      this.sourceDatasetUploadRef.clearFiles()
      this.getDatasetList(this.currentPage)
    },
    handleUploadError(err: Error, uploadFile: UploadFile, uploadFiles: UploadFiles) {
      // 这里的Error 类型 是 typescript 自带的类型
      let error = eval('(' + err.message + ')');
      this.$notify.error({
        title: '错误',
        message: error.detail
      })
      this.$refs['dropdown_import'].handleClose();
    },
    handleExceed(files: File[], uploadFiles: UploadFiles){
      console.log(uploadFiles)
      const file = files[0] as UploadRawFile
      file.uid = genFileId()
      this.sourceDatasetUploadRef.handleStart(file)
      this.sourceDatasetUploadRef.submit()
    },
    handleCurrentChange (currentPage) {
      this.getDatasetList(this.currentPage);
    },
    getDatasetList (currentPage, q='') {
      let params = {ipp: this.ipp, limit: this.ipp, offset: (currentPage-1)*this.ipp};
      requests.GetSourceDatasetList(params, this).then(res => {
        this.maxPage = res.data.maxPage;
        this.datasets = res.data.datasets;
        // console.log(this.datasets);
      })
    },
    selectDatasetDetail (id){
      this.$router.push('/dataset/source/'+id)
    }
  },
  created() {
    this.getDatasetList(this.currentPage);
  },
}
</script>

<style scoped>
.datasets-main-wrapper{
    display: flex;
    justify-content: center;
}
.datasets-container-page{
    flex: none;
}
.datasets-sidebar{
    background-color: white;
}
.datasets-main-list{
    width: 700px;
}
.box-card {
  margin: 20px;
  border-radius: 10px;
}
</style>