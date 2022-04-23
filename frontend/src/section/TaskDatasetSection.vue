
<template>
  <el-form label-position="top" size="large">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="源域数据集">
          <el-select v-model="task_prop.source_id" class="m-2" placeholder="选择数据集" @change="selectSourceChange">
            <el-option
              v-for="dataset in source_selections"
              :key="dataset.id"
              :label="dataset.title"
              :value="dataset.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="源域标签">
          <el-table :data="source_labels" styel="width: 100%" class="table-container">
              <el-table-column type="index" :index="(index) => index" width="50" label="id" />
              <el-table-column prop="name" label="标签名称" width="180px"/>
          </el-table>
        </el-form-item>
        
      </el-col>
      <el-col :span="12">
        <el-form-item label="目标域数据集">
          <el-select v-model="task_prop.target_id" class="m-2" placeholder="选择数据集">
            <el-option
              v-for="dataset in target_selections"
              :key="dataset.id"
              :label="dataset.title"
              :value="dataset.id"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import requests from "../common/api"
interface DatasetSelection {
  id : number
  title: string
}
export default {
  props:['task_prop'],
  data(){
    return {
      target_selections: [],
      source_selections: [],
      target_id: null,
      source_id: this.task_prop.source_id,
      target_idx2name: {},
      source_idx2name: {},
      source_idx2labels: {},
      source_labels: [],
      task: {},
    }
  },
  methods:{
    getSelection(){
      requests.GetTargetSelection({}, this).then(res => {
        this.target_selections = res.data.selections
        for(let i =0; i<this.target_selections.length; i++){
          let item = this.target_selections[i]
          this.target_idx2name[item.id] = item.title
        }
      })

      requests.GetSourceSelection({}, this).then(res => {
        this.source_idx2name = {}
        this.source_idx2labels = {}
        this.source_selections = res.data.selections
        for(let i =0; i<this.source_selections.length; i++){
          let item = this.source_selections[i]
          this.source_idx2name[item.id] = item.title
          this.source_idx2labels[item.id] = item.labels
        }

        this.source_labels = this.source_idx2labels[this.task_prop.source_id]
      })
    },
    onSubmit(){
      // requestDto.task_id,
      //   requestDto.source_id,
      //   requestDto.source_name,
      //   requestDto.target_id,
      //   requestDto.target_name,
      let datas = {
        task_id: this.task_prop.id,
        source_id: this.task_prop.source_id,
        source_name: this.source_idx2name[this.task_prop.source_id],
        target_id: this.task_prop.target_id,
        target_name: this.target_idx2name[this.task_prop.target_id],
      }
      
      requests.UpdateTaskDatasetConfig(datas, this).then(res => {
        // this.getSelection()
        this.$notify.success({
        title: '成功',
        message: '更新成功',});
      })
    },
    selectSourceChange(val) {
      this.source_labels = this.source_idx2labels[val]
    }
    
  },
  created() {
    this.getSelection()
  },
}
</script>
<style scoped>
.table-container {
  text-align: left;
}
</style>