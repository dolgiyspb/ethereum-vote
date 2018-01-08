// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from "bootstrap-vue"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"
import VueResource from "vue-resource"
import 'chart.js'
import 'hchs-vue-charts'
import VeeValidate from 'vee-validate'
import {Validator} from 'vee-validate'

Validator.extend('private-key', {
  getMessage: field => 'The ' + field + ' value is not truthy.',
  validate: value => false
});

Vue.use(VeeValidate)
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueResource)
Vue.use(window.VueCharts)

Vue.http.options.root = '/api';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
