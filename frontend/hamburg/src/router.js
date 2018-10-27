import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import MovieDetails from './views/MovieDetails'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
        path: '/movie/:id',
        name: 'details',
        component: MovieDetails
    }
  ]
})
