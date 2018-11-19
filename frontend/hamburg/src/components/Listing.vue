<template>
    <div>
        <section v-if="error.length">
            <div>
                {{ this.error }}
            </div>
        </section>
        <section v-else-if="this.results.length !== 0">
            <span class="typed">{{ this.type }} Movies</span>
            <div class="listed container-fluid">
                <div v-for="(result, index) in this.results" :key="index">
                    <keep-alive>
                        <b-link class="trendLink" v-bind:to="{name: 'details', params: {id: result.id}}">
                            <b-card-group class="d-flex flex-fill flex-row flex-now h-100" >
                                <b-card class="decked" v-bind:title='result.title'
                                        title-tag=h5
                                        v-bind:img-src="posterBase+result.poster_path"
                                        img-fluid
                                        img-alt="Img" 
                                        img-top
                                        align='center'/>
                            </b-card-group>
                        </b-link>
                    </keep-alive>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.getDetails()
        },
        name: 'Listing',
        data() {
            return {
                posterBase: process.env.VUE_APP_POSTER_BASE,
                results: '',
                type: '',
                error: ''
            }
        },
        props: [
            'endpoint'
        ],
        methods: {
            getDetails() {
                var _aux = this.endpoint.split(process.env.VUE_APP_DELIM);
                this.type = _aux[1];
                this.$http.get(_aux[0]).then(
                    function (response) {
                        this.results = response.body.results;
                        if (response.body.errors) {
                            this.error = response.body.errors[0];
                        } else {
                            this.error = "";
                        }
                    },
                    function (response) {
                    }
                );
            }
        }
    }
</script>

<style scoped>
.typed {
    color: white;
    font-size: 24px;
    text-shadow: 1px 1px 5px #333;
    margin: 35px 40px -5px;
}
.listed {
  padding: 24px;
  display: flex;
  overflow-x: scroll;
  text-decoration: none;
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
.trendLink {
  text-decoration: none;
  color: #333;
}
.vertical-scrollbar
{
   overflow-x: hidden; /*for hiding horizontal scroll bar*/
   overflow-y: auto; /*for vertical scroll bar*/
}
</style>
