<template>
  <div>
    <MyHeader />
    <!-- <GlobalMessage /> -->
    {{message}}
    <div class="uk-section uk-flex uk-flex-middle uk-animation-fade">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid>
            <div class="uk-width-1-1@m">
              <div
                class="uk-margin uk-width-large uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
              >
                <h2 class="uk-card-title uk-text-center">新規登録</h2>
                <form @submit.prevent="submitUser()">
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: user"></span>
                      <input
                        class="uk-input"
                        type="text"
                        placeholder="ユーザー名"
                        v-model="username"
                        required
                      />
                    </div>
                    {{username}}
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: mail"></span>
                      <input
                        class="uk-input"
                        type="email"
                        placeholder="メールアドレス"
                        v-model="email_adress"
                        required
                      />
                    </div>
                    {{email_adress}}
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: lock"></span>
                      <input
                        class="uk-input"
                        type="password"
                        placeholder="パスワード"
                        v-model="password1"
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
                        placeholder="パスワード（確認）"
                        v-model="password2"
                        required
                      />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <button
                      class="uk-button uk-button-primary uk-button-large uk-width-1-1"
                      type="submit"
                    >新規登録</button>
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
import MyHeader from "@/components/MyHeader.vue";
import { mapGetters } from "vuex";
import api from "@/services/api";

export default {
  components: {
    MyHeader,
  },
  data() {
    return {
      message: "",
      username: "",
      email_adress: "",
      password1: "",
      password2: "",
      isLoading: false,
      // isLoggedIn: true
    };
  },
  methods: {
    submitUser: function () {
      if (this.password1 == this.password2) {
        api
          .post("/users/", {
            username: this.username,
            email: this.email_adress,
            password: this.password1,
          })
          .then((response) => {
            console.log("送信内容: " + response.data);
            this.autoLogin()
            // this.message = "送信しました！";
          })
          // .then(this.autoLogin())
          .catch((error) => {
            console.log("response: ", error.response.data);
          });
      } else {
        this.message = "送信できませんでした";
      }
    },
    autoLogin: function () {
      this.isLoading = true;
      this.$store
        .dispatch("auth/login", {
          username: this.username,
          password: this.password1,
        })
        .then(() => {
          console.log("かか")
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
            this.Loading = false;
            // クエリ文字列に「next」がなければ、ホーム画面へ
            const next = this.$route.query.next || "/";
            this.$router.push(next)
            .catch(()=>{});
            // .catch((error) => {
              // navigationが失敗するとエラーを吐くことを知った
              // test環境はどうしようか迷ったが今の所除外
            //   if (process.env.NODE_ENV === "development") console.log(error);
            // });
          } else {
            console.log("ログインエラー");
          }
        })
        .catch((error) => {
          if (process.env.NODE_ENV !== "production") console.log(error);
        });
    },
  },
  computed: {
    ...mapGetters("auth", {
      // username: "username",
      isLoggedIn: "isLoggedIn",
      id: "id",
    }),
  },
};
</script>
