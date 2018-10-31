import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
<<<<<<< HEAD
import MovieDetails from './views/MovieDetails.vue'
import Search from './components/searchResults.vue'
=======
import MovieDetails from './views/MovieDetails'
>>>>>>> development

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
<<<<<<< HEAD
    },
    {
        path: '/search/:queryFor',
        name: 'search',
        component: Search
=======
>>>>>>> development
    }
  ]
})
