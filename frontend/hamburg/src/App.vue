<template>
  <div id="app">
    <div id="nav">
      <!--<router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>-->
    </div>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<style lang="scss">

  @import url("https://fonts.googleapis.com/css?family=Raleway");

  body,
  h1,
  h2,
  h3,
  h4,
  h5 {
    font-family: "Raleway", sans-serif;
  }
  #app {
    font-family: "Raleway", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
