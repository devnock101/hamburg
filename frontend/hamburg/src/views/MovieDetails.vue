<template>
    <div class="movie">
        <headed/>
        <div v-if="error.length" class="section">
            <div class="notification is-danger">
                {{this.error}}
            </div>
        </div>
        <div v-else>
            <div>
                <div class="context conatiner-fluid">
                    <div class="backdrop">
                        <b-img class="backPoster" :src="imgsrc+result.backdrop_path"/>
                    </div>
                    <b-img class="moviePoster" :src="imgsrc+result.poster_path"/>
                    <div class="info">
                        <div class="mov0">
                            <span class="movTitle">{{ result.title }}</span>
                        </div>
                        <div class="mov1">
                            <span class="movTag" v-if="result.tagline">"{{ result.tagline }}"</span>
                        </div>
                        <div class="mov2">
                            <span class="movOverview">Overview</span>
                        </div>
                        <div class="mov3">
                            <span class="movContext">{{ result.overview }}</span>
                        </div>
                        <div class="mov4">
                            <span class="movRelease">Release Date : </span>
                            <span class="movDate">{{ result.release_date }}</span>
                            <span class="movTime">Duration : </span>
                            <span class="movDuration">{{ result.runtime }} min.</span>
                        </div>
                        <div class="mov5">
                            <span class="movPopu">Popularity : </span>
                            <span class="movPop">{{ result.popularity }} %</span>
                            <a class="movWeb" v-bind:href="result.homepage"><span>Movie Homepage</span></a>
                        </div>
                        <div class="mov6">
                            <span class="movAV">Average Vote : </span>
                            <span class="movAVote">{{ result.vote_average }}</span>
                            <span class="movVC">Vote Count : </span>
                            <span class="movVCount">{{ result.vote_count }}</span>
                        </div>
                        <br/>
                        <div class="mov7">
                            <b-btn class="movAV" v-bind:to="{name: 'explore', params: {mid: result.id}}">Explore
                                Movie
                            </b-btn>
                            <b-btn class="movVC" v-bind:to="{name: 'showtime', params: {sid: result.id, imdb:result.imdb_id, name: result.title}}">
                                View Showtimes
                            </b-btn>
                        </div>
                    </div>
                </div>
            </div>
            <div class="trailer container-fluid">
                <youtube class="vid" :video-id="result.video"/>
            </div>
            <div v-if="alert" class="mail conatiner-fluid d-flex flex-row flex-now">
                <span class="reminder">Get movie release alerts : </span>
                <form @submit.prevent="setAlert" class="searchForm">
                    <b-input-group>
                        <b-form-input v-model="email" v-validate="'required|email'" type="text" name="email"
                                      placeholder="Email" class="searchBar"/>
                        <span>{{ errors.first('email') }}</span>
                    </b-input-group>
                </form>
            </div>
            <div class="movs1">
                <Listing :endpoint="combine(endpoint_similar, 'Similar')"/>
            </div>
            <div class="movs2">
                <Listing :endpoint="combine(endpoint_recommended, 'Recommended')"/>
            </div>
        </div>
        <foot/>
    </div>
</template>

