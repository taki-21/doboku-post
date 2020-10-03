<template>
  <div v-if="isLoggedIn">
    <ul>
      <li>
        <div class="uk-grid-medium uk-flex-middle" uk-grid>
          <!-- <pre>{{ user.username }}</pre> -->
          <!-- <pre>{{ id }}</pre> -->
          <router-link class="router-link" to="/newpostpage">
            <div class="link">
              <i id="header_post_icon" uk-icon="pencil"></i>投稿する
              <!-- <pre>{{ user }}</pre> -->
            </div>
          </router-link>
          <div class="uk-inline">
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
                  class="router-link"
                  :to="{ name: 'mypage', params: { user_id: user.id } }"
                  v-if="user.id"
                >
                  <div class="link">
                    <i id="mypage_icon" uk-icon="user"></i>
                    <span>マイページ</span>
                  </div>
                </router-link>
              </div>
              <div class="dropdown">
                <a href="#modal-logout" class="logout link" uk-toggle>
                  <i id="logout_icon" uk-icon="sign-out"></i>ログアウト
                </a>
                <div id="modal-logout" uk-modal>
                  <div class="uk-modal-dialog uk-modal-body">
                    <h2 class="uk-modal-title">ログアウト確認</h2>
                    <p>ログアウトします。よろしいですか？</p>
                    <p class="uk-text-right">
                      <button
                        id="cancel_button"
                        class="uk-button uk-button-default uk-modal-close"
                        type="button"
                      >
                        キャンセル
                      </button>
                      <button
                        class="uk-button uk-button-primary uk-modal-close"
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
          </div>
        </div>
      </li>
    </ul>
  </div>
  <div v-else>
    <ul>
      <li>
        <!-- <pre>{{ id }}</pre> -->
        <div class="uk-grid-medium uk-flex-middle" uk-grid>
          <router-link class="router-link" to="/signup">
            <div class="link">
              <i id="signup_icon" uk-icon="plus-circle"></i>新規登録
            </div>
          </router-link>
          <router-link class="router-link" to="/login">
            <div class="link">
              <i id="login_icon" uk-icon="sign-in"></i>ログイン
            </div>
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
      // var result = window.confirm("ログアウトします。よろしいですか？");
      // if (result) {
      sessionStorage.clear();
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("user/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました",
      });
      this.$router.replace("/login");
      // }
    },
  },
  computed: {
    // 1:storeのuserModule, 2:このコンポーネント内で使えるcomputed, 3:userModuleのgetters
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
.router-link {
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
.uk-modal-body {
  display: flow-root;
  padding: 30px 30px;
  border-radius: 5px;
}
#cancel_button {
  margin-right: 10px;
}
</style>
