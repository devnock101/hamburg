<template>
    <div class="movie">
        <section v-if="error.length" class="section">
            <div class="notification is-danger">
                {{this.error}}
            </div>
        </section>
        <section v-else>
            <article>
                <div class="layer">
                    <b-img blank blank-color="#777" alt="img"/>
                </div>
                <div class="backdrop container-fluid">
                    <b-img class="backPoster" :src="imgsrc+result.backdrop_path"/>
                </div>
                <div class="trailer container-fluid">
                    <youtube :video-id="result.video"></youtube>
                </div>
                <div>
                    <div>
                        <a v-bind:href="result.homepage"><h4>{{ result.homepage }}</h4></a>
                        <p>{{ result.title }}</p>
                        <p>{{ result.popularity }}</p>
                        <p>{{ result.overview }}</p>
                        <p>{{ result.release_date }}</p>
                        <p>{{ result.runtime }}</p>
                        <p>{{ result.tagline }}</p>
                        <p>{{ result.vote_average }}</p>
                        <p>{{ result.vote_count }}</p>
                    </div>
                </div>
            </article>
        </section>
        <section v-if="alert" class="section">
            <form @submit.prevent="setAlert" class="searchForm">
                <b-input-group>
                    <b-form-input v-model="email" v-validate="'required|email'" type="text" name="email"
                                  placeholder="Email" class="searchBar"/>
                    <span>{{ errors.first('email') }}</span>
                </b-input-group>
            </form>
        </section>
    </div>
</template>

<script>
    export default {
        mounted: function() {
            this.getDetails()
        },
        methods: {
            getDetails: function() {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        this.result = response.body;
                        this.alert = Date.now() < Date.parse(this.result.release_date);
                        if (response.body.errors) {
                            this.error = response.body.errors[0];
                        } else {
                            this.error = "";
                        }
                    },
                    function (response) {
                    }
                );
            },
            setAlert: function() {
                this.$validator.validateAll().then(response => {
                    if (response) {
                        this.$http.post(process.env.VUE_APP_ALERT_ENDPOINT, {
                            email: this.email,
                            movie_name: this.result.title,
                            release_date: this.result.release_date
                        }).then(
                            function (response) {
                            }
                        )
                    } else {
                        alert('Error in email.!')
                    }
                })
            }
        },
        data: function() {
            return {
                endpoint: process.env.VUE_APP_DETAILS_ENDPOINT + this.$route.params.id,
                imgsrc: process.env.VUE_APP_POSTER_BASE,
                result: {},
                error: '',
                alert: false,
                email: '',
                title: '',
                release_date: ''
                };
            }
        }
</script>

<style scoped>
.backdrop {
    position: fixed;
    height: 650px;
    width: 105%;
    margin: auto -15px;
    overflow: hidden;
    z-index: -99;
}
.backPoster {
    height: 1200px;
    object-fit: cover;
    filter: blur(10px);
}
.layer {
    position: fixed;
    width: 105%;
    height: 650px;
    z-index: 1;
}
.trailer {
    position: relative;
    z-index: 2;
}
</style>
