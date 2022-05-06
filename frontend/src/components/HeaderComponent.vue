<script lang="ts" setup>
import {computed, ref} from 'vue'
import {ArrowDown} from '@element-plus/icons-vue'

const props = defineProps({
    selectedTab: String
})
</script>
<template>
    <div class="header-left">
        <a href="/">
            <img alt="Vue logo" src="../assets/header-logo.png"/>
        </a>
        
    </div>
    <nav class="header-nav">
        <el-link class="nav-link" :class="overviewSelectedClassObject" href="/">首页</el-link>
        <el-link class="nav-link" 
            v-if="isUser"
            :class="datasetsSelectedClassObject" href="/datasets">数据集</el-link>
        <el-link class="nav-link"
            v-if="isAdmin" 
            :class="datasetsSelectedClassObject" 
            href="/source_datasets">管理员</el-link>
        <el-link class="nav-link" :class="tasksSelectedClassObject" href="/tasks">任务</el-link>
    </nav>
    <div class="header-right">
            <el-link class="header-item-right" href="/">关于</el-link>
            <a v-if="!logined" class="header-button" href="/login">登录</a>
            <el-dropdown v-if="logined" trigger="click" @command="logout">
                <span class="el-dropdown-link">
                {{username}}<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </span>
                <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
                </template>
            </el-dropdown>
    </div>
</template>

<script lang="ts">
export default {
    computed: {
        overviewSelectedClassObject(){
            return {
                'nav-link--selected': this.selectedTab == "overview"
            }
        },
        datasetsSelectedClassObject(){
            return {
                'nav-link--selected': this.selectedTab == "datasets"
            }
        },
        tasksSelectedClassObject() {
            return {
                'nav-link--selected': this.selectedTab == "tasks"
            }
        },
        isAdmin() {
            return this.$cookies.isKey('access_token') && this.$cookies.get('is_admin')=='true'
        },
        isUser() {
            return this.$cookies.isKey('access_token') && this.$cookies.get('is_admin')=='false'
        },
        logined() {
            return this.$cookies.isKey('access_token')
        },
        username() {
            return this.$cookies.get('username')
        }

    },
    methods: {
        logout(command) {
            this.$cookies.remove('access_token')
            this.$cookies.remove('username')
            this.$cookies.remove('is_admin')
            this.$router.push('/login')
        }
    }
}
</script>


<style scoped>
.header-left {
    position: absolute;
    left: 20px;
    display: flex;
}
.header-nav {
    position: relative;
    width: 100%;
    justify-content: center;
    display: flex;
    align-items: center;
}
.header-nav .nav-link{
    margin: 0 24px;
    font-family: LabGrotesque,Helvetica Neue,Helvetica,Arial,sans-serif;
    font-size: 18px;
    font-weight: 500;
    
}
.nav-link--selected {
    text-decoration: none;
    transform: translateY(-1px) scale(1.2);
    color: #333;
}
.header-right {
    position: absolute;
    display: flex;
    right: 20px;
}
.header-item-right{
    margin-right: 35px;
}
.header-button {
    background-color: #4285F4;
    color: #fff;
    padding: 8px 15px 6px;
    border-radius: 8px;
    font-size: 18px;
    display: inline-block;
    font-family: 'BoingSemiBold', Helvetica, Arial, sans-serif;
    text-decoration: none;
}
</style>