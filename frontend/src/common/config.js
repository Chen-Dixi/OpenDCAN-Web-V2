// 前端可以用到的配置
let globalConfig = {
    cookieExpire: 60*30, // 30分钟
    backend_service_url: 'http://localhost:8000',
    allowedImageType: ['image/png', 'image/jpeg'],
    bgRouter: [
      '/login', '/register', '/datasets',
      '/forgetPassword', '/tasks', '/index'
    ],
    depositThreshold: 2000,
  };
  
  export default globalConfig;