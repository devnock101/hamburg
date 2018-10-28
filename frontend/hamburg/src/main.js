import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueResource from 'vue-resource'
import VueYouTubeEmbed from 'vue-youtube-embed'
import VeeValidate from 'vee-validate';

require('process');
if (process.env.NODE_ENV !== 'production') {
    Vue.config.productionTip = process.env.NODE_ENV === 'production';
}

Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(VueYouTubeEmbed);
Vue.use(VeeValidate);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
