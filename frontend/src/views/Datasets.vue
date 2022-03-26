<script>
import DatasetListCell from '../components/DatasetListCell.vue'
export default {
  components: {
    DatasetCell: DatasetListCell
  },
  data() {
    return {
      tasks: [
        { name: 'Semantic Segmentation', badge:'12' },
        { name: 'Image Classification', badge:'175' },
        { name: 'Object Detection', badge:'56' },
        { name: 'Question Answering', badge:'749' },
        { name: 'Action Recognition', badge:'56' },
        { name: 'Domain Adaptation', badge:'78' }
      ],
      datasets: [
        {id:1, title:'Office31', description:'The Office dataset contains 31 object categories in three domains: Amazon, DSLR and Webcam. The 31 categories in the dataset consist of objects commonly encountered in office settings, such as keyboards, file cabinets, and laptops. The Amazon domain contains on average 90 images per class and 2817 images in total. As these images were captured from a website of online merchants, they are captured against clean background and at a unified scale. The DSLR domain contains 498 low-noise high resolution images (4288×2848). There are 5 objects per category. Each object was captured from different viewpoints on average 3 times. For Webcam, the 795 images of low resolution (640×480) exhibit significant noise and color as well as white balance artifacts.'},
        {id:2, title:'Digits', description:'The DIGITS dataset consists of 1797 8×8 grayscale images (1439 for training and 360 for testing) of handwritten digits.'},
        {id:3, title:'Office-Home', description:'Office-Home is a benchmark dataset for domain adaptation which contains 4 domains where each domain consists of 65 categories. The four domains are: Art – artistic images in the form of sketches, paintings, ornamentation, etc.; Clipart – collection of clipart images; Product – images of objects without a background and Real-World – images of objects captured with a regular camera. It contains 15,500 images, with an average of around 70 images per class and a maximum of 99 images in a class.'},
        {id:4, title:'VisDA-2017', description:'VisDA-2017 is a simulation-to-real dataset for domain adaptation with over 280,000 images across 12 categories in the training, validation and testing domains. The training images are generated from the same object under different circumstances, while the validation images are collected from MSCOCO..'}
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
            <content-filter class="box-card" :contents="tasks"/>
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