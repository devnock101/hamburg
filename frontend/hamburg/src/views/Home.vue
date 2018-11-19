
<template>
  <div class="home">
    <div class="backgr">
      <b-img class="backbase" src="http://orig08.deviantart.net/2315/f/2011/035/6/4/imdb_top_250_movie_poster_by_saxon1964-d38rnod.jpg"/>
    </div>
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
.backgr {
  position: fixed;
  width: 101.1%;
  z-index: -99;
  background-color: rgba(0, 0, 0, 0.473);
}
.backbase {
  width: 102%;
  filter: blur(20px);
  margin: 0px -15px 0px;
  mix-blend-mode:overlay;
  image-rendering: optimizeSpeed;
}
.landing {
  z-index: 2;
}
</style>
