import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios' //追記
import VueAxios from 'vue-axios' //追記

import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import 'uikit/dist/css/uikit.css'
import 'uikit/dist/css/uikit.min.css'
UIkit.use(Icons);

Vue.config.productionTip = false

Vue.use(VueAxios, axios) //追記

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
