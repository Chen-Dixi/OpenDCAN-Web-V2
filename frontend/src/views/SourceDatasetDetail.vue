<template>
    <h1>{{ source_dataset.title }}</h1>

    <p>{{ source_dataset.description}}</p>
    <el-card shadow="nerver">
        <el-table :data="source_labels" styel="width: 100%" >
            <el-table-column type="index" :index="(index) => index" width="50" label="id" />
            <el-table-column prop="name" label="标签名称" width="180px"/>
        </el-table>
    </el-card>
</template>

<script lang="ts">
import requests from '../common/api'

export default {
    data() {
        return {
            source_dataset:{},
            source_labels:[],
        }
    },
    methods: {
        getDataset(){
            let params = {dataset_id: this.$route.params.datasetId}
            requests.GetSourceDataset(params, this).then(res => {
                
                this.source_dataset = res.data
                this.source_labels = []
                for(let i =0; i<this.source_dataset.labels.length; i++){
                    let item = {name:this.source_dataset.labels[i]}
                    this.source_labels.push(item)
                }
            });
        }
    },
    created() {
        this.getDataset()
    },
}
</script>

<style scoped>
.table-container {
  text-align: left;
}
</style>