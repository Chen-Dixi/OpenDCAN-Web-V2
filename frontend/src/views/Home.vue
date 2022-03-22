<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Header from '../components/Header.vue'
</script>
<template>
    <el-container class="home-container">
      <el-header>
        <Header :selectedTab="selectedTab" />
      </el-header>
      <router-view @didSelectTab="selectTab" msg="hello"/>
    </el-container>
</template>
<script>
export default {
  data() {
    return {
      selectedTab: ""
    }
  },
  methods:{
    selectTab(tabName){
      this.selectedTab = tabName
    }
  }
}
</script>


<style>
.home-container{
  display: block; 
}
.home-container .el-header{
  position: relative;
  background-color:ghostwhite;
  display: flex;
  align-items: center;
}
</style>