<script>
    import headed from "@/components/headerSection.vue";
    import foot from "@/components/footerSection.vue";
    import Listing from "@/components/Listing";

    export default {
        name: "MovieDetails",
        mounted: function () {
            this.getDetails();
        },
        updated: function () {
        },
        components: {
            headed,
            foot,
            Listing,
        },
        methods: {
            getDetails: function () {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        this.result = response.body;
                        this.endpoint_showtimes =
                            process.env.VUE_APP_SHOWTIMES_ENDPOINT +
                            this.result.id +
                            "&imdb_id=" +
                            this.result.imdb_id +
                            "&movie_name=" +
                            this.result.title;
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
            setAlert: function () {
                this.$validator.validateAll().then(response => {
                    if (response) {
                        this.$http
                            .post(process.env.VUE_APP_ALERT_ENDPOINT, {
                                email: this.email,
                                movie_name: this.result.title,
                                release_date: this.result.release_date
                            })
                            .then(function (response) {
                            });
                        alert("Alert Set!");
                    } else {
                        alert("Error in email.!");
                    }
                });
            },
            combine: function (_endpoint, _type) {
                return _endpoint + process.env.VUE_APP_DELIM + _type;
            },
            showShowtimes: function () {
                if (this.showtime_flag === false) {
                    this.showtime_flag = true;
                    this.showtime_text = "Hide Showtimes";
                } else {
                    this.showtime_flag = false;
                    this.showtime_text = "View Showtimes";
                }
            },
        },
        data: function () {
            return {
                endpoint: process.env.VUE_APP_DETAILS_ENDPOINT + this.$route.params.id,
                endpoint_similar:
                    process.env.VUE_APP_SIMILAR_ENDPOINT + this.$route.params.id,
                endpoint_recommended:
                    process.env.VUE_APP_RECOMMENDED_ENDPOINT + this.$route.params.id,
                endpoint_showtimes: "",
                imgsrc: process.env.VUE_APP_POSTER_BASE,
                result: "",
                error: "",
                alert: false,
                email: "",
                title: "",
                release_date: "",
                showtime_flag: false,
                showtime_text: "View Showtimes"
            };
        }
    };
</script>

<style scoped>
    .movie {
        width: 100%;
        overflow-x: hidden;
    }

    .backdrop {
        position: fixed;
        width: 101.1%;
        z-index: -99;
        background-color: rgba(0, 0, 0, 0.562);
    }

    .backPoster {
        width: 102%;
        margin: 0px -15px 0px;
        filter: blur(10px);
        mix-blend-mode: overlay;
        image-rendering: optimizeSpeed;
    }

    .context {
        position: relative;
        width: 100%;
        height: 700px;
        margin: 75px auto 0px;
        display: flex;
    }

    .moviePoster {
        position: relative;
        top: 15%;
        left: 20%;
        height: 450px;
        width: 300px;
        box-shadow: 0px 0px 40px #222;
        image-rendering: optimizeSpeed;
    }

    .info {
        position: relative;
        top: -4%;
        left: 30%;
        width: 600px;
    }

    .mov0 {
        position: relative;
        top: 18%;
    }

    .movTitle {
        position: relative;
        top: 20%;
        color: white;
        font-size: 36px;
        text-shadow: 1px 1px 5px #333;
        font-weight: bold;
    }

    .mov1 {
        position: relative;
        top: 20%;
    }

    .movTag {
        position: relative;
        top: 30%;
        left: 0%;
        color: white;
        font-size: 28px;
        text-shadow: 1px 1px 5px #333;
    }

    .mov2 {
        position: relative;
        top: 25%;
    }

    .movOverview {
        position: absolute;
        top: 0%;
        left: 0%;
        color: white;
        font-size: 24px;
        text-shadow: 1px 1px 5px #333;
    }

    .mov3 {
        position: relative;
        top: 32%;
    }

    .movContext {
        position: relative;
        top: 60%;
        left: 0%;
        width: 100%;

        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .mov4 {
        position: relative;
        top: 35%;
    }

    .movRelease {
        position: relative;
        top: 73%;
        left: 0%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
    }

    .movDate {
        position: relative;
        top: 73.5%;
        left: 2%;
        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .movTime {
        position: relative;
        top: 73%;
        left: 25%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
    }

    .movDuration {
        position: relative;
        top: 73.5%;
        left: 27%;
        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .mov5 {
        position: relative;
        top: 35%;
    }

    .movPopu {
        position: relative;
        top: 78%;
        left: 0%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
    }

    .movPop {
        position: relative;
        top: 78.5%;
        left: 2%;
        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .movWeb {
        position: relative;
        top: 78%;
        left: 32%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
        text-decoration: none;
    }

    .mov6 {
        position: relative;
        top: 35%;
    }

    .mov7 {
        position: relative;
        top: 35%;
    }

    .movAV {
        position: relative;
        top: 83%;
        left: 0%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
    }

    .movAVote {
        position: relative;
        top: 83.5%;
        left: 2%;
        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .movVC {
        position: relative;
        top: 83%;
        left: 35%;
        color: white;
        font-size: 20px;
        text-shadow: 1px 1px 5px #333;
    }

    .movVCount {
        position: relative;
        top: 83.5%;
        left: 37%;
        color: white;
        text-shadow: 1px 1px 5px #333;
    }

    .trailer {
        position: relative;
        left: 33%;
        height: 380px;
    }

    .vid {
        position: relative;
    }

    .made {
        position: relative;
        width: 100%;
        padding-top: 56px;
        padding-bottom: 48px;
    }

    .mail {
        position: relative;
        width: 100%;
        padding-top: 56px;
        padding-bottom: 48px;
        left: -8%;
    }

    .reminder {
        position: relative;
        left: 30%;
        color: white;
        font-size: 24px;
        text-shadow: 1px 1px 5px #333;
    }

    .searchForm {
        position: relative;
        left: 34%;
        width: 30%;
    }

    .movs1 {
        max-height: 550px;
    }

    .movs2 {
        max-height: 550px;
    }

    .show {
        background-color: whitesmoke;
        color: black;
        border: none;
        margin: 0px 30px 40px 30px;
    }

    .show:hover {
        background-color: lightgrey;
    }
</style>
