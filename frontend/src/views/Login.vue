<template>
  <img alt="Vue logo" src="../assets/appicon.png"/>
  <h1>OpenDCAN标注平台</h1>
  <el-row>
    <el-col :span="5"></el-col>
    <el-col :span="5"></el-col>
    <el-col :span="5">
      <el-form ref="loginForm" :model="loginForm" :rules="rules" label-width="80px" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item>
              <el-button type="primary" @click="submitForm('loginForm')" >登录</el-button>
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
<script lang="ts">
import requests from '../common/api';
import globalConfig from '../common/config';

export default {
  name: 'Login',
  data() {
    // let validatePhone = (rule, value, callback) => {
    //     if (!/^[1][34578][0-9]{9}$/.test(value)) {
    //       callback(new Error('手机号码输入格式不正确'));
    //     } else {
    //       callback();
    //     }
    //   };
    
    return {
      loginForm: {
        'username': '',
        'password': ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
          // { validator: validatePhone, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
      }
    }
  },
  methods: {
    submitForm(formName) {
      console.log(this.$refs[formName])
      this.login()
    },
    login(){
      // must send a username and password fields as form data.
      let formData = new FormData()

      Object.entries(this.loginForm).forEach(([key, val]) => {
        // HACK - make type happy…
        const hackVal = val as string | File;
        formData.append(key, hackVal);
      });
      requests.Login(formData, this).then(res => {
        // console.log(res)
        let data = res.data;
        this.$cookies.set('access_token', data.access_token, globalConfig.cookieExpire);
        this.$cookies.set('username', data.username, globalConfig.cookieExpire);
        this.$cookies.set('is_admin', data.is_admin, globalConfig.cookieExpire);
        this.$router.push('/index');
      });
    }
  }

}
</script>