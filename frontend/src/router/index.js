import {createRouter, createWebHistory} from "vue-router";


const HelloWorld = () => import('../components/HelloWorld.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')

const routes = [
    {
        path: '/',
        component: HelloWorld
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