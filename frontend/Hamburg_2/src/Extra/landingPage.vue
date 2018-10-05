<template>
    <div id="LandingPage">
        <div>
            <header>
                <b-navbar class="myNavbar w3-container w3-top w3-white w3-xlarge
                    w3-padding-16 w3-padding-small">
                    <b-container fluid>
                    <b-navbar-brand href="#" class="title">BEVERLY BVLD</b-navbar-brand>
                    <form @submit.prevent="searchString" class="searchForm">
                        <b-input-group>
                        <b-form-input v-model="text1" class="searchBar"
                            type="text" name="search" placeholder="Search..."/>
                        </b-input-group>  
                    </form>
                    <b-button class="hamburger w3-button w3-white btn-lg" @click="openSidebar()">☰</b-button>
                    </b-container>
                </b-navbar>
            </header>

            <b-card>
                
            </b-card>

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

<script>
export default {
  name: "LandingPage"
};
</script>

<style>
footer {
  position: absolute;
  width: 100%;
  bottom: 0px;
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
</style>
