<template>
  <img alt="Vue logo" src="../assets/appicon.png"/>
  <h1>登录OpenDCAN标注平台</h1>
  <el-row>
    <el-col :span="5"></el-col>
    <el-col :span="5"></el-col>
    <el-col :span="5">
      <el-form ref="form" :model="account" label-width="80px" label-position="top">
        <el-form-item label="用户名 或 邮箱地址">

          <el-input v-model="account.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="account.password" type="password"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item>
              <el-button type="primary" >登录</el-button>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-link href="/register" type="primary">没有账号? 点击注册</el-link>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-col>
    <el-col :span="5"></el-col>
    <el-col :span="5"></el-col>
  </el-row>
</template>
<script>
export default {
  name: 'Login',
  data() {
    return {
      account: {
        username: null,
        password: null
      }
    }
  }
}
</script>