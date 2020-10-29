<template>
  <div>
    <v-alert
      dense
      type="success"
      class="message"
      border="left"
      elevation="8"
      dark
      show
      v-if="message.success"
    >
      {{ message.success }}
    </v-alert>

    <v-alert
    dense
      type="info"
      class="message"
      border="left"
      elevation="8"
      dark
      show
      v-if="message.info"
    >
      {{ message.info }}
    </v-alert>
    <v-alert
      dense
      type="warning"
      class="message"
      border="left"
      elevation="8"
      dark
      show
      v-if="message.warning"
    >
      {{ message.warning }}
    </v-alert>
    <v-alert
    dense
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
