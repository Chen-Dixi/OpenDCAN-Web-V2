
<template>
  <el-col :span="16" :offset="1">
    <el-form label-position="top">
      <el-form-item label="目标域数据集">
        <el-select v-model="target_id" class="m-2" placeholder="选择数据集" size="large">
          <el-option
            v-for="dataset in target_selections"
            :key="dataset.id"
            :label="dataset.title"
            :value="dataset.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="源域数据集">
        <el-select v-model="source_id" class="m-2" placeholder="选择数据集" size="large">
          <el-option
            v-for="dataset in source_selections"
            :key="dataset.id"
            :label="dataset.title"
            :value="dataset.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
  </el-col>
</template>

<script lang="ts">
import requests from "../common/api"
export default {
  props:['task_prop'],
  data(){
    return {
      target_selections: [],
      source_selections: [],
      target_id: null,
      source_id: null
    }
  },
  methods:{

  },
  created() {
    requests.GetTargetSelection({}, this).then(res => {
      this.target_selections = res.data.selections
    })

    requests.GetSourceSelection({}, this).then(res => {
      this.source_selections = res.data.selections
    })
  }
}
</script>
<style>
.form-container{
  text-align: left;
}
</style>