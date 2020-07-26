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
                        type
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
export default {
  components: {
    MyHeader
  },
  data() {
    return {
      message:"",
      username: "",
      email_adress: "",
      password1: "",
      password2: ""
    };
  },
  methods: {
    submitUser: function() {
      if (this.password1 == this.password2) {
        this.axios
          .post("http://127.0.0.1:8000/api/v1/users/", {
            username: this.username,
            email: this.email_adress,
            password: this.password1
          })
          .then(response => {
            console.log("送信内容: " + response.data);
            this.message = '送信しました！'
          })
          .catch(error => {
            console.log("response: ", error.response.data);
          });
      } else{
        this.message = '送信できませんでした'
      }
    }
  }
};
</script>
