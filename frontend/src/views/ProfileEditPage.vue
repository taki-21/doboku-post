<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div>
      <div class="uk-section uk-flex uk-flex-middle uk-animation-fade">
        <div class="uk-width-1-1">
          <div class="uk-container">
            <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid></div>
            <div class="uk-width-1-1@m">
              <div
                class="uk-margin uk-width-large uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
              >
                <h2 class="uk-card-title uk-text-center">プロフィール編集</h2>
                <pre>{{ user }}</pre>
                <form method="post" enctype="multipart/form-data">
                    <div uk-form-custom id="form_custom">
                      <div class="uk-placeholder uk-text-center">
                        <input type="file"/>
                        <div id="preview">
                          <img/>
                        </div>
                      <div class="camera-choice">
                        <div class="camera-icon" uk-icon="icon: camera; ratio: 5"></div>
                        <p>画像を選択してください</p>
                      </div>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: user"></span>
                      <input
                        class="uk-input"
                        type="text"
                        placeholder="ユーザー名"
                        v-model="user.username"
                        required
                      />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: mail"></span>
                      <input
                        class="uk-input"
                        type
                        placeholder="メールアドレス"
                        v-model="user.email"
                        required
                      />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span class="uk-form-icon" uk-icon="icon: file-edit"></span>
                      <textarea class="uk-textarea" rows="8" type="text" v-model="user.introduction" required></textarea>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <button
                      class="uk-button uk-button-primary uk-button-large uk-width-1-1"
                      type="submit"
                    >変更を保存する</button>
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
import MyHeader from "@/components/MyHeader";
export default {
  components: {
    MyHeader
  },
  data(){
    return{
      user: "",
      id: this.$store.getters["auth/id"]
    }

  },
  mounted(){
    this.axios
    .get('http://127.0.0.1:8000/api/v1/users/' + this.id + '/')
    .then(response => {
      this.user = response.data
    })
  }
};
</script>
