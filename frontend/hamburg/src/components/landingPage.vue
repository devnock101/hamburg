<template>
    <div id="landing">
      <div id="border">  
        <b-carousel id="carousel"
                    controls
                    indicators
                    :interval="4000"
                    v-model="slide"
        >
              <b-link class="movieLink" href="#" v-for="(result, index) in results" :key="index">  
                <b-carousel-slide>
                    <b-img slot="img" class="d-block img-fluid w-100" v-bind:src="backDropBase+result.backdrop_path" 
                      blank-color="#bbb" alt="image slot"/>
                    <h1>{{ result.title }}</h1>
                </b-carousel-slide>
              </b-link>
        </b-carousel>
      </div>
      <div class="trend container-fluid">
        
      </div>  
    </div>
</template>

<script>
export default {
  name: "landing",
  data() {
    return {
      backDropBase: process.env.VUE_APP_POSTER_BASE
    };
  },
  props: {
    results: {}
  }
};
</script>

<style>
.carousel {
  text-shadow: 1px 1px 2px #333;
  margin: 75px auto 0px;
  box-shadow: 0px 0px 40px #333;
}
.carousel.img-fluid {
  object-fit: cover;
  max-width: 100%;
  height: 650px;
}
</style>

