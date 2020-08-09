import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios' //追記
import VueAxios from 'vue-axios' //追記
import * as VueGoogleMaps from 'vue2-google-maps'

// Uikitの導入
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import 'uikit/dist/css/uikit.css'
import 'uikit/dist/css/uikit.min.css'


// vue_sessionの導入
import VueSession from 'vue-session'



UIkit.use(Icons);

Vue.config.productionTip = false
// Vue.config.productionTip = process.env.NODE_ENV === 'production'

Vue.use(VueSession)
Vue.use(VueAxios, axios) //追記

Vue.use(VueGoogleMaps, {
  load: {
    key: '',
    libraries: "places",
    v: 3.38,
    region: 'JP',
    language: 'ja'
  },
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
