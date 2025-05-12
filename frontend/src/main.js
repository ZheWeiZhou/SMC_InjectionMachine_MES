import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import VueCookies from 'vue3-cookies'
import router from './router'
import store from './store'
loadFonts()

createApp(App)
  .use(store)
  .use(VueCookies)
  .use(router)
  .use(vuetify)
  .mount('#app')
