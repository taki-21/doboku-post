<template>
  <div v-if="isLoggedIn && user.icon_image">
    <div>
      <!-- <div class="uk-inline"> -->
        <a class="show_user">
          <div class="uk-card header_user_buttonuk-margin">
            <img class="user_icon" :src="user.icon_image" />
            {{ user.username }}
            <i id="chevron-down" uk-icon="chevron-down"></i>
          </div>
        </a>
        <div uk-dropdown="pos: bottom-center; mode: click">
          <div class="dropdown">
            <router-link
              class="router-link uk-hidden-notouch"
              to="/newpostpage"
            >
              <v-icon>mdi-pencil</v-icon>
              投稿する
            </router-link>
          </div>
          <div class="dropdown">
            <router-link
              class="router-link"
              :to="{ name: 'mypage', params: { user_id: user.id } }"
              v-if="user.id"
            >
              <v-icon>mdi-account</v-icon>
              <span>マイページ</span>
            </router-link>
          </div>
          <div class="dropdown">
            <a href="#modal-logout" id="logout" uk-toggle>
              <v-icon>mdi-logout</v-icon>ログアウト
            </a>
            <div id="modal-logout" uk-modal>
              <div class="uk-modal-dialog uk-modal-body">
                <h2 class="uk-modal-title">ログアウト確認</h2>
                <p>ログアウトします。よろしいですか？</p>
                <p class="uk-text-right">
                  <button
                    class="uk-button uk-button-default uk-modal-close"
                    type="button"
                  >
                    キャンセル
                  </button>
                  <button
                    id="ok_button"
                    class="uk-button uk-button-default uk-modal-close"
                    type="button"
                    @click="clickLogout"
                  >
                    OK
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      <!-- </div> -->
    </div>
    <!-- </li> -->
    <!-- </ul> -->
  </div>
  <div v-else>
    <ul>
      <li>
        <div class="uk-grid-medium uk-flex-middle" uk-grid>
          <router-link class="router-link" to="/signup">
            <button class="uk-button header_button" id="signup_button">
              <i id="icon" uk-icon="plus-circle"></i>新規登録
            </button>
          </router-link>
          <router-link class="router-link" to="/login">
            <button class="uk-button header_button" id="login_button">
              <i id="icon" uk-icon="sign-in"></i>ログイン
            </button>
          </router-link>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  methods: {
    // ログアウトリンク押下
    clickLogout: function () {
      sessionStorage.clear();
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("user/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました",
      });
      this.$router.replace("/login");
    },
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser",
    }),
    isLoggedIn: function () {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },
};
</script>

<style scoped>
@import "../assets/common.css";
#post {
  padding-left: 0;
}

#userlist_button {
  background-color: rgba(204, 194, 149, 0.5);
}
#post_button {
  background-color: rgba(225, 225, 225, 0.5);
}
#signup_button {
  background-color: rgba(230, 160, 160, 0.4);
}
#login_button {
  background-color: rgba(150, 210, 200, 0.4);
}
.show_user {
  font-size: large;
  font-weight: bold;
  color: #333333;
  text-decoration: none;
}

li {
  list-style: none;
}

.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

#logout {
  color: black;
  text-decoration: none;
}

.dropdown {
  margin: 10px auto;
}

/* UIkitの上書き */
.uk-dropdown {
  position: absolute;
  text-align: center;
  z-index: 1020;
  box-sizing: border-box;
  min-width: 100px;
  width: 160px;
  padding: 10px 10px;
  background: #f7fcfc;
  color: #666;
  box-shadow: 0 20px 20px rgba(0, 0, 0, 0.15);
  border-radius: 5px;
}

.uk-modal-body {
  display: flow-root;
  padding: 30px 30px;
  border-radius: 5px;
}
@media (max-width: 640px) {
  #post {
    display: none;
  }
  .show_user {
    font-size: 18px;
    font-weight: bold;
    color: #333333;
    text-decoration: none;
  }

  .user_icon {
    width: 30px;
    height: 30px;
    margin-right: 5px;
    border-radius: 50%;
  }
  .uk-dropdown {
    position: absolute;
    text-align: center;
    z-index: 1000;
    box-sizing: border-box;
    min-width: 100px;
    width: 140px;
    padding: 5px 5px;
    background: #f3ffff;
    color: #666;
    box-shadow: 0 20px 20px rgba(0, 0, 0, 0.15);
    border-radius: 5px;
    font-size: 14px;
  }
  .header_button {
    height: 30px;
    line-height: 30px;
    padding: 0px 6px;
    font-size: 10px;
  }
  .router-link {
    padding-left: 8px;
  }
}
</style>
