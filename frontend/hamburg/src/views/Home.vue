
<template>
  <div class="home">
    <landing/>
  </div>
</template>

<script>
import landing from "@/components/landingPage.vue";

export default {
  data() {
    return {
      name: "home"
    };
  },
  components: {
    landing,
  }
};
</script>

<style>
body {
  background-color: whitesmoke;
}
</style>
