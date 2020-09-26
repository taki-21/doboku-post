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
UIkit.use(Icons);

// // //vee-validateの導入
// import {
//   ValidationProvider,
//   extend
// } from 'vee-validate';

// // Add a rule.
// extend('secret', {
//   validate: value => value === 'example',
//   message: 'This is not the magic word'
// });

// // Register it globally
// Vue.component('ValidationProvider', ValidationProvider);

// vue-sessionの導入
import VueSession from 'vue-session'

// vue-infinite-loadingの導入
import InfiniteLoading from 'vue-infinite-loading';
Vue.use(InfiniteLoading);



Vue.config.productionTip = false
Vue.config.productionTip = process.env.NODE_ENV === 'production'

Vue.use(VueSession)
Vue.use(VueAxios, axios) //追記

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
