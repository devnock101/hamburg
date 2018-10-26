<template>
    <section   v-if="error.length" class="section">
        <div class="notification is-danger">
            {{this.error}}
        </div>
    </section>
    <section  v-else class="section">
        <article class="media" v-for="result in results">
            <figure class="media-left">
                <p class="image is-256x256">
                    <img v-bind:src="posterBase+result.poster_path ">
                </p>
            </figure>
            <div class="media-content ">
                <div class="content">
                    <a><h4 class="title is-4 is-spaced">{{ result.title }}</h4></a>
                    <p class="subtitle is-6 is-spaced">{{ result.overview }}</p>
                    <p class="subtitle is-6 is-spaced">{{ result.cast}}</p>
                    <p class="subtitle is-6 is-spaced">{{ result.overview }}</p>
                    <p class="subtitle is-6 is-spaced"> {{result.release_date}}</p>
                </div>
            </div>
        </article>
    </section>
    <!--<form class="field has-addons" v-on:submit.prevent="getResults()">-->
        <!--<p class="control is-expanded">-->
            <!--<input class="input is-rounded is-danger" v-model="query" type="text" placeholder="Search movies">-->
        <!--</p>-->
        <!--<div class="control is-fullwidth">-->
            <!--<input class="button is-rounded is-danger" type="submit" value="search">-->
        <!--</div>-->
    <!--</form>-->
</template>

<script>
    export default {
        name: "MovieDetails",
        methods: {
            getResults() {
                let endpoint = process.env.VUE_APP_ENDPOINT + this.movieId;
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
            // ,setReminder(){}
        },
        props: {

            movieId: ''
        }
    }
</script>

<style scoped>

</style>