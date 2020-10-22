<template>
  <v-app id="app">
    <div>
        <router-view />
    </div>
  </v-app>
</template>

<style>
@import "./assets/common.css";
html{
  overflow: overlay;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
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
