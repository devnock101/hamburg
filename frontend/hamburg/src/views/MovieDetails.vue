<template>
    <div>
        <section v-if="error.length" class="section">
            <div class="notification is-danger">
                {{this.error}}
            </div>
        </section>
        <section v-else>
            <article>
                <figure>
                    <p>
                        <youtube :video-id="result.video"></youtube>
                    </p>
                </figure>
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
        <showtimes :_query="result.id" :imdb_id="result.imdb_id" :movie_name="result.title"></showtimes>
    </div>
</template>

<script>
    import Showtimes from  "@/components/Showtimes.vue";
    export default {
        mounted() {
            this.getDetails()
        },
        methods: {
            getDetails() {
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
            setAlert() {
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
        data() {
            return {
                endpoint: process.env.VUE_APP_DETAILS_ENDPOINT + this.$route.params.id,
                result: {},
                error: '',
                alert: false,
                email: '',
                title: '',
                release_date: ''
            };
        },
        components: {
            Showtimes
        }
    }
</script>

<style scoped>
</style>