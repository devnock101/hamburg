<template>
    <div>jdwijeinvceinenveivn</div>
</template>
<script>
    export default {
        mounted() {
            this.getDetails()
        },
        name: 'Listing',
        data(){
        },
        props: {
            results: {},
            error: '',
            endpoint:''
        },
        methods: {
            getDetails() {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        this.result = response.body;
                        console.log(this.result);
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

