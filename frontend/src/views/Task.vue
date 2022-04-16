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
                <span>办公生活用品标注项目  </span>
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
                    <component :is="Component"/>
                </keep-alive>
            </router-view>
        </el-main>

    </el-container>
</template>
<script lang="ts">
import { computed, watch } from "vue";
import { useRoute } from "vue-router";
import utils from '../common/utils';
export default {
    setup() {
        const route = useRoute();

        // in setup() function, we can create reactivity APIs and expose them,
        // and the computed() function will return a read-only ref object
    },
    methods:{
        didSelect(index){
            this.$router.replace(index)
        }
    },
    computed:{
        onRouted() {
            // 帮助 菜单栏确定当前选中栏目
            return utils.lastPathElem(this.$route.path)
        }
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