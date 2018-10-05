<template>
  <div id="SearchPage">

    <!--Header-->
    <header>
      <b-navbar class="myNavbar w3-container w3-top w3-white w3-xlarge
        w3-padding-16 w3-padding-small">
        <b-container fluid>
          <!--Title-->
          <b-navbar-brand href="#" class="title">BEVERLY BVLD</b-navbar-brand>
          <!--Search Bar-->
          <form @submit.prevent="getResults" class="searchForm">
            <b-input-group>
              <b-form-input v-model="query" class="searchBar"
                type="text" name="search" placeholder="Search..."/>
              </b-input-group>  
          </form>
          <!--Hamburger Button-->
          <b-button class="hamburger w3-button w3-white btn-lg" @click="openSidebar()">☰</b-button>
        </b-container>
      </b-navbar>
    </header>

    <!--Hamburger Menu / Sidebar-->
    <div>
      <nav class="mySidebar w3-sidebar w3-bar-block w3-black
        w3-animate-right w3-top w3-text-light-grey w3-large" 
        v-bind:style="{ display: unHide}" id="mySidebar" ref="mySidebar">
        <a href="javascript:void()" @click="closeSidebar()"
          class="w3-bar-item w3-button w3-center w3-padding-32">CLOSE</a>
        <a href="#" @click="closeSidebar()"
          class="w3-bar-item w3-button w3-center w3-padding-16">ABOUT US</a>
        <a href="#contact" @click="closeSidebar()"
          class="w3-bar-item w3-button w3-center w3-padding-16">CONTACT</a>
      </nav>
      <div v-bind:class="{ bar: unHide }"/>
    </div>
    
    <!--Content-->
    <div class="main container-fluid">
      <div class="holder">
        <section  v-if="error.length">
          <div>
            <b-card class="bucket">
              <b-media tag="li" class="my-4">
                <b-img slot="aside" v-bind:src="posterBase+result.poster_path" 
                  height="144" width="96" alt="placeholder" />
                <h5 class="mt-0 mt-1"><b>{{ result.title }}</b></h5>
                <p>{{this.error}}</p>
              </b-media>
            </b-card>
          </div>
        </section>
        <section  v-else>  
          <ul class="list-unstyled">
            <b-card class="bucket" v-for="(result, index) in res2.results" :key="index">
              <b-media tag="li" class="my-4">
                <b-img slot="aside" v-bind:src="posterBase+result.poster_path" 
                  height="144" width="96" alt="placeholder" />
                <h5 class="mt-0 mt-1"><b>{{ result.title }}</b></h5>
                <p>{{ result.overview }}</p>
                <p><b>Released Date:</b> {{ result.release_date }}</p>
              </b-media>
            </b-card>  
          </ul>
        </section>  
      </div>
    </div>

    <!--footer-->
    <div>
      <footer class="foot w3-container w3-padding-32 w3-grey">
        <div class="w3-row-padding">
          <div class="teamInfo1 w3-third">
            <br><br><br>
            <p>Pallavi Bahl</p>
            <p>Sakshi Gautam</p>
          </div>
          <div class="teamInfo2 w3-third">
            <h2>Team Hamburg</h2>
            <br><br>
            <p>Aman Kaushik</p>
          </div>
          <div class="teamInfo3 w3-third">
            <br><br><br>
            <p>Summan Parlapalli</p>
            <p>Abhishek Gupta</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script >
export default{
  name: 'SearchPage',
  data() {
    return {
      unHide: 'none',
    };
  },
};
</script>

<style>
.myNavbar {
  position: sticky;
  top: 0px;
  align-items: center;
  box-shadow: 0px -4px 40px rgb(146, 145, 145);
 }
.title {
  position: relative;
  font-size: 24px;
}
.searchForm {
  width: 50%;
}
.searchBar {
  position: relative;
  right: 70px;
  border: 0;
  box-shadow: 0px 1px 2px rgb(150, 149, 149);
  background-color:rgba(0,0,0,0) !important;
}
.searchBar:hover {
  background-color:rgba(238, 238, 238, 0.747) !important;
}
.searchBar:focus {
  box-shadow: 0px 1px 2px rgb(150, 149, 149);
}
.searcher {
  position: relative;
  background-color:rgba(0,0,0,0) !important;
  border: none;
}
.hamburger {
  position: relative;
  border: none;
  text-decoration: none !important
}
.hamburger:focus,.hamburger:active {
   outline: none !important;
   box-shadow: none;
}
.mySidebar {
  position: relative;
  z-index:3;
  max-width:250px;
  font-weight:bold;
  right:0;
  text-decoration: none !important
}
.main {
  position: relative;
  margin: 100px auto 30px;
  align-items: center;
  height: 100%;
  width: 60%;
}
.bucket {
  padding: 10px;
  margin: 20px auto;
  box-shadow: 0px 0px 40px lightgray;
}
footer {
  position: relative;
  width: 100%;
  box-shadow: 0px -5px 40px lightgray;
  }
.teamInfo1 {
  text-align: left;
}
.teamInfo2 {
  text-align: center;
}
.teamInfo3 {
  text-align: right;
}
#main {
    transition: margin-left .5s;
    padding: 20px;
}
</style>
