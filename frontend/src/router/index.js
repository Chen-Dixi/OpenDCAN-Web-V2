import {createRouter, createWebHistory} from "vue-router";

const Home = () => import('../views/Home.vue')
const HelloWorld = () => import('../components/HelloWorld.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const TaskList = () => import('../views/TaskList.vue')
const Datasets = () => import('../views/Datasets.vue')
const Play = () => import('../views/Play.vue')

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
                name: 'HelloWorld',
                component: HelloWorld
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