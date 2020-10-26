<template>
  <v-app>
    <v-app-bar app color="blue-grey lighten-2">
      <v-app-bar-nav-icon class="d-none"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link to="/" id="title">
          <v-btn icon class="mb-2" disable>
            <v-img
              src="./assets/doboku.png"
              max-width="35px"
              max-height="35px"
            />
          </v-btn>
          DOBOKU_Post
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <HeaderSide/>
    </v-app-bar>
    <GlobalMessage />
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import HeaderSide from "./components/HeaderSide";
import GlobalMessage from "@/components/GlobalMessage.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    HeaderSide,
    GlobalMessage,
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser",
    }),
    ...mapGetters("user", {
      user: "getUser",
    }),
    isLoggedIn: function () {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },
};
</script>
<style>
@import "./assets/common.css";

/* html {
  overflow: overlay;
} */
/* v-app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
} */
#title {
  height: 50px;
  text-decoration: none;
  color: black;
  font-size: 40px;
  font-family: "Economica";
}

.v-enter-active {
  transition: opacity 0.4s;
}
.v-enter {
  opacity: 0;
}
.v-enter-to {
  opacity: 1;
}
.v-leave,
.v-leave-active,
.v-leave-to {
  opacity: 0;
}
</style>
