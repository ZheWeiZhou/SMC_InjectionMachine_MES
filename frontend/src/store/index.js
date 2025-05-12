import { createStore } from 'vuex'
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();
export default createStore({
  state() {
    return {
      token: '',
      host: '140.135.106.49:8000'
    }
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      
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
    isLoggedIn() {
      const token = cookies.get('accesstoken');
      return !!token
    },
    getHost(state) {
        return state.host
    }
  }
})