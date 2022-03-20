import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import ContentFilter from './components/ContentFilter.vue'
import DatasetListCell from './components/DatasetListCell.vue'
import 'element-plus/dist/index.css'
import router from './router/index'

const app = createApp(App)
app
    .component('content-filter', ContentFilter)
    .component('dataset-cell', DatasetListCell)
    .use(ElementPlus)
    .use(router)
    .mount('#app')
    
