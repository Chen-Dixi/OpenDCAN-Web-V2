import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import ContentFilter from './components/ContentFilter.vue'
import UploadDropdownMenu from './components/UploadDropdownMenu.vue'
import VueCookies from 'vue3-cookies'
import {useCookies} from 'vue3-cookies'
import 'element-plus/dist/index.css'
import './assets/css/main.css'
import router from './router'
import globalConfig from './common/config'


const app = createApp(App)
const {cookies} = useCookies()
app
    .component('content-filter', ContentFilter)
    .component('upload-dataset-dropdown-menu', UploadDropdownMenu)
    .use(ElementPlus)
    .use(VueCookies)
    .use(router)

router.beforeEach((to, from, next) => {
    let isLoggedIn = cookies.isKey('access_token');
    let allowRouter = globalConfig.bgRouter
    if (!isLoggedIn && allowRouter.indexOf(to.path) < 0) {
        next({path: '/login'})
    } else if (isLoggedIn && to.path === '/login') {
        next({path: '/index'})
    } else {
        next()
    }
});


app.mount('#app') //mount 不返回应用本身。相反，它返回的是根组件实例vm(viewmodel)。