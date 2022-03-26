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
                <span>无标签姿态数据标注项目  </span>
                <el-icon><edit /></el-icon>
            </div>
            <el-menu
            default-active="1" @select="didSelect"
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
        
    </el-container>
</template>
<script lang="ts">
import { computed, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
export default {
    setup() {
        const route = useRoute();

        const onRoutes = computed(() => {
            return route.path;
        });

        const store = useStore();

        return {
            onRoutes,
        };
    },
    methods:{
        didSelect(index){
            console.log(index)
        }
    },
    beforeRouteUpdate (to, from){
        console.log(to.params.id)
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
</style>