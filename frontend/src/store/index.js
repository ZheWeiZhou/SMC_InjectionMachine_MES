import { createStore } from 'vuex'
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();
export default createStore({
  state() {
    return {
      token: '',
      host: '/api',
      // host: 'http://140.135.106.49:8000',
      selectmachine: cookies.get('setSelectMachine')  || 'Engel-120'
    }
  },
  mutations: {
    setSelectMachine(state, name) {
      state.selectmachine = name
      
    },
    clearToken(state) {
      state.token = ''
    }
  },
  getters: {
    getToken() {
      var token = cookies.get('accesstoken');
      return token
    },
    getselectmachine(state){
      
      return state.selectmachine
    },
    isLoggedIn() {
      var token = cookies.get('accesstoken');
      return !!token
    },
    getHost(state) {
        return state.host
    }
  }
})
