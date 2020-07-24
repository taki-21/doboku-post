<template>
  <ul>
    <li>
      <div class="uk-grid-medium uk-flex-middle" uk-grid>
        <!-- <pre>{{ user }}</pre> -->
        <!-- <pre>{{ user.username }}</pre> -->
        <!-- <pre>{{ id }}</pre> -->
        <router-link class="router-link" to="/newpostpage">
          <div class="link">
            <i id="header_post_icon" uk-icon="pencil"></i>投稿する
          </div>
        </router-link>
        <div class="uk-inline">
          <a class="show_user">
            <div class="uk-card header_user_buttonuk-margin">
              <img class="user_icon" :src="'http://127.0.0.1:8000' + user.icon_image " />
              {{ username }}
              <i id="chevron-down" uk-icon="chevron-down"></i>
            </div>
          </a>
          <div uk-dropdown="pos: bottom-center; mode: click">
            <div class="dropdown">
              <router-link class="router-link" to="/mypage">
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
// import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      user: "",
      id: this.$store.getters["auth/id"]
    };
  },
  computed: {
    username: function() {
      return this.$store.getters["auth/username"];
    },
    isLoggedIn: function() {
      return this.$store.getters["auth/isLoggedIn"];
    }
    // id: function() {
    //   return this.$store.getters["auth/id"];
    // }
  },
  mounted() {
    this.axios
      .get("http://127.0.0.1:8000/api/v1/users/" + this.id + "/")
      .then(response => {
        this.user = response.data;
      });
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
.router-link{
  text-decoration: none;
}
.signup,
.header_post,
.show_user {
  font-size: large;
  font-weight: bold;
  color: #333333;
  text-decoration: none;
}

li {
  list-style: none;
}
.link {
  color: black;
  text-decoration: none;
}

.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

.uk-dropdown {
  display: none;
  position: absolute;
  z-index: 1020;
  box-sizing: border-box;
  min-width: 100px;
  width: 160px;
  padding: 10px 10px;
  background: #f7fcfc;
  color: #666;
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.15);
  border-radius: 5px;
}

.dropdown {
  text-align: center;
  width: 140px;
  margin: 10px auto;
}
</style>
