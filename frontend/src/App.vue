<template>
  <v-app>
    <v-app-bar app color="blue-grey lighten-2">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title
        ><router-link to="/" id="title"
          >DOBOKU_Post</router-link
        ></v-toolbar-title
      >
      <v-spacer></v-spacer>
      <router-link class="router-link" id="post" to="/newpostpage">
        <v-btn depressed elevation="3" color="brown lighten-2"
          ><v-icon>mdi-pencil-outline</v-icon>投稿する</v-btn
        >
      </router-link>
      <nav>
        <HeaderSide />
      </nav>
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

export default {
  components: {
    HeaderSide,
    GlobalMessage,
  },
};
</script>
<style>
@import "./assets/common.css";

html {
  overflow: overlay;
}
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
} */
#title {
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
