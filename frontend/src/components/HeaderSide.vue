<template>
  <ul>
    <li>
      <div class="uk-grid-medium uk-flex-middle" uk-grid>
        <router-link to="/newpostpage">
          <div class="link">
            <i id="header_post_icon" uk-icon="pencil"></i>投稿する
          </div>
        </router-link>
        <div class="uk-inline">
          <a class="show_user">
            <div class="uk-card header_user_buttonuk-margin">
              <img class="user_icon" />
              {{ username }}
              <i
                id="chevron-down"
                uk-icon="chevron-down"
              ></i>
            </div>
          </a>
          <div uk-dropdown="pos: bottom-center; mode: click">
            <div class="dropdown">
              <router-link to="/mypage">
                <div class="link">
                  <i id="mypage_icon" uk-icon="user"></i>
                  <span>マイページ</span>
                </div>
              </router-link>
            </div>
            <div class="dropdown">
              <a href="#modal-logout" class="logout link" uk-toggle @click="clickLogout">
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
  // data(){
  //   user: null
  // },
  computed: {
    username: function() {
      return this.$store.getters["auth/username"];
    },
    isLoggedIn: function() {
      return this.$store.getters["auth/isLoggedIn"];
    }
  },
  // mounted() {
  //   this.axios.get("http://127.0.0.1:8000/api/v1/users/").then(response => {
  //     this.user = response.data;
  // });
  // },
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
.link {
  color: black;
  text-decoration: none;
}
</style>
