<template>
    
    <el-main class="text-align-left">
        <el-header>
            <header-component/>
        </el-header>
        
        <div class="float-right dataset-edit">
            <el-button :icon="Edit" @click="editFormVisible = true">编辑</el-button>
        </div>
        <h1>{{ target_dataset.title }}</h1>
        
        <el-row>
            <el-col :span="12">
                

                <p class="text-wrapper">{{ target_dataset.description}}</p>
            </el-col>
            <el-col :span="10" :offset="2">
                <div class="bg-purple-light grid-content"/>
            </el-col>
        </el-row>
        <el-dialog v-model="editFormVisible" title="编辑数据集" :before-close="beforClose">
            <el-form :model="form" label-position="top">
                <el-form-item label="标题" :label-width="formLabelWidth">
                    <el-input v-model="form.title" autocomplete="off" />
                </el-form-item>
                <el-form-item label="描述" :label-width="formLabelWidth">
                    <el-input
                        v-model="form.description"
                        :rows="4"
                        type="textarea"
                        placeholder="Please input"
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="resetForm">Cancel</el-button>
                    <el-button type="primary" @click="submitChange"
                    >确定</el-button
                    >
                </span>
            </template>
        </el-dialog>
    </el-main>
</template>

<script setup lang="ts">
import { Edit } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
const editFormVisible = ref(false)

const formLabelWidth = '60px'

const form = reactive({
  title: '',
  description: '',
})

</script>
<script lang="ts">
import requests from '../common/api'
import Header from '../components/HeaderComponent.vue'

export default {
    data() {
        return {
            target_dataset:{},
        }
    },
    components: {
        HeaderComponent: Header
    },
    methods: {
        getDataset(){
            let params = {dataset_id: this.$route.params.datasetId}
            requests.GetTargetDataset(params, this).then(res => {
                this.target_dataset = res.data
                this.form.title = res.data.title
                this.form.description = res.data.description
            });
        },
        beforClose(done: () => void){
            this.resetForm()
            done()
        },
        resetForm(){
            this.form.title = this.target_dataset.title
            this.form.description = this.target_dataset.description
        },
        submitChange(){
            let data = {
                id: this.target_dataset.id,
                title: this.form.title,
                description: this.form.description
            }
            requests.UpdateTargetDataset(data, this).then(res => {
                this.getDataset()
            });
            this.editFormVisible = false
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