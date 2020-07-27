<template>
  <!-- メッセージエリア -->
  <div id="messages" class="Message">
    <div variant="danger" show v-show="message.error" class="mb-0">{{ message.error }}</div>
    <div variant="warning" show v-show="message.warnings.length > 0" class="mb-0">
      <p v-for="(warning, key) in message.warnings" v-bind:key="key" class="mb-0">{{ warning }}</p>
    </div>
    <div variant="info" show v-show="message.info" class="mb-0">{{ message.info }}</div>
  </div>
</template>

<script>
export default {
  computed: {
    message: function() {
      return this.$store.state.message;
    }
  }
};
</script>

<style scoped>
.Message{

  top: 0;
  width: 100%;
  max-width: 700px;
  z-index: 1000;
  transition: .3s ease-in-out;
}
</style>
