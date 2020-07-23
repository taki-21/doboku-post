<template>
  <ul>
    <li>
      <div class="uk-grid-medium uk-flex-middle" uk-grid>
        <a class="header_post">
          <i id="header_post_icon" uk-icon="pencil"></i>投稿する
        </a>
        <div class="uk-inline">
          <a class="show_user">
            <div class="uk-card header_user_buttonuk-margin">
              <img class="user_icon" src />
              {{ username }}
              <i id="chevron-down" uk-icon="chevron-down"></i>
            </div>
          </a>
          <div uk-dropdown="pos: bottom-center; mode: click">
            <div class="dropdown">
              <a href class="username">
                <i id="mypage_icon" uk-icon="user"></i>マイページ
              </a>
            </div>
            <div class="dropdown">
              <a href="#modal-logout" class="logout" uk-toggle @click="clickLogout">
                <i id="logout_icon" uk-icon="sign-out"></i>ログアウト
              </a>
            </div>
          </div>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  computed: {
    username: function() {
      return this.$store.getters["auth/username"];
    },
    isLoggedIn: function() {
      return this.$store.getters["auth/isLoggedIn"];
    }
  },
  methods: {
    // ログアウトリンク押下
    clickLogout: function() {
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました。"
      });
      this.$router.replace("/login");
    }
  }
};
</script>
<style scoped>
.signup,
.header_post,
.show_user {
  font-size: large;
  font-weight: bold;
  color: #333333;
}

li {
  list-style: none;
}

</style>
