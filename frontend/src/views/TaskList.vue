<template>
    <el-main class="tasks-main-wrapper">
        
        <div class="table-wrapper">
            <div style="padding-bottom: 40px">
              <el-button type="primary" class="float-left" @click="createTaskConfirm">新任务</el-button>
            </div>
            
            <el-table :data="tasks" styel="width: 100%">
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
                <el-table-column prop="name" label="名称" width="180px"/>
                <el-table-column prop="source_name" label="源域数据集" width="220px"/>
                <el-table-column prop="target_name" label="目标域数据集" width="220"/>
                <el-table-column prop="create_time" label="创建日期"/>
                <el-table-column prop="update_time" label="编辑日期"/>
                <el-table-column prop="state" label="任务状态">
                  <template #default="scope">
                    <el-tag
                      :type="stateTagType(scope.row.state)"
                      >{{ stateTagName(scope.row.state) }}</el-tag
                    >
                  </template>  
                </el-table-column>> <!-- TBD自定义 -->
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button size="small" @click="handleEdit(scope.row)">查看</el-button>
                  </template>  
                </el-table-column>
            </el-table>
            <el-pagination
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-size="ipp"
              :page-count="maxPage"
              background
              layout="prev, pager, next">
            </el-pagination>
        </div>
        
    </el-main>
</template>
<script lang="ts" setup>

</script>
<script lang="ts" >
import {useCookies} from 'vue3-cookies'
import requests from '../common/api';
const {cookies} = useCookies()
import { ElMessageBox } from 'element-plus'

export default {
  data() {
    return {
      maxPage: 1,
      currentPage: 1,
      ipp: 10,
      tasks: []
    }
  },
  mounted(){
    // emit
    this.$emit('didSelectTab', 'tasks')
  },
  methods: {
    handleCurrentChange (currentPage) {
      this.getTaskList(this.currentPage);
    },
    getTaskList (currentPage, q='') {
      let params = {ipp: this.ipp, offset: (currentPage-1)*this.ipp};
      requests.GetTaskList(params, this).then(res => {
        this.maxPage = res.data.maxPage
        this.tasks = res.data.tasks;
        // console.log(this.datasets);
      })
    },
    createTaskConfirm( ) {
      ElMessageBox.prompt(
        '请输入新任务的名称',
        '创建任务',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
        }
      ).then(({value}) => {
        let data = {task_name: value}
        requests.CreateTask(data, this).then(res => {
          this.getTaskList(this.currentPage)
        })
      })
    },
    handleEdit(row) {
      // 任务详情界面
      this.$router.push('/task/'+row.id)
    },
    stateTagType(state: number){
      if (state == 1) {
        // ready
        return 'info'
      }
      if (state == 2) {
        return ''
      }
      if (state == 3) {
        return 'success'
      }
      return 'danger'
    },
    stateTagName(state: number){
      if (state == 1) {
        // idle
        return '待训练'
      }
      if (state == 2) {
        return '训练中'
      }
      if (state == 3) {
        return '准备好'
      }
      return '错误'
    },
  },
  created() {
    this.getTaskList(this.currentPage);
  },
}
</script>

<style scoped>
.tasks-main-wrapper{
    justify-content: center;
    display: flex;
}
.table-wrapper {
    flex: 0 0 auto;
    width: 80%
}
</style>