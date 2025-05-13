import { createStore } from 'vuex'
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();
export default createStore({
  state() {
    return {
      token: '',
      host: '140.135.106.49:8000',
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
      const token = cookies.get('accesstoken');
      return token
    },
    getselectmachine(state){
      
      return state.selectmachine
    },
    isLoggedIn() {
      const token = cookies.get('accesstoken');
      return !!token
    },
    getHost(state) {
        return state.host
    }
  }
})