<template>
    <div class="movie">
        <headed/>
        <section v-if="error.length" class="section">
            <div class="notification is-danger">
                {{this.error}}
            </div>
        </section>
        <section v-else>
            <div>
                <div class="backdrop container-fluid">
                    <b-img class="backPoster" :src="imgsrc+result.backdrop_path"/>
                </div>
                <div class="context conatiner-fluid d-inline-flex flex-row flex-now">
                    <b-img class="moviePoster" :src="imgsrc+result.poster_path"/>
                    <div class="info">
                        <span class="movTitle">{{ result.title }}</span>
                        <span class="movOverview">Overview</span>
                        <span class="movContext">{{ result.overview }}</span>
                        <span class="movRelease">Release Date : </span>
                        <span class="movDate">{{ result.release_date }}</span>
                        <span class="movTag" v-if="result.tagline">"{{ result.tagline }}"</span>
                        <span class="movTime">Duration : </span>
                        <span class="movDuration">{{ result.runtime }} min.</span>
                        <span class="movPopu">Popularity : </span>
                        <span class="movPop">{{ result.popularity }} %</span>
                        <a class="movWeb" v-bind:href="result.homepage"><span>Website</span></a>
                        <span class="movAV">Average Vote : </span>
                        <span class="movAVote">{{ result.vote_average }}</span>
                        <span class="movVC">Vote Count : </span>
                        <span class="movVCount">{{ result.vote_count }}</span>
                    </div>
                </div>
            </div>
            <div class="trailer container-fluid">
                <youtube :video-id="result.video"></youtube>
            </div>
        </section>
        <section v-if="alert" class="mail conatiner-fluid d-inline-flex flex-row flex-now">
            <span class="reminder">Get movie release alerts : </span>
            <form @submit.prevent="setAlert" class="searchForm">
                <b-input-group>
                    <b-form-input v-model="email" v-validate="'required|email'" type="text" name="email"
                                  placeholder="Email" class="searchBar"/>
                    <span>{{ errors.first('email') }}</span>
                </b-input-group>
            </form>
        </section>
        <Listing :endpoint = "combine(endpoint_similar, 'Similar')"/>
        <Listing :endpoint = "combine(endpoint_recommended, 'Recommended')"/>
        <div>
            <button v-on:click="showShowtimes()">{{ showtime_text }}</button>
            <div v-if="this.showtime_flag">
                <Showtimes :endpoint="combine(endpoint_showtimes, 'Showtimes')"></Showtimes>
            </div>
        </div>
        <foot/>
    </div>
</template>

<script>
    import headed from "@/components/headerSection.vue";
    import foot from "@/components/footerSection.vue";
    import Listing from "@/components/Listing"
    import Showtimes from "@/components/Showtimes.vue";

    export default {
        name: 'MovieDetails',
        mounted: function () {
            console.log("MovieDetails beforeCreate");
            this.getDetails()
        },
        updated: function () {
            console.log("MovieDetails Updated");
        },
        components: {
            headed,
            foot,
            Listing,
            Showtimes
        },
        methods: {
            getDetails: function () {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        this.result = response.body;
                        this.endpoint_showtimes = process.env.VUE_APP_SHOWTIMES_ENDPOINT + this.result.id + "&imdb_id=" + this.result.imdb_id + "&movie_name=" + this.result.title;
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
                        this.$http.post(process.env.VUE_APP_ALERT_ENDPOINT, {
                            email: this.email,
                            movie_name: this.result.title,
                            release_date: this.result.release_date
                        }).then(
                            function (response) {
                            }
                        );
                        alert('Alert Set!')
                    } else {
                        alert('Error in email.!')
                    }
                })
            },
            combine(_endpoint, _type) {
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
            }
        },

        data() {
            return {
                endpoint: process.env.VUE_APP_DETAILS_ENDPOINT + this.$route.params.id,
                endpoint_similar: process.env.VUE_APP_SIMILAR_ENDPOINT + this.$route.params.id,
                endpoint_recommended: process.env.VUE_APP_RECOMMENDED_ENDPOINT + this.$route.params.id,
                endpoint_showtimes: '',
                imgsrc: process.env.VUE_APP_POSTER_BASE,
                result: '',
                error: '',
                alert: false,
                email: '',
                title: '',
                release_date: '',
                showtime_flag: false,
                showtime_text: 'View Showtimes'
            };
        }
    }
</script>

<style scoped>
.backdrop {
    position: fixed;
    height: 1200px;
    width: 101.1%;
    margin: 75px -15px;
    
    z-index: -99;
    background-color: rgba(0, 0, 0, 0.562);
}
.backPoster {
    width: 105%;
    height: auto;
    margin: -5px -15px 0px;
    filter: blur(10px);
    mix-blend-mode:overlay;
}
.context {
    position: relative;
    width: 100%;
    height: 600px;
    margin: 75px auto 0px;
}
.moviePoster {
    position: relative;
    top: 15%;
    left: 22%;
    height: 450px;
    width: 300px;
    box-shadow: 0px 0px 40px #222;
}
.info {
    position: relative;
    top: -4%;
    left: 30%;
    width: 600px;
}
.movTitle {
    position: absolute;
    top: 20%;
    color: white;
    font-size: 36px;
    text-shadow: 1px 1px 5px #333;
    font-weight: bold;

}
.movOverview {
    position: absolute;
    top: 46%;
    color: white;
    font-size: 24px;
    text-shadow: 1px 1px 5px #333;
}
.movContext {
    position: absolute;
    top: 54%;
    width: 110%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.movRelease {
    position: absolute;
    top: 68%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
}
.movDate {
    position: absolute;
    top: 68.5%;
    left: 25%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.movTag {
    position: absolute;
    top: 34%;
    color: white;
    font-size: 28px;
    text-shadow: 1px 1px 5px #333;
}
.movTime {
    position: absolute;
    top: 68%;
    left: 60%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
}
.movDuration {
    position: absolute;
    top: 68.5%;
    left: 78%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.movPopu {
    position: absolute;
    top: 75%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
}
.movPop {
    position: absolute;
    top: 75.5%;
    left: 25%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.movWeb {
    position: absolute;
    top: 75%;
    left: 60%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
    text-decoration: none;
}
.movAV {
    position: absolute;
    top: 82%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
}
.movAVote {
    position: absolute;
    top: 83%;
    left: 25%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.movVC {
    position: absolute;
    top: 82%;
    left: 60%;
    color: white;
    font-size: 20px;
    text-shadow: 1px 1px 5px #333;
}
.movVCount {
    position: absolute;
    top: 83%;
    left: 80%;
    color: white;
    text-shadow: 1px 1px 5px #333;
}
.trailer {
    position: relative;
    left: 33%;
    height: 380px;
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
    left:-8%;
}
.reminder {
    position: relative;
    left:32%;
    color: white;
    font-size: 24px;
    text-shadow: 1px 1px 5px #333;
}
.searchForm {
    position: relative;
    left: 34%;
    width: 30%;
}
</style>
