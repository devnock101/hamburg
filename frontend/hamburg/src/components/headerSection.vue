<template>
    <div id="headed">
        <header>
            <b-navbar class="myNavbar container-fluid">
                <b-container fluid>
                <!--Title-->
                    <b-navbar-brand v-bind:to="{name: 'home'}" class="title">BEVERLY BLVD</b-navbar-brand>
                    <!--Search Bar-->
                    <div class="searchForm col-auto">
                        <b-form @submit.prevent="getQuery()">
                            <b-input-group>
                                <b-form-input v-model="query" class="searchBar"
                                type="text" name="search" placeholder="Search..."/>
                            </b-input-group>
                        </b-form>
                    </div>
                    <transition name="slide-fade">
                        <!--Sign/In-->
                        <div fluid v-cloak class='signIn'>
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
                    <b-button class="hamburger .navbar-btn btn-link btn-lg" @click="show != show">☰</b-button>
                </b-container>
            </b-navbar>
        </header>
    </div>
</template>

<script>
export default {
    name: "headed",
    data: function() {
        return {
            results: {},
            query: '',
            error: ''
        };
    },
    methods: {
        getQuery: function() {
            this.$router.push({ name: "search", params: { queryFor: this.query }})
        }
    }
};
</script>

<style scoped>
.myNavbar {
  position: fixed;
  position: -webkit-fixed;
  top: 0;
  padding: 16px;
  background: white;
  box-shadow: 0px -4px 40px #777;
  z-index: 10;
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
.signIn {
    display: none;
}
</style>
