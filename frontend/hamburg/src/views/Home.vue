
<template>
  <div class="home">
    <b-img class="backbase" src="http://orig08.deviantart.net/2315/f/2011/035/6/4/imdb_top_250_movie_poster_by_saxon1964-d38rnod.jpg"/>
    <landing/>
  </div>
</template>

<script>
import landing from "@/components/landingPage.vue";

export default {
  data() {
    return {
      name: "home"
    };
  },
  components: {
<<<<<<< HEAD
    landing,
=======
    //landing,
    Search,
    foot
  },
  methods: {
    getResults() {
      let endpoint = process.env.VUE_APP_SEARCH_ENDPOINT + this.query;
      this.$http.get(endpoint).then(
        function(response) {
          this.results = response.body.results;
          if (response.body.errors) {
            this.error = response.body.errors[0];
          } else {
            this.error = "";
          }
        },
        function(response) {}
      );
    }
>>>>>>> development
  }
};
</script>

<style scoped>
.backbase {
  background-color: rgba(0, 0, 0, 0.562);
  position: fixed;
  z-index: -99;
  filter: blur(35px);
  mix-blend-mode:overlay;
}
.landing {
  z-index: 2;
}
</style>
