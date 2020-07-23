<template>
  <div id="login-page">
    <MyHeader />
    <!-- <GlobalMessage /> -->

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
                <form @submit.prevent="submitLogin">
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: user"></span>
                      <input class="uk-input" type="text" v-model="form.username" placeholder="ユーザー名" required />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: lock"></span>
                      <input class="uk-input" type="password" v-model="form.password" placeholder="パスワード" required />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <button
                      class="uk-button uk-button-primary uk-button-large uk-width-1-1"
                      type="submit"
                    >ログイン</button>
                  </div>
                  <div class="uk-text-small uk-text-center">
                    登録していない方
                    <a href="#">アカウント作成</a>
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
// import GlobalMessage from "@/components/GlobalMessage.vue";

export default {
  components: {
    MyHeader,
    // GlobalMessage
  },
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    // ログインボタン押下
    submitLogin: function() {
      // ログイン
      this.$store
        .dispatch("auth/login", {
          username: this.form.username,
          password: this.form.password
        })
        .then(() => {
          console.log("Login succeeded.");
          this.$store.dispatch("message/setInfoMessage", {
            message: "ログインしました。"
          });
          // クエリ文字列に「next」がなければ、ホーム画面へ
          const next = this.$route.query.next || "/";
          this.$router.replace(next);
        });
    }
  }
};
</script>
