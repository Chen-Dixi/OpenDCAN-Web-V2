<template>
    <div class="header-left">
        <a href="/">
            <img alt="Vue logo" src="../assets/header-logo.png"/>
        </a>
        
    </div>
    <nav class="header-nav">
        <el-link class="nav-link" :class="overviewSelectedClassObject" href="/">Overview</el-link>
        <el-link class="nav-link" :class="datasetsSelectedClassObject" href="/datasets">Dataset</el-link>
        <el-link class="nav-link" :class="tasksSelectedClassObject" href="/tasks">Task</el-link>
        <el-link class="nav-link" :class="playSelectedClassObject" href="/play">Play</el-link>
    </nav>
    <div class="header-right">
            <el-link class="header-item-right" href="/">关于</el-link>
            <a class="header-button" href="/login">登录</a>
    </div>
</template>
<script lang="ts" setup>
import {computed, ref} from 'vue'

const activeChildPage = ref('first')
// TBD: class and style bind
const handleClick = (tab: string, event: Event) => {
    console.log(tab, event)
}

const props = defineProps({
    selectedTab: String
})

</script>
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
        playSelectedClassObject() {
            return {
                'nav-link--selected': this.selectedTab == "play"
            }
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