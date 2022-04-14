// 前端可以用到的配置
let globalConfig = {
    cookieExpire: 60*60*20, // 20小时
    backend_service_url: 'http://localhost:8000',
    allowedImageType: ['image/png', 'image/jpeg'],
    bgRouter: [
      '/login', '/register', '/register/two',
      '/forgetPassword', '/forgetPassword/two',
    ],
    depositThreshold: 2000,
  };
  
  export default globalConfig;