<template>
    <section v-if="error.length" class="section">
        <div class="notification is-danger">
            {{this.error}}
        </div>
    </section>
    <section v-else>
        <article>
            <div class="inTime container-fluid">
                <span>{{ this.cinemas.cinema_name }}</span>
                <span>{{ this.cinemas.distance }}</span>
                <ul class="list-unstyled" v-for="(_time, index) in this.cinemas.showings.Standard.times" :key="index">
                    <span>{{ _time.start_time }} - {{ _time.end_time }}</span>
                </ul>
            </div>
        </article>
    </section>
</template>

<script>
    export default {
        mounted() {
            this.getShowtimes();
        },
        name: "Showtimes",
        data() {
            return {
                cinemas: '',
                error: '',
                type: '',
            }
        },
        props: [
            'endpoint'
        ],
        methods: {
            getShowtimes() {
                var _aux = this.endpoint.split(process.env.VUE_APP_DELIM);
                this.type = _aux[1];
                this.$http.get(_aux[0]).then(
                    function (response) {
                        console.log(response);
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
            }
        }
    }
</script>

<style scoped>
.inTime {
    background-color: white;
    margin: 0px 30px 40px 30px;
}
</style>
