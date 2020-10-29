<template>
  <v-app>
    <MyHeader />
    <GlobalMessage />
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import MyHeader from "@/components/MyHeader";
import GlobalMessage from "@/components/GlobalMessage";

export default {
  components: {
    MyHeader,
    GlobalMessage,
  },
};
</script>
<style>
::-webkit-scrollbar-thumb {
  background-color: rgba(208, 210, 212, 0.993);
  border-right: none;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar {
  width: 10px;
}
/* html {
  overflow: overlay;
} */
/* v-app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
} */

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
@media (min-width: 960px){
.container {
    max-width: 1200px;
}}
</style>
