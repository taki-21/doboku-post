<template>
  <!-- ヘッダナビゲーション -->
  <div id="header">
    <div type="dark" variant="dark">
      <a class="navbar-brand" href="/">DRF Sample</a>
      <div class="ml-auto" v-if="$route.meta.requiresAuth">
        <div right v-if="isLoggedIn">
          <template slot="button-content">{{ username }}</template>
          <div href="#" @click="clickLogout">ログアウト</div>
        </div>
        <div href="#" @click="clickLogin" v-else>ログイン</div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    computed: {
      username: function () {
        return this.$store.getters['auth/username']
      },
      isLoggedIn: function () {
        return this.$store.getters['auth/isLoggedIn']
      }
    },
    methods: {
      // ログアウトリンク押下
      clickLogout: function () {
        this.$store.dispatch('auth/logout')
        this.$store.dispatch('message/setInfoMessage', { message: 'ログアウトしました。' })
        this.$router.replace('/login')
      },
      // ログインリンク押下
      clickLogin: function () {
        this.$store.dispatch('message/clearMessages')
        this.$router.replace('/login')
      }
    }
  }
</script>
