<template>
  <div id="login-page">
    <MyHeader />
    <GlobalMessage />

    <!-- メインエリア -->
    <div class="uk-section uk-flex uk-flex-middle uk-animation-fade">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid>
            <div class="uk-width-1-1@m">
              <div
                class="uk-margin uk-width-large uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
              >
                <h2 class="uk-card-title uk-text-center">ログイン</h2>
                <form @submit.prevent="submitLogin(form.username,form.password)">
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: user"></span>
                      <input
                        class="uk-input"
                        type="text"
                        v-model="form.username"
                        placeholder="ユーザー名"
                        required
                      />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: lock"></span>
                      <input
                        class="uk-input"
                        type="password"
                        v-model="form.password"
                        placeholder="パスワード"
                        required
                      />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <button
                      class="uk-button uk-button-primary uk-button-large uk-width-1-1"
                      type="submit"
                    >ログイン</button>
                  </div>
                  <div @click="submitLogin()">
                    <button class="uk-button uk-button-secondary uk-width-1-1">かんたんログイン</button>
                  </div>
                  <div class="uk-text-small uk-text-center" id="create_account">
                    登録していない方
                    <router-link class="router-link" to="/signup">アカウント作成</router-link>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import MyHeader from "@/components/MyHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";

export default {
  components: {
    MyHeader,
    GlobalMessage,
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      // id: this.$store.getters["auth/id"],
      isLoading: false,
    };
  },
  methods: {
    // ログインボタン押下
    submitLogin: function (username = "GuestUser", password = "testtest") {
      // ログイン
      this.isLoading = true;
      this.$store
        .dispatch("auth/login", {
          username: username,
          password: password,
        })
        .then(() => {
          if (this.isLoggedIn) {
            console.log("Login succeed.");
            this.$store.dispatch("message/setInfoMessage", {
              message: "ログインしました",
            });
            console.log("this.id: " + this.id);
            this.$store
              .dispatch("user/load", { id: this.id })
              .catch((error) => {
                if (process.env.NODE_ENV !== "production") console.log(error);
              });
          }
        })
        .catch((error) => {
          if (process.env.NODE_ENV !== "production") console.log(error);
        })
        .then(() => {
          this.Loading = false;
          // クエリ文字列に「next」がなければ、ホーム画面へ
          const next = this.$route.query.next || "/";
          this.$router.push(next).catch((error) => {
            // navigationが失敗するとエラーを吐くことを知った
            // test環境はどうしようか迷ったが今の所除外
            if (process.env.NODE_ENV === "development") console.log(error);
          });
        });

      // // クエリ文字列に「next」がなければ、ホーム画面へ
      // const next = this.$route.query.next || "/";
      // this.$router.replace(next);
    },
  },
  computed: {
    ...mapGetters("auth", {
      username: "username",
      isLoggedIn: "isLoggedIn",
      id: "id",
    }),
  },
};
</script>

<style scoped>
#create_account {
  margin-top: 20px;
}

</style>
