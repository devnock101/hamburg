<template>
  <div id="app">
    <SearchPage />
  </div>
</template>

<script>
import SearchPage from './components/searchPage.vue'

export default {
  name: 'app',
  components: {
    SearchPage
  }
}
</script>

<style>
@import url("https://www.w3schools.com/w3css/4/w3.css");
@import url("https://fonts.googleapis.com/css?family=Raleway");

body,h1,h2,h3,h4,h5 {
  font-family: "Raleway", sans-serif;
}
.w3-quarter img {
  margin-bottom: -6px;
  cursor: pointer
}
.w3-quarter img:hover {
  opacity: 0.6;
  transition: 0.3s
}
#app {
  font-family: "Raleway", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
