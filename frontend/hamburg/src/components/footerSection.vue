<template>
    <!--footer-->
        <div id="foot">
          <footer class="base">
            <b-row>
              <b-col class="left">
                <br>
                <h5>Pallavi Bahl</h5>
                <br>
                <h5>Sakhi Gautam</h5>
              </b-col>
              <b-col class="center">
                <h2>Team Hamburg</h2>
                <br>
                <h5>Aman Kaushik</h5>
              </b-col>
              <b-col class="right">
                <br>
                <h5>Summan Parlapalli</h5>
                <br>
                <h5>Abhishek Gupta</h5>
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
  background-color: white;
  bottom: 0;
  width: 100%;
  box-shadow: 0px -5px 40px #777;
}
.left, .center, .right {
  text-align: center;
  padding: 20px;
}
</style>
