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
html{
  overflow: overlay;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}
::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-thumb {
  background-color: rgba(208, 210, 212, 0.993);
  /* border: 1px solid #ccc; */
  border-right: none;
}
::-webkit-scrollbar-track {
  background: transparent;
}

/* ::-webkit-scrollbar {
  display: none;
  -webkit-appearance: none;
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
</style>
