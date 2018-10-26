<template>
  <div class="home">
    <header>
      <b-navbar class="myNavbar container-fluid">
        <b-container fluid>
          <!--Title-->
          <b-navbar-brand href="#" class="title">BEVERLY BLVD</b-navbar-brand>
          <!--Search Bar-->
          <div class="searchForm">
            <b-form @submit.prevent="getResults()">
              <b-input-group>
                <b-form-input v-model="query" class="searchBar"
                  type="text" name="search" placeholder="Search..."/>
              </b-input-group>
            </b-form>
          </div>
          <transition name="slide-fade">
             <!--Sign/In-->
              <div fluid v-if="show">
                <b-form inline>
                  <label class="sr-only" for="inlineFormInputName2">Name</label>
                  <b-input class="navForm mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Username" />
                  <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
                  <b-input-group left="@" class="mb-2 mr-sm-2 mb-sm-0">
                    <b-input class="navForm" id="inlineFormInputGroupUsername2" placeholder="Password" />
                  </b-input-group>
                  <b-form-checkbox class="mb-2 mr-sm-2 mb-sm-0">Remember me</b-form-checkbox>
                </b-form>
              </div>
          </transition>
          <!--Hamburger Button-->
          <b-button class="hamburger .navbar-btn btn-link btn-lg" @click="show = !show">☰</b-button>
        </b-container>
      </b-navbar>
    </header>
    <landing :results="results"/>
    <Search :results="results" :error="error"/>
    <foot/>
  </div>
</template>

<script>
import landing from "@/components/landingPage.vue";
import Search from "@/components/SearchResults.vue";
import foot from "@/components/footerSection.vue";

export default {
  data() {
    return {
      name: "home",
      results: {},
      query: '',
      error: ''
    };
  },
  components: {
    //landing,
    Search,
    foot
  },
  methods: {
    getResults: function() {
      let endpoint = process.env.VUE_APP_ENDPOINT + this.query;
      this.$http.get(endpoint).then(
        function(response) {
          this.results = response.body.results;
          if (response.body.errors) {
            this.error = response.body.errors[0];
          } else {
            this.error = "";
          }
        },
        function(response) {}
      );
    }
  }
};
</script>

<style>
body {
  background-color: whitesmoke;
}
.myNavbar {
  position: fixed;
  position: -webkit-fixed;
  top: 0;
  padding: 16px;
  background: white;
  box-shadow: 0px -4px 40px #777;
  z-index: 3;
}
.title {
  position: relative;
  font-size: 24px;
}
.searchForm {
  width: 50%;
  min-width: 20%;
}
.searchBar {
  border: 0;
  box-shadow: 0px 1px 2px rgb(150, 150, 150);
  background-color: rgba(0, 0, 0, 0) !important;
}
.searchBar:hover {
  background-color: rgba(238, 238, 238, 0.747) !important;
}
.searchBar:focus {
  box-shadow: 0px 1px 2px rgb(150, 150, 150);
}
.navForm {
  position: relative;
  border: 0;
  box-shadow: 0px 1px 2px rgb(150, 149, 149);
  background-color: rgba(0, 0, 0, 0) !important;
}
.navForm:hover {
  background-color: rgba(238, 238, 238, 0.747) !important;
}
.navForm:focus {
  box-shadow: 0px 1px 2px rgb(150, 149, 149);
}
.hamburger {
  position: relative;
  border: none;
  color: black;
  text-decoration: none !important;
}
.hamburger:focus,
.hamburger:active {
  outline: none !important;
  box-shadow: none;
}
</style>
