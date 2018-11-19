<template>
    <div id="landing">
      <headed/>>
      <div id="border">  
        <b-carousel id="carousel"
                    controls
                    indicators
                    :interval="2500">
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
      <div class="sub">
        <h3 class="subtext">Trending Movies</h3>
      </div>
      <div class="trend container-fluid">
        <div v-for="(result, index) in trendz" :key="index">
            <b-link class="trendLink" v-bind:to="{name: 'details', params: {id: result.id}}">
              <b-card-group class="d-flex flex-fill flex-row flex-now h-100">
                <b-card class="decked" v-bind:title="result.title"
                        title-tag=h5
                        v-bind:img-src="backDropBase+result.poster_path"
                        img-fluid
                        img-alt="Img" 
                        img-top
                        align='center'/>
              </b-card-group>
            </b-link> 
        </div>
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
  filters:{
    limit: function(value) {
      value = value.toString()
      if (value.length > 20) {
        value = value.substring(0,10);
        value = value + "..."
      }
      return value
    }
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
.subtext {
  color: white;
  text-shadow: 1px 1px 5px #000;
}
.carousel {
  background-color: lightgrey;
  text-shadow: 1px 1px 2px #333;
  margin: 54px auto 0px;
  max-width: 100%;
  height: 650px;
  box-shadow: 0px 0px 40px #222;
  z-index: 1;
  image-rendering: optimizeSpeed;
}
.box {
  width: 105%;
  margin: 0px 0px 0px -15px;
  height: 650px;
  overflow: hidden;
}
.sub {
  margin: 35px 40px -5px;
}
.trend {
  padding: 24px;
  display: flex;
  overflow-x: scroll;
  text-decoration: none;
}
.trendLink {
  text-decoration: none;
  color: #333;
}
.decked {
  width: 220px;
  min-height: 220px;
  object-fit: contain;
  box-shadow: 0px 0px 40px #333;
  margin: 0px 25px;
  border-radius: 7px;
  image-rendering: optimizeSpeed;
  scroll-behavior: smooth;
}
.decked:hover {
  background-color: rgba(255,255,255,0.678);
}
.vertical-scrollbar
{
   overflow-x: hidden; /*for hiding horizontal scroll bar*/
   overflow-y: auto; /*for vertical scroll bar*/
}
</style>

