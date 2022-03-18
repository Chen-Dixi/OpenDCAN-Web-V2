import {createRouter, createWebHistory} from "vue-router";


const HelloWorld = () => import('../components/HelloWorld.vue')
const Login = () => import('../views/Login.vue')

const routes = [
    {
        path: '/',
        component: HelloWorld
    },
    {
        path: '/login',
        component: Login
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes
});

export default router;