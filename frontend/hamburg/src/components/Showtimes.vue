<template>
    <section v-if="error.length" class="section">
        <div class="notification is-danger">
            {{this.error}}
        </div>
    </section>
    <section v-else>
        <article>
            <div>
                <p>{{ this.cinemas.cinema_name }}</p>
                <p>{{ this.cinemas.distance }}</p>
                <ul class="list-unstyled" v-for="(_time, index) in this.cinemas.showings.Standard.times" :key="index">
                    <p>{{ _time.start_time }} - {{ _time.end_time }}</p>
                </ul>
            </div>
        </article>
    </section>
</template>

<script>
    export default {
        name: "Showtimes",
        mounted() {
            console.log("Showtimes mounted");
            this.getShowtimes();
        },
        updated() {
            console.log("Showtimes updated");
        },
        data() {
            return {
                endpoint: process.env.VUE_APP_SHOWTIMES_ENDPOINT + this._query + "&imdb_id=" + this.imdb_id + "&movie_name=" + this.movie_name,
                cinemas: '',
                error: '',
            }
        },
        props: {
            _query: '',
            movie_name: '',
            imdb_id: ''
        },
        methods: {
            getShowtimes() {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        this.cinemas = response.body.cinemas[0];
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
            getShowtimesDummy() {
                var dummy = {
                    "film": {
                    },
                    "cinemas": [
                        {
                            "cinema_id": 10506,
                            "cinema_name": "Harkins Tempe Marketplace 16",
                            "distance": 2.3831618641707,
                            "logo_url": "https://assets.movieglu.com/chain_logos/us/UK-397-sq.jpg",
                            "showings": {
                                "Standard": {
                                    "film_id": 247729,
                                    "film_name": "Venom",
                                    "times": [
                                        {
                                            "start_time": "10:00",
                                            "end_time": "12:17"
                                        },
                                        {
                                            "start_time": "12:35",
                                            "end_time": "14:52"
                                        },
                                        {
                                            "start_time": "15:15",
                                            "end_time": "17:32"
                                        },
                                        {
                                            "start_time": "17:50",
                                            "end_time": "20:07"
                                        },
                                        {
                                            "start_time": "20:30",
                                            "end_time": "22:47"
                                        },
                                        {
                                            "start_time": "23:00",
                                            "end_time": "01:17"
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "status": {
                    }
                }
                this.cinemas = dummy.cinemas[0];
                this.error = "";
            }
        }
    }
</script>

<style scoped>
</style>