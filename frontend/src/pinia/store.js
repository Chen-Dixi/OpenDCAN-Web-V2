import {defineStore} from 'pinia'
import {useCookies} from 'vue3-cookies'
const { cookies } = useCookies();

export const useUserStore = defineStore('user', {
    state:() => {
        return {
            // initial state
            isAdmin: false,
        }
    },
    getters: {
        isLoggedIn () {

            return cookies.isKey('access_token')
        },
        username (){
            return cookies.get('username')
        },
        accessToken (){
            return cookies.get('access_token')
        }
    }
})

// export default {
//     computed: {
//         ...mapStores(useUserStore),
//         ...mapState(useUserStore, ['isAdmin', 'name', 'logined'])
//     }
// }