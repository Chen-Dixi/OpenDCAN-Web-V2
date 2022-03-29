<script>
import DatasetListCell from '../components/DatasetListCell.vue'
export default {
  components: {
    DatasetCell: DatasetListCell
  },
  data() {
    return {
      tasks: [
        
        { name: 'Image Classification', badge:'3' },
        { name: 'Action Recognition', badge:'1' },
      ],
      datasets: [
        {id:1, title:'手写数字体', description:'自己的手写数字体，用来训练能识别自己手写数字的模型', imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000000001-f66c5dc9_UOPLOsj.jpg'},
        {
          id:2, 
          title:'实验室物品', 
          description:'从实验室收集的办公室物品，包括Office31的所有类别',
          imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000000862-18b92295_QcdVuiG.jpg'},
        {
          id:3, 
          title:'手势', 
          description:'自己收集的手势图片，希望通过已有的数据集进行辅助标注',
          imageUrl:'https://production-media.paperswithcode.com/thumbnails/dataset/dataset-0000003668-ac1bf57d_vhxwilG.jpg'
        }
      ]
    }
  },
  mounted(){
    // emit
    this.$emit('didSelectTab', 'datasets')
  },
  // emits:['didSelectTab'],
}
</script>

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
            <el-dropdown class="float-right" trigger="click">
              <el-button>导入</el-button>
              <template #dropdown>
                <upload-dataset-dropdown-menu/>
              </template>
            </el-dropdown>
            
          </div>
          
          <dataset-cell v-for="dataset in datasets" :dataset="dataset" :key="dataset.id"/>

        </el-main>
      </el-container>
  </el-main>
</template>


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