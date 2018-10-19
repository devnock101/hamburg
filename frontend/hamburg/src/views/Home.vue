<template>
  <div class="home">
    <div class="container hero is-dark is-bold is-fullheight">
      <section class="section">
        <form class="field has-addons" v-on:submit.prevent="getResults()">
          <p class="control is-expanded">
            <input class="input is-rounded is-danger" v-model="query" type="text" placeholder="Search movies">
          </p>
          <div class="control is-fullwidth">
            <input class="button is-rounded is-danger" type="submit" value="search">
          </div>
        </form>
      </section>
      <search :results="results" :error="error"></search>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Search from '@/components/SearchResults.vue'

export default {
    data () {
       return {
          name: 'home',
          results: {},
          query: '',
          error: ''
       }
    },
  components: {
    Search
  },
  methods: {
    getResults() {
        let endpoint = process.env.VUE_APP_ENDPOINT + this.query;
        this.$http.get(endpoint).then(function(response) {
                this.results = response.body.results;
                if  (response.body.errors) {
                    this.error = response.body.errors[0];
                } else {
                    this.error = '';
                }
        }, function(response) {}
    )
  }
}
}
</script>
