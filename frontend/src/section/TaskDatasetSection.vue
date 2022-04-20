
<template>
  DatasetSection {{task_prop.name}}
  <div>
    <el-select v-model="value" class="m-2" placeholder="Select" size="large">
      <el-option
        v-for="dataset in target_selections"
        :key="dataset.id"
        :label="dataset.title"
        :value="dataset.id"
      />
    </el-select>
  </div>
</template>

<script lang="ts">
import requests from "../common/api"
export default {
  props:['task_prop'],
  data(){
    return {
      target_selections: [],
      value: this.task_prop.source_name
    }
  },
  methods:{

  },
  created() {
    requests.GetTargetSelection({}, this).then(res => {
      this.target_selections = res.data.selections
    })
  }
}
</script>

<style>

</style>