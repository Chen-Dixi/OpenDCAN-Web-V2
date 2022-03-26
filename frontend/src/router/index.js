import {createRouter, createWebHistory} from "vue-router";

const Home = () => import('../views/Home.vue')
const Overview = () => import('../components/Overview.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const TaskList = () => import('../views/TaskList.vue')
const Datasets = () => import('../views/Datasets.vue')
const Play = () => import('../views/Play.vue')
const TaskView = () => import('../views/Task.vue')

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
            },{
                path: 'play',
                component: Play
            }
        ]
    },{
        path: '/task/:id',
        component: TaskView
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/register',
        component: Register
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes
});

export default router;