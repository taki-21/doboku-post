<template>
  <v-container>
    <h3 class="h3 text-center pt-8">ログイン</h3>
    <v-row justify="center">
      <v-col justify="center">
        <v-card
          elevation="5"
          shaped
          color="blue-grey lighten-5"
          class="mx-auto"
          max-width="500px"
        >
          <div class="pa-8">
            <form @submit.prevent="submitLogin(form.username, form.password)">
              <v-text-field
                v-model="form.username"
                required
                placeholder="ユーザー名"
                prepend-inner-icon="mdi-account"
              ></v-text-field>
              <v-text-field
                v-model="form.password"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show1 ? 'text' : 'password'"
                required
                placeholder="パスワード"
                @click:append="show1 = !show1"
                prepend-inner-icon="mdi-lock"
              ></v-text-field>
              <v-btn block elevation="2" class="mr-4 mt-4" type="submit">
                ログイン
              </v-btn>
            </form>
            <v-btn
              block
              color="blue-grey lighten-3"
              elevation="2"
              class="mr-4 mt-4"
              @click="submitLogin()"
            >
              かんたんログイン
            </v-btn>
            <div class="pa-4 text-center">
              登録していない方
              <router-link id="to_signup" class="router-link" to="/signup"
                >アカウント作成</router-link
              >
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      show1: false,
    };
  },
  methods: {
    // ログインボタン押下
    submitLogin(username = "GuestUser", password = "test09876") {
      this.form.username = username;
      this.form.password = password;
      // ログイン
      this.$store
        .dispatch("auth/login", {
          username: username,
          password: password,
        })
        .then(() => {
          if (this.isLoggedIn) {
            console.log("ログイン成功");
            this.$store.dispatch("message/setInfoMessage", {
              message: "ログインしました",
            });
            console.log("this.id: " + this.id);
            this.$store
              .dispatch("user/load", { id: this.id })
              .catch((error) => {
                if (process.env.NODE_ENV !== "production") console.log(error);
              });
            // クエリ文字列に「next」がなければ、ホーム画面へ
            const next = this.$route.query.next || "/";
            this.$router.push(next).catch(() => {});
          } else {
            console.log("ログイン失敗");
            this.$store.dispatch("message/setErrorMessage", {
              message: "ユーザー名、もしくはパスワードが間違っています",
            });
          }
        })
        .catch((error) => {
          if (process.env.NODE_ENV !== "production") console.log(error);
        });
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
