import Vue from 'vue'
import Router from 'vue-router'
import Search from './components/searchPage.vue'
import Lister from './components/Lister.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Search',
      component: Search
    },
    {
      path: '/lister',
      name: 'lister',
      component: Lister
    }
  ]
})