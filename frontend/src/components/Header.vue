<template>
    <div class="header-left">
        <a href="/">
            <img alt="Vue logo" src="../assets/header-logo.png"/>
        </a>
        
    </div>
    <div class="header-right">
            <el-link class="header-item" href="/">关于</el-link>
            <a class="header-button" href="/login">登录</a>
    </div>
</template>

<style>
.header-left {
    position: relative;
    left: 0;
    display: flex;
}
.header-right {
    position: absolute;
    right: 0;
    display: flex;
    margin: 0 20px;
}
.header-item{
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