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
                    <p class="subtitle is-6 is-spaced"> {{result.release_date}}</p>
                </div>
            </div>
        </article>
    </section>
</template>
<script>
   export default {
       name: 'Search',
       data() {
           return { posterBase: process.env.VUE_APP_POSTER_BASE }
       },
       props: {
           results: {},
           error: ''
       }
   }
</script>
