<template>
  <div>
    <v-alert
      type="error"
      class="message"
      border="left"
      elevation="8"
      dark
      show
      v-if="message.error"
    >
      {{ message.error }}
    </v-alert>
    <v-alert
      dense
      type="success"
      class="message"
      border="left"
      elevation="8"
      dark
      show
      v-if="message.info"
    >
      {{ message.info }}
    </v-alert>
  </div>
</template>

<script>
export default {
  computed: {
    message: function () {
      return this.$store.state.message;
    },
  },
};
</script>

<style scoped>
.message {
  text-align: center;
  position: absolute;
  top: 10px;
  left: 50%;
  min-width: 40%;
  transform: translateX(-50%);
  -webkit-transform: translateX(-50%);
  -ms-transform: translateX(-50%);
  /* font-size: 20px; */
  font-weight: bold;
  z-index: 1000;
  animation: fadein-keyframes 2s 0s 1 forwards;
}

@keyframes fadein-keyframes {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
@media (max-width: 640px) {
  .message {
    font-size: 15px;
  }
}
</style>
