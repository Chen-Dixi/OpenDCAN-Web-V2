<template>
    <el-container class="home-container">
      <el-header>
        <header-component :selectedTab="selectedTab" />
      </el-header>
      <router-view @didSelectTab="selectTab"/>
    </el-container>
</template>
<script lang="ts">
// @ts-ignore
import Header from '../components/HeaderComponent.vue'

export default {
  data() {
    return {
      selectedTab: ""
    }
  },
  components: {
    HeaderComponent: Header
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
