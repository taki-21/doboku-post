<template>
  <div id="app">
    <div>
      <transition appear>
        <router-view />
      </transition>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

.v-enter-active {
  transition: opacity 0.5s;
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
