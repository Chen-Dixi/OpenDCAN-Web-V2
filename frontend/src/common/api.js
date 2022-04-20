import axios from 'axios'
import config from './config'
import {useCookies} from 'vue3-cookies'
const {cookies} = useCookies()

const request = (url, options = {}, method = 'get', _this, autoCatch = true, bodyGet = false) => {
  let headers = {};
  if (!url.endsWith('login') && !url.endsWith('register') && !url.endsWith('forgetPassword')) {
    headers = {
      'Authorization': 'Bearer '+cookies.get('access_token')
    }
  }

  let key = ~['get', 'head', 'options'].indexOf(method) ? 'params' : 'data';
  
  let apiUrl = config.backend_service_url;
  let promise = axios(
    Object.assign({
      'url': `${apiUrl}${url}`,
      'method': method,
      'headers': headers
    }, {[key]: options})
  );

  let cPromise = autoCatch ? promise.catch(error => {
    if (!error.response) {
      _this.$notify.error({
        title: '错误',
        message: '请求失败，请检查网络'
      })
    } else if (!error.response.data.hasOwnProperty('detail')) {
      _this.$notify.error({
        title: '错误',
        message: error.response.statusText
      })
    } else {
      _this.$notify.error({
        title: '错误',
        message: error.response.data.detail
      });
    }
  }) : promise;

  return cPromise.then(res => {
    return new Promise(resolve => {
      if (res !== undefined)
        resolve(res);
    })
  });
};

const axiosLogin = (data, _this) => {
  return request('/login', data, 'post', _this);
};

const axiosRegister = (data, _this) => {
  return request('/users/register', data, 'post', _this);
};

const axiosDatasetList = (data, _this) => {
  return request('/dataset/target/list', data, 'get', _this, true, true)
}

const axiosTaskList = (data, _this) => {
  return request('/task/list', data, 'get', _this)
}

let requests = {
    Login: axiosLogin,
    Register: axiosRegister,
    GetDatasetList: axiosDatasetList,
    GetTaskList: axiosTaskList,
};

export default requests;