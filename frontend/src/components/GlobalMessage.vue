<template>
  <!-- メッセージエリア -->
  <div>
    <div variant="danger" id="error" class="message" show v-if="message.error">{{ message.error }}</div>
    <!-- <div variant="warning" show v-show="message.warnings.length > 0" class="mb-0"> -->
      <!-- <p v-for="(warning, key) in message.warnings" v-bind:key="key" class="mb-0">{{ warning }}</p> -->
    <!-- </div> -->
    <div variant="info" id="info" class="message" show v-if="message.info">{{ message.info }}</div>
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
.message{
  padding:0px 20px;
  text-align: center;
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  -webkit-transform: translateX(-50%);
  -ms-transform: translateX(-50%);
  font-size: 20px;
  font-weight: bold;
  z-index: 1000;
  border-radius: 3px;
  animation: fadein-keyframes 2s 0s 1 forwards;
}
#info {
  background-color: #bef5de;
}
#error{
  background-color: #f7e167;
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
.message#info{
  padding:0px 20px;
  position: absolute;
  top: 15px;
  font-size: 15px;
}
.message#error{
  padding:0px 10px;
  position: absolute;
  top: 8px;
  font-size: 15px;
}
}

</style>
