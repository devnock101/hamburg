<template>
    <div class="main container-fluid">
        <div class="holder">  
            <section   v-if="error.length" class="section">
                <div class="notification is-danger">
                    <b-card class="bucket">
                    <b-media tag="li" class="my-4">
                        <h2 class="mt-0 mt-1"><b>{{ "Error" }}</b></h2>
                        <p>{{ this.error }}</p>
                    </b-media>
                    </b-card>
                </div>
            </section>
            <section  v-else class="section">
                <ul class="list-unstyled">
                    <b-link class="movieLink" href="#" v-for="(result, index) in results" :key="index">
                    <b-card class="bucket">
                        <b-media tag="li" class="my-4">
                        <b-img-lazy slot="aside" v-bind:src="posterBase+result.poster_path" 
                            height="256" width="170" blank-src="@/assets/alt.png" blank-color="#bbb" alt="alt"/>
                        <h5 class="mt-0 mt-1"><b>{{ result.title }}</b></h5>
                        <p class='releaseDate'>{{ result.release_date }}</p>
                        <p>{{ result.overview }}</p>
                        </b-media>
                    </b-card>  
                    </b-link>
                </ul>
            </section>
        </div>    
    </div>
</template>
<script>
   export default {
       name: 'Search',
       data() {
           return { posterBase: process.env.VUE_APP_POSTER_BASE }
       },
       props: {
           results: {},
           error: ''
       }
   }
</script>

<style>
.main {
  position: relative;
  margin: 105px auto 10px;
  align-items: center;
  height: 100%;
  width: 60%;
  z-index: 2;
}
.bucket {
  padding: 10px;
  margin: 20px auto;
  box-shadow: 0px 0px 40px lightgray;
}
.bucket:hover {
  box-shadow: 0px 0px 20px darkgrey;
}
.movieLink {
  text-decoration: none;
  color: #333;
}
.movieLink:hover {
  text-decoration: none;
  color: #07b;
}
</style>
