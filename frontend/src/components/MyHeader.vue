<template>
  <v-app-bar app color="blue-grey lighten-2">
    <v-app-bar-nav-icon class="d-none"></v-app-bar-nav-icon>
    <v-toolbar-title class="pl-0 pl-sm-5">
      <router-link to="/" id="title">
        <v-btn icon class="mb-2" depressed disabled>
          <v-img
            src="../assets/doboku.png"
            max-width="35px"
            max-height="35px"
          />
        </v-btn>
        DOBOKU_Post
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <HeaderSide />
  </v-app-bar>
</template>

<script>
import HeaderSide from "@/components/HeaderSide";
export default {
  components: {
    HeaderSide,
  },
};
</script>

<style scoped>
@import "../assets/common.css";

#title {
  text-decoration: none;
  font-size: 40px;
  font-family: "Economica";
  color: black;
}
</style>
