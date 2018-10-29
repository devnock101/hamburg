<template>
    <div>
        <p>{{ this.type }}</p>
        <section v-if="error.length">
            <div>
                {{ this.error }}
            </div>
        </section>
        <section v-else-if="this.results.length !== 0">
            <div>
                <ul class="list-unstyled" v-for="(result, index) in this.results" :key="index">
                    <keep-alive>
                        <b-link class="movieLink" v-bind:to="{name: 'details', params: {id: result.id}}" >
                            <b-media tag="li" class="my-4">
                                <b-img slot="aside" v-bind:src="posterBase+result.poster_path"
                                       height="256" width="170" blank-color="#bbb" alt="alt"/>
                                <p class="mt-0 mt-1"><b>{{ result.title }}</b></p>
                            </b-media>
                        </b-link>
                    </keep-alive>
                </ul>
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
        props: {
            endpoint: '',
        },
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

</style>
