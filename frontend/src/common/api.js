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

const axiosSourceDatasetList = (data, _this) => {
  return request('/dataset/source/list', data, 'get', _this, true, true)
}

const axiosTargetSelectionList = (data, _this) => {
  return request('/dataset/target/list_selection', data, 'get', _this)
}

const axiosSourceSelectionList = (data, _this) => {
  return request('/dataset/source/list_selection', data, 'get', _this)
}

const axiosGetTargetDataset = (params, _this) => {
  return request('/dataset/target/get', params, 'get', _this);
}

const axiosGetSourceDataset = (params, _this) => {
  return request('/dataset/source/get', params, 'get', _this);
}

const axiosUpdateTargetDataset = (data, _this) => {
  return request('/dataset/target/update', data, 'post', _this);
}

const axiosUpdateSourceDataset = (data, _this) => {
  return request('/dataset/source/update', data, 'post', _this);
}

const axiosGetTaskList = (data, _this) => {
  return request('/task/list', data, 'get', _this);
}

const axiosGetTask = (taskId, params, _this) => {
  return request('/task/detail/' + taskId, params, 'get', _this);
}

const axiosCreateTask = (data, _this) => {
  return request('/task/create', data, 'post', _this);
}

const axiosUpdateTaskDatasetConfig = (data, _this) => {
  return request('/task/update/dataset', data, 'post', _this);
}

const axiosGetTaskModelList = (taskId, params, _this) => {
  return request('/task/train/' + taskId, params, 'get', _this);
}

const axiosCreateTaskTraining = (data, _this) => {
  return request('/task/train/create', data, 'post', _this);
}

const axiosGetTaskModelSelection = (taskId, _this) => {
  return request('/task/play/model/list/' + taskId, {}, 'get', _this);
}

const axiosCheckSampleResult = (checkId, _this) => {
  return request('/task/play/sample/'+checkId+'/check', {}, 'get', _this);
}

let requests = {
    Login: axiosLogin,
    Register: axiosRegister,
    GetDatasetList: axiosDatasetList,
    GetSourceDatasetList: axiosSourceDatasetList,
    GetTaskList: axiosGetTaskList,
    GetTargetSelection: axiosTargetSelectionList,
    GetTargetDataset: axiosGetTargetDataset,
    UpdateTargetDataset: axiosUpdateTargetDataset,
    GetSourceSelection: axiosSourceSelectionList,
    GetSourceDataset: axiosGetSourceDataset,
    UpdateSourceDataset: axiosUpdateSourceDataset,
    GetTask: axiosGetTask,
    CreateTask: axiosCreateTask,
    UpdateTaskDatasetConfig: axiosUpdateTaskDatasetConfig,
    GetTaskTrainingModel: axiosGetTaskModelList,
    GetReadyTaskModelSelection: axiosGetTaskModelSelection,
    CreateTaskTraining : axiosCreateTaskTraining,
    CheckSampleInferenceResult: axiosCheckSampleResult,
};

export default requests;