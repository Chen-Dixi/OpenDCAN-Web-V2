import {createRouter, createWebHistory} from "vue-router";

const Home = () => import('../views/Home.vue')
const Overview = () => import('../components/Overview.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const TaskList = () => import('../views/TaskList.vue')
const Datasets = () => import('../views/Datasets.vue')
const TaskView = () => import('../views/Task.vue')
const TaskDatasetSection = () => import('../section/TaskDatasetSection.vue')
const TaskPlaySection = () => import('../section/TaskPlaySection.vue')
const TaskTrainSection = () => import('../section/TaskTrainSection.vue')
const NotFound = () => import('../views/404.vue')

const routes = [
    {
        path: '/',
        redirect: '/index'
    },{
        path: '/',
        name: 'Home',
        component: Home,
        children:[
            {
                path: '/index',
                name: 'Overview',
                component: Overview
            },{
                path: 'tasks',
                component: TaskList
            },{
                path: 'datasets',
                component: Datasets
            }
        ]
    },{
        path: '/task/:taskId',
        component: TaskView,
        children: [
            {
                path: 'dataset',
                name: 'task-dataset-section',
                component: TaskDatasetSection
            },{
                path: 'train',
                component: TaskTrainSection
            },
            {
                name: 'play',
                path: 'play',
                component: TaskPlaySection
            },{
                path: '',
                redirect: {name: 'task-dataset-section'}
            }
        ]
    },
    {
        path: '/login',
        component: Login
    },
    {
      path: '/404',
      name: 'NotFound',
      component: NotFound
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/:pathMatch(.*)*',
        hidden: true,
        redirect: {path: '/404'}
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes
});

export default router;