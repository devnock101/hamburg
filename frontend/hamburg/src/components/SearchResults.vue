<template>
    <div class="main">
        <div class="backbuild">
            <b-carousel id="background"
                        :interval="4000"
                        v-model="slide">
                <b-carousel-slide v-for="(result, index) in results" :key="index">
                    <b-img slot="img" class="back d-block img-fluid w-100" v-bind:src="posterBase+result.backdrop_path"
                           blank-color="#bbb" alt=""/>
                </b-carousel-slide>
            </b-carousel>
        </div>
        <div class="holder container-fluid">
            <section v-if="error.length" class="section">
                <div class="notification is-danger">
                    <b-card class="bucket">
                        <b-media tag="li" class="my-4">
                            <h2 class="mt-0 mt-1"><b>{{ "Error" }}</b></h2>
                            <p>{{ this.error }}</p>
                        </b-media>
                    </b-card>
                </div>
            </section>
            <section v-else class="section">
                <ul class="list-unstyled" v-for="(result, index) in results" :key="index">
                    <keep-alive>
                        <b-link class="movieLink" v-bind:to="{name: 'details', params: {id: result.id}}">
                            <transition name="fade">
                                <b-card class="bucket">
                                    <b-media tag="li" class="my-4">
                                        <b-img slot="aside" v-bind:src="posterBase+result.poster_path"
                                               height="256" width="170" blank-color="#bbb" alt="alt"/>
                                        <h5 class="mt-0 mt-1"><b>{{ result.title }}</b></h5>
                                        <p class='releaseDate'>{{ result.release_date }}</p>
                                        <p>{{ result.overview }}</p>
                                    </b-media>
                                </b-card>
                            </transition>
                        </b-link>
                    </keep-alive>
                </ul>
            </section>
        </div>
    </div>
</template>
<script>
    export default {
        name: 'Search',
        data() {
            return {posterBase: process.env.VUE_APP_POSTER_BASE}
        },
        props: {
            results: {},
            error: ''
        }
    }
</script>

<style>
    .backbuild {
        position: fixed;
        width: 105%;
        margin: -120px -50px;
        z-index: -99;
    }

    .back {
        -webkit-filter: blur(20px);
        filter: blur(20px);
    }

    .holder {
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
        box-shadow: 0px 0px 40px #777;
    }

    .bucket:hover {
        box-shadow: 0px 0px 20px #444;
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
