<template>
    <h1>{{ target_dataset.title }}</h1>

    <p>{{ target_dataset.description}}</p>
</template>

<script lang="ts">
import requests from '../common/api'

export default {
    data() {
        return {
            target_dataset:{},
        }
    },
    methods: {
        getDataset(){
            let params = {dataset_id: this.$route.params.datasetId}
            requests.GetTargetDataset(params, this).then(res => {
                this.target_dataset = res.data
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