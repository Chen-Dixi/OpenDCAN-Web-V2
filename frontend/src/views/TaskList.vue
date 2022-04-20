<template>
    <el-main class="tasks-main-wrapper">
        <div class="table-wrapper">
            <el-table :data="tasks" styel="width: 100%">
                <el-table-column  label="任务类型" width="150px"/>
                <el-table-column prop="name" label="名称" width="180px"/>
                <el-table-column prop="address" label="源域数据集" width="220px"/>
                <el-table-column label="目标域数据集" width="220"/>
                <el-table-column prop="date" label="创建日期" />
                <el-table-column label="任务状态"/>
                <el-table-column label="操作"/>
            </el-table>
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
      totalItems: 0,
      currentPage: 1,
      ipp: 6,
      tasks: []
    }
  },
  mounted(){
    // emit
    this.$emit('didSelectTab', 'tasks')
  },
  methods: {
    getTaskList (currentPage, q='') {
      let params = {ipp: this.ipp, limit: this.ipp, offset: (currentPage-1)*this.ipp, username: cookies.get('username')};
      requests.GetTaskList(params, this).then(res => {
        this.totalItems = res.data.maxPage * this.ipp;
        this.tasks = res.data.tasks;
        // console.log(this.datasets);
      })
    },
  }
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