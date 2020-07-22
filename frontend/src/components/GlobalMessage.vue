<template>
  <!-- メッセージエリア -->
  <div id="messages">
    <div variant="danger" show v-show="message.error" class="mb-0">
      {{ message.error }}
    </div>
    <div
      variant="warning" show v-show="message.warnings.length > 0" class="mb-0">
      <p v-for="(warning, key) in message.warnings" class="mb-0" v-bind:key='key'>{{ warning }}</p>
    </div>
    <div variant="info" show v-show="message.info" class="mb-0">
      {{ message.info }}
    </div>
  </div>
</template>

<script>
  export default {
    computed: {
      message: function () {
        return this.$store.state.message
      }
    }
  }
</script>
