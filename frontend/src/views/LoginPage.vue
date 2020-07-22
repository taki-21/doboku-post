<template>
  <div id="login-page">
    <GlobalHeader/>
    <GlobalMessage/>

    <!-- メインエリア -->
    <main class="container">
      <p class="h5 mb-4">ログイン</p>
      <form @submit.prevent="submitLogin">
        <div class="row form-group">
          <label class="col-sm-3 col-form-label">ユーザー名</label>
          <div class="col-sm-8">
            <input type="text" v-model="form.username" required/>
          </div>
        </div>
        <div class="row form-group">
          <label class="col-sm-3 col-form-label">パスワード</label>
          <div class="col-sm-8">
            <input type="password" v-model="form.password" required/>
          </div>
        </div>
        <div class="row text-center mt-5">
          <div class="col-sm-12">
            <v-btn type="submit" variant="primary">ログイン</v-btn>
          </div>
        </div>
      </form>
    </main>
  </div>
</template>

<script>
  import GlobalHeader from '@/components/GlobalHeader.vue'
  import GlobalMessage from '@/components/GlobalMessage.vue'

  export default {
    components: {
      GlobalHeader,
      GlobalMessage
    },
    data () {
      return {
        form: {
          username: '',
          password: ''
        }
      }
    },
    methods: {
      // ログインボタン押下
      submitLogin: function () {
        // ログイン
        this.$store.dispatch('auth/login', {
          username: this.form.username,
          password: this.form.password
        })
          .then(() => {
            console.log('Login succeeded.')
            this.$store.dispatch('message/setInfoMessage', { message: 'ログインしました。' })
            // クエリ文字列に「next」がなければ、ホーム画面へ
            const next = this.$route.query.next || '/'
            this.$router.replace(next)
          })
      }
    }
  }
</script>
