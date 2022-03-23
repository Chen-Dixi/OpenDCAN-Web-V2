import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import ContentFilter from './components/ContentFilter.vue'
import DatasetListCell from './components/DatasetListCell.vue'
import UploadDropdownMenu from './components/UploadDropdownMenu.vue'
import 'element-plus/dist/index.css'
import './assets/css/main.css'
import router from './router/index'

const app = createApp(App)
app
    .component('content-filter', ContentFilter)
    .component('dataset-cell', DatasetListCell)
    .component('upload-dataset-dropdown-menu', UploadDropdownMenu)
    .use(ElementPlus)
    .use(router)
    .mount('#app') //mount 不返回应用本身。相反，它返回的是根组件实例vm(viewmodel)。
    
