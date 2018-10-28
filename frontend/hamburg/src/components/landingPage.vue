<template>
    <div id="landing">
      <headed/>>
      <div id="border">  
        <b-carousel id="carousel"
                    controls
                    indicators
                    :interval="4000">
              <div v-for="(result, index) in now" :key="index">
                <b-link class="movieLink" v-bind:to="{name: 'details', params: {id: result.id}}">  
                  <b-carousel-slide class="box">
                      <b-img slot="img" class="d-block img-fluid w-100" v-bind:src="backDropBase+result.backdrop_path" 
                        blank-color="#bbb" alt="image slot"/>
                      <h1>{{ result.title }}</h1>
                  </b-carousel-slide>
                </b-link>
              </div>
        </b-carousel>
      </div>
      <div class="trend container-fluid">
        <b-card-group deck>
          <div class="decked d-inline-flex flex-row flex-now" v-for="(result, index) in trendz" :key="index">
            <b-link v-bind:to="{name: 'details', params: {id: result.id}}">
              <b-card v-bind:title='result.title'
                      v-bind:img-src="backDropBase+result.poster_path"
                      img-alt="Img" 
                      img-top>
              </b-card>
            </b-link>
          </div>  
        </b-card-group>
      </div>
      <foot/>
    </div>
</template>

<script>
import headed from "@/components/headerSection.vue";
import foot from "@/components/footerSection.vue";

export default {
  name: "landing",
  data() {
    return {
      backDropBase: process.env.VUE_APP_POSTER_BASE,
      trendz: {},
      now: {},
      error_trendz: '',
      error_now:''
    };
  },
  components: {
    headed,
    foot
  },
  mounted: function() {
    this.getTrends(),
    this.getNow()
  },
  methods: {
    getTrends: function() {
      let trending = process.env.VUE_APP_POPULAR_ENDPOINT;
      this.$http.get(trending).then(
        function(response) {
          this.trendz = response.body.results;
          if (response.body.errors) 
          {
            this.error_trendz = response.body.errors[0];
          } 
          else 
          {
            this.error_trendz = "";
          }
         },
        function(response) {}
      );
    }
    ,
    getNow: function() {
      let playing = process.env.VUE_APP_NOW_PLAYING_ENDPOINT;
      this.$http.get(playing).then(
        function(response) {
          this.now = response.body.results;
          if (response.body.errors) 
          {
            this.error_now = response.body.errors[0];
          } 
          else 
          {
            this.error_now = "";
          }
         },
        function(response) {}
      );
    }
  }
}
</script>

<style scoped>

.carousel {
  text-shadow: 1px 1px 2px #333;
  margin: 75px auto 0px;
  max-width: 100%;
  height: 650px;
  box-shadow: 0px 0px 40px #777;
}
.box {
  width: 105%;
  margin: 0px 0px 0px -15px;
  height: 650px;
  overflow: hidden;
}
.trend {
  padding: 24px;
  overflow-x: hidden;
  display: flex;
}
.decked {
  width: 224px;
  height: 224px;
  object-fit: fill;
}
</style>

