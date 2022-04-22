<template>
    <el-main class="tasks-main-wrapper">
        <div class="table-wrapper">
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
                <el-table-column prop="state" label="任务状态"/> <!-- TBD自定义 -->
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button size="small" @click="handleEdit(scope.row)">查看</el-button>
                  </template>  
                </el-table-column>> <!-- TBD自定义 -->
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
// const tableData = [
//   {
//     date: '2016-05-03',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-02',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-04',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-01',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-08',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-06',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
//   {
//     date: '2016-05-07',
//     name: 'Tom',
//     address: 'No. 189, Grove St, Los Angeles',
//   },
// ]

</script>
<script lang="ts" >
import {useCookies} from 'vue3-cookies'
import requests from '../common/api';
const {cookies} = useCookies()

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
    handleEdit(row) {
      // 任务详情界面
      this.$router.push('/task/'+row.id)
    }
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
    width: 75%
}
</style>