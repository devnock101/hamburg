import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueResource from 'vue-resource'

require('process');
if (process.env.NODE_ENV !== 'production') {
    Vue.config.productionTip = process.env.NODE_ENV === 'production';
}

Vue.use(VueResource);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
