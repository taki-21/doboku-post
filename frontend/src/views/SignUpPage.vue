<template>
  <div>
    <v-container>
      <h3 class="h3 text-center pt-8">新規登録</h3>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card elevation="5" shaped color="blue-grey lighten-5">
            <div class="pa-8">
              <ValidationObserver v-slot="{ invalid }">
                <form @submit.prevent="submitUser()">
                  <ValidationProvider
                    mode="eager"
                    name="ユーザー名"
                    rules="required|max:10"
                    v-slot="{ errors }"
                  >
                    <v-text-field
                      v-model="username"
                      :counter="10"
                      :error-messages="errors"
                      required
                      placeholder="ユーザー名"
                      hint=": 10文字以下"
                      persistent-hint
                      prepend-inner-icon="mdi-account"
                    ></v-text-field>
                  </ValidationProvider>
                  <ValidationProvider
                    mode="lazy"
                    name="入力内容"
                    rules="required|email"
                    v-slot="{ errors }"
                  >
                    <v-text-field
                      v-model="email_adress"
                      :error-messages="errors"
                      required
                      placeholder="メールアドレス"
                      prepend-inner-icon="mdi-email"
                    ></v-text-field>
                  </ValidationProvider>
                  <ValidationProvider
                    mode="lazy"
                    name="パスワード"
                    rules="required|min:8|password"
                    v-slot="{ errors }"
                    vid="password1"
                  >
                    <v-text-field
                      v-model="password1"
                      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show1 ? 'text' : 'password'"
                      counter
                      :error-messages="errors"
                      required
                      placeholder="パスワード"
                      hint=": 8文字以上（半角英小文字,数字を含む）"
                      persistent-hint
                      @click:append="show1 = !show1"
                      prepend-inner-icon="mdi-lock"
                    ></v-text-field>
                  </ValidationProvider>
                  <ValidationProvider
                    mode="aggressive"
                    name="パスワード"
                    rules="required|confirmed:password1"
                    v-slot="{ errors }"
                  >
                    <v-text-field
                      v-model="password2"
                      :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show2 ? 'text' : 'password'"
                      counter
                      :error-messages="errors"
                      required
                      placeholder="パスワード（確認）"
                      @click:append="show2 = !show2"
                      prepend-inner-icon="mdi-lock"
                    ></v-text-field>
                  </ValidationProvider>
                  <v-btn
                    block
                    elevation="2"
                    class="mr-4 mt-4"
                    type="submit"
                    :disabled="invalid"
                  >
                    送信
                  </v-btn>
                </form>
              </ValidationObserver>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
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
      show1: false,
      show2: false,
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
              message: "登録完了",
            });
            console.log("this.id: " + this.id);
            this.$store
              .dispatch("user/load", { id: this.id })
              .catch((error) => {
                if (process.env.NODE_ENV !== "production") console.log(error);
              });
            this.isLoading = false;
            // クエリ文字列に「next」がなければ、ホーム画面へ
            const next = this.$route.query.next || "/";
            this.$router.push(next).catch(() => {});
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
      isLoggedIn: "isLoggedIn",
      id: "id",
    }),
  },
};
</script>
