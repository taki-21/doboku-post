import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios' //追記
import VueAxios from 'vue-axios' //追記

// Uikitの導入
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import 'uikit/dist/css/uikit.css'
import 'uikit/dist/css/uikit.min.css'

// Vuetifyの導入
import Vuetify from 'vuetify'

// vue_sessionの導入
import VueSession from 'vue-session'



UIkit.use(Icons);

Vue.config.productionTip = false
// Vue.config.productionTip = process.env.NODE_ENV === 'production'

const vuetifyOption = {}
Vue.use(VueSession)
Vue.use(Vuetify)
Vue.use(VueAxios, axios) //追記

new Vue({
  router,
  store,
  vuetify: new Vuetify(vuetifyOption),
  render: h => h(App)
}).$mount('#app')
