
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
    landing,
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
