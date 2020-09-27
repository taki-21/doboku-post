<template>
  <div>
    <MyHeader />
    <!-- <GlobalMessage /> -->
    <!-- {{message}} -->
    <div class="uk-section uk-flex uk-flex-middle uk-animation-fade">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid>
            <div class="uk-width-1-1@m">
              <div
                id="signup_card"
                class="uk-margin uk-width-large uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
              >
                <h2 class="uk-card-title uk-text-center">新規登録</h2>
                <ValidationObserver v-slot="{ invalid }">
                  <form @submit.prevent="submitUser()">
                    <div>
                      <div class="uk-inline uk-width-1-1">
                        <ValidationProvider
                          mode="eager"
                          name="ユーザー名"
                          rules="required|max:10"
                          v-slot="{ errors }"
                        >
                          <span id="form_icon" class="uk-form-icon" uk-icon="icon: user"></span>
                          <input
                            class="uk-input"
                            type="text"
                            placeholder="ユーザー名"
                            v-model="username"
                            required
                          />
                          <span id="designated_message">: 10文字以下</span>
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div>
                      <div class="uk-inline uk-width-1-1">
                        <ValidationProvider
                          mode="lazy"
                          name="入力内容"
                          rules="required|email"
                          v-slot="{ errors }"
                        >
                          <span id="form_icon" class="uk-form-icon" uk-icon="icon: mail"></span>
                          <input
                            class="uk-input"
                            type="email"
                            placeholder="メールアドレス"
                            v-model="email_adress"
                            required
                          />
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                      <!-- {{email_adress}} -->
                    </div>
                    <div>
                      <div class="uk-inline uk-width-1-1">
                        <ValidationProvider
                          mode="lazy"
                          name="パスワード"
                          rules="required|min:8|password"
                          v-slot="{ errors }"
                          vid="password1"
                        >
                          <span id="form_icon" class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input
                            class="uk-input"
                            type="password"
                            placeholder="パスワード"
                            v-model="password1"
                            required
                          />
                          <span id="designated_message">: 8文字以上(半角英小文字、数字)</span>
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div>
                      <div class="uk-inline uk-width-1-1">
                        <ValidationProvider
                          mode="aggressive"
                          name="パスワード"
                          rules="required|confirmed:password1"
                          v-slot="{ errors }"
                        >
                          <span id="form_icon" class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input
                            class="uk-input"
                            type="password"
                            placeholder="パスワード（確認）"
                            v-model="password2"
                            required
                          />
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div>
                      <button
                        id="send_button"
                        class="uk-button uk-button-large uk-width-1-1"
                        :disabled="invalid"
                        type="submit"
                      >新規登録</button>
                    </div>
                  </form>
                </ValidationObserver>
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
import {
  ValidationProvider,
  ValidationObserver,
  extend,
  localize,
} from "vee-validate";
import ja from "vee-validate/dist/locale/ja.json";
import { required, max, min, email, confirmed } from "vee-validate/dist/rules";

extend("required", required);
extend("max", max);
extend("min", min);
extend("email", email);
extend("confirmed", confirmed);
extend("password", (password1) => {
  if (password1.match(/\d/) && password1.match(/[a-z]/)) {
    return true;
  }
  return "半角英小文字、数字をそれぞれ1種類以上含めてください";
});
localize("ja", ja);

export default {
  components: {
    MyHeader,
    ValidationProvider,
    ValidationObserver,
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
    submitUser() {
        api
          .post("/users/", {
            username: this.username,
            email: this.email_adress,
            password: this.password1,
          })
          .then((response) => {
            console.log("送信内容: " + response.data);
            this.autoLogin();
            // this.message = "送信しました！";
          })
          // .then(this.autoLogin())
          .catch((error) => {
            console.log("response: ", error.response.data);
          });
      },
    autoLogin: function () {
      this.isLoading = true;
      this.$store
        .dispatch("auth/login", {
          username: this.username,
          password: this.password1,
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
            this.Loading = false;
            // クエリ文字列に「next」がなければ、ホーム画面へ
            const next = this.$route.query.next || "/";
            this.$router.push(next).catch(() => {});
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

<style scoped>
#signup_card {
  background-color: rgba(151, 132, 116, 0.315);
  border-radius: 10px;
}
#form_icon {
  height: 40px;
}
#designated_message {
  font-size: 14px;
  color: gray;
}
#error_message {
  margin-top: 0;
  color: red;
}
#send_button {
  background-color: rgba(107, 86, 73, 0.404);
  font-size: 18px;
  color: rgb(0, 0, 0);
}
</style>
