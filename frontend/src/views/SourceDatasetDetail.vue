<template>
    <el-main class="text-align-left">
        <el-header>
            <header-component/>
        </el-header>
        <div class="float-right dataset-edit">
            <el-button :icon="Edit" @click="editFormVisible = true">编辑</el-button>
        </div>
        <h1>{{ source_dataset.title }}</h1>
        
        <el-row>
            <el-col :span="12">
                

                <p class="text-wrapper">{{ source_dataset.description}}</p>
                <el-card shadow="nerver">
                    <el-table :data="source_labels" styel="width: 100%" >
                        <el-table-column type="index" :index="(index) => index" width="50" label="id" />
                        <el-table-column prop="name" label="标签名称" />
                    </el-table>
                </el-card>
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
                    <el-button @click="resetForm">取消</el-button>
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
            source_dataset:{},
            source_labels:[],
        }
    },
    components: {
        HeaderComponent: Header
    },
    methods: {
        getDataset(){
            let params = {dataset_id: this.$route.params.datasetId}
            requests.GetSourceDataset(params, this).then(res => {
                
                this.source_dataset = res.data
                this.source_labels = []
                this.form.title = res.data.title
                this.form.description = res.data.description
                for(let i =0; i<this.source_dataset.labels.length; i++){
                    let item = {name:this.source_dataset.labels[i]}
                    this.source_labels.push(item)
                }
            });
        },
        beforClose(done: () => void){
            this.resetForm()
            done()
        },
        resetForm(){
            this.form.title = this.source_dataset.title
            this.form.description = this.source_dataset.description
            this.editFormVisible = false
        },
        submitChange(){
            let data = {
                id: this.source_dataset.id,
                title: this.form.title,
                description: this.form.description
            }
            requests.UpdateSourceDataset(data, this).then(res => {
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
.dataset-edit {
    position: relative;
    top: 30px;
}
.dialog-footer button:first-child {
  margin-right: 10px;
}

</style>