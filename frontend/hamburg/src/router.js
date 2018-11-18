import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import MovieDetails from './views/MovieDetails.vue'
import Search from './components/SearchResults.vue'
import ExploreMovie from './views/ExploreMovie'

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
        },
        {
            path: '/search/:queryFor',
            name: 'search',
            component: Search
        },
        {
            path: '/explore/:id',
            name: 'explore',
            component: ExploreMovie
        }
    ]
})
