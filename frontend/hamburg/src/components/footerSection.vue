<template>
    <!--footer-->
        <div id="foot">
          <footer class="base">
            <b-row>
              <b-col class="left">
                <p>Pallavi Bahl</p>
                <p>Sakhi Gautam</p>
              </b-col>
              <b-col class="center">
                <h2>Team Hamburg</h2>
                <p>Aman Kaushik</p>
              </b-col>
              <b-col class="right">
                <p>Summan Parlapalli</p>
                <p>Abhishek Gupta</p>
              </b-col>
            </b-row>
          </footer>
        </div>
</template>

<script>
export default {
  name: "foot"
};
</script>


<style>
.base {
  position: relative;
  padding: 32px;
  background-color: darkgrey;
  bottom: 0;
  width: 100%;
  box-shadow: 0px -5px 40px lightgray;
}
.left, .center, .right {
  text-align: center;
  padding: 20px;
}
</style>
