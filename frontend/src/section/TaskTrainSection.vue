<script lang="ts" setup>
import {ref} from 'vue'
const props = defineProps({
  task_prop: Object
})

const loading = ref(true)

const dialogVisible = ref(false)
</script>

<template>
<!-- 这里用message box更合适 -->
  <!-- <el-dialog v-model="dialogVisible" title="提示" width="30%">
    <span>确定终止此次训练吗？</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="stopTraining"
          >确定</el-button
        >
      </span>
    </template>
  </el-dialog> -->
  <div>
    <h2 style="color:#6b778c;">训练场</h2>
  </div>
  <el-card  class="bg-gray-light margin-bottom-20" shadow="never">
    <el-result
        v-if="task_prop.state==2"
        title="训练中"
        sub-title="模型正在训练中..."
      >
      <template #icon>
        <el-image
          src="/src/assets/training2.gif" class="loading-image"/>
      </template>
      <template #extra>
        <el-button type="danger" @click="dialogVisible = true">终止</el-button>
      </template>
    </el-result>
    <el-result
        v-if="task_prop.state==3"
        icon="success"
        title="完成"
        sub-title="模型训练结束"
      >
      <template #extra>
        <el-button type="default" @click="dialogVisible = true">重新训练</el-button>
      </template>
    </el-result>
    <el-result
        v-if="task_prop.state==1"
        title="待训练"
        sub-title="等待提交训练任务"
      >
      <template #icon>
        <el-image
          src="/src/assets/training_idel.gif" class="loading-image"/>
      </template>
      <template #extra>
        <el-button type="success" @click="dialogVisible = true">提交训练</el-button>
      </template>
    </el-result>
  </el-card>
  <el-table :data="model_records" table-layout="auto">
      <!--
      id : int
      name : int
      username : int
      state : int  # 1 ready, 2 not ready
      source_id : int
      source_name : str
      target_id : int
      target_name : str

      is_active : bool # 1 active; 2 disabled
      create_time : datetime
      update_time : datetime
      -->
      <el-table-column prop="id" label="id" />
      <el-table-column prop="state" label="状态" >
        <template #default="scope">
          <el-tag
            :type="stateTagType(scope.row.state)"
            >{{ stateTagName(scope.row.state) }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column prop="source_name" label="源域数据集" />
      <el-table-column prop="target_name" label="目标域数据集" />
      <el-table-column prop="create_time" label="创建日期"/>
  </el-table>
</template>

<script lang="ts">
import requests from '../common/api'
export default {
  data(){
    return{
      model_records:[],
    }
  },
  methods:{
    stopTraining(){
      this.dialogVisible = false
      console.log("终止训练!")
    },
    getTrainingModel(){
      requests.GetTaskTrainingModel(this.$route.params.taskId, {}, this).then(res => {
        this.model_records = res.data.trainings
      });
    },
    stateTagType(state: number){
      if (state == 1) {
        // ready
        return 'success'
      }
      if (state == 2) {
        return ''
      }
      return 'danger'
    },
    stateTagName(state: number){
      if (state == 1) {
        // ready
        return '训练完成'
      }
      if (state == 2) {
        return '正在训练'
      }
      return '错误'
    }
  },
  created(){
    this.getTrainingModel()
  },
}
</script>

<style>
.loading-image {
  max-width: 200px;
}
</style>