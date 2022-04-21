// 前端可以用到的配置
let globalConfig = {
    cookieExpire: 60*60*3, // 3小时
    backend_service_url: 'http://localhost:8000',
    allowedImageType: ['image/png', 'image/jpeg'],
    bgRouter: [
      '/login', '/register',
      '/forgetPassword', '/index'
    ],
    needLoginUrl: [
      '/datasets', '/tasks',
      '/task/:taskId', '/dataset/:datasetId'
    ],
    depositThreshold: 2000,
  };
  
  export default globalConfig;