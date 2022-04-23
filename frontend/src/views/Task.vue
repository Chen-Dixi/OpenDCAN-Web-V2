<script setup lang="ts">

import {Menu as IconMenu} from '@element-plus/icons-vue'
import {Grid} from '@element-plus/icons-vue'
import {Timer} from '@element-plus/icons-vue'
import {VideoPlay} from '@element-plus/icons-vue'
import {Edit} from '@element-plus/icons-vue'
</script>


<template>
    <el-container>
        <el-aside  width="280px">
            <div class="menu-header">
                <span>{{task.name}}</span>
                <el-icon><edit /></el-icon>
            </div>
            <el-menu
            :default-active="onRouted" @select="didSelect"
            >
                <el-menu-item index="dataset">
                <el-icon><grid /></el-icon>
                <span>Dataset</span>
                </el-menu-item>
                <el-menu-item index="train">
                <el-icon><timer /></el-icon>
                <span>Train</span>
                </el-menu-item>
                <el-menu-item index="play">
                <el-icon><video-play /></el-icon>
                <span>Play</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main class="main-container">
            <router-view v-slot="{ Component }">
                <keep-alive>
                    <component :is="Component" :task_prop='task'/>
                </keep-alive>
            </router-view>
        </el-main>
    </el-container>
</template>

<script lang="ts">
import { computed, watch } from "vue";
import { useRoute } from "vue-router";
import requests from '../common/api'
import utils from '../common/utils';
export default {
  setup() {
    // const route = useRoute();

    // in setup() function, we can create reactivity APIs and expose them,
    // and the computed() function will return a read-only ref object
  },
  data() {
    return {
      task:{

      }
    }
  },
  methods:{
    didSelect(index){
      this.$router.replace(index)
    },
    getTask() {
      requests.GetTask(this.$route.params.taskId, {}, this).then(res => {
    // this.articleForm = res.data.article;
    // this.contentTemp = this.articleForm.content;
    // if (this.articleForm.bannerUrl) {
    //   this.uploadImageName = 'banner.jpg';
    //   this.uploadImages = [{ name: this.uploadImageName, url: this.articleForm.bannerUrl }];
    // }
      this.task = res.data
    });
    }
  },
  computed:{
    onRouted() {
        // 帮助 菜单栏确定当前选中栏目
      return utils.lastPathElem(this.$route.path)
    }
  },
  created() {
    this.getTask()
  },
  beforeRouteUpdate (to, from){
    
  },
}
</script>

<style scoped>
.menu-header{
  display: flex;
  padding: 20px;
  font-family: "Lato";
  font-weight: 500;
  font-size: 18px;
  text-align: left;
  align-items: center;
  justify-content: space-between;
}
.main-container {
  padding: 20px;
}
</style>