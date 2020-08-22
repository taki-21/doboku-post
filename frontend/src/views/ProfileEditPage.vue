<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div class="uk-section">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-margin uk-width-large uk-margin-auto">
            <a @click="$router.back()" title="前ページへ戻る">
              <i uk-icon="icon: chevron-double-left; ratio: 2"></i>
            </a>
            <div
              class="uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <h2 class="uk-card-title uk-text-center">プロフィール編集</h2>
              <form @submit.prevent="submitPost()">
                <div uk-form-custom id="form_custom">
                  <div class="uk-placeholder uk-text-center">
                    <input type="file" @change="selectedFile" />
                    <div id="preview">
                      <div v-if="previewImage">
                        <img id="preview_image" :src="previewImage" />
                      </div>
                      <div v-else>
                        <img id="preview_image" :src="beforeIconImage " />
                      </div>
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
                      v-model="username"
                      required
                    />
                  </div>
                </div>
                <div class="uk-margin">
                  <div class="uk-inline uk-width-1-1">
                    <span class="uk-form-icon" uk-icon="icon: mail"></span>
                    <input
                      class="uk-input"
                      type="email"
                      placeholder="メールアドレス"
                      v-model="email"
                      required
                    />
                  </div>
                </div>
                <div class="uk-margin">
                  <div class="uk-inline uk-width-1-1">
                    <span class="uk-form-icon" uk-icon="icon: file-edit"></span>
                    <textarea
                      class="uk-textarea textarea-input"
                      rows="8"
                      type="text"
                      placeholder="自己紹介文"
                      v-model="introduction"
                      required
                    ></textarea>
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
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";

import MyHeader from "@/components/MyHeader";

export default {
  components: {
    MyHeader,
  },
  computed: {
    ...mapGetters("auth", {
      id: "id",
    }),
  },
  data() {
    return {
      isLoading: false,
      beforeIconImage: "",
      icon_image: "",
      previewImage: "",
      username: "",
      email: "",
      introduction: "",
    };
  },
  // mounted() {
  //   this.axios
  //     .get("http://127.0.0.1:8000/api/v1/users/" + this.id + "/")
  //     .then(response => {
  //       this.user = response.data;
  //     });
  // },
  methods: {
    selectedFile(event) {
      event.preventDefault();
      this.icon_image = event.target.files[0];
      this.createImage(event.target.files[0]);
    },
    submitPost: function () {
      const formData = new FormData();
      if (this.icon_image) formData.append("icon_image", this.icon_image);
      formData.append("username", this.username);
      formData.append("email", this.email);
      formData.append("introduction", this.introduction);
      api
        .patch("http://127.0.0.1:8000/api/v1/users/" + this.id + "/", formData)
        .then(async () => {
          this.$store.dispatch("message/setInfoMessage", {
            message: "更新完了",
          });
          // ここで一度更新してないとユーザーIDを変更した際にエラーが出る
          // storeのユーザー情報を更新
          await this.$store.dispatch("auth/reload");
          await this.$store.dispatch("user/load", {
            id: this.$store.getters["auth/id"],
          });
          this.$router.replace("/mypage/");
          this.isLoading = false;
        });
    },
    createImage(file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        this.previewImage = event.target.result;
      };
      reader.readAsDataURL(file);
    },
    back() {
      // 1つ前へ
      this.$router.back();
    },
  },
  mounted() {
    this.isLoading = true;
    this.$store.dispatch("user/load", { id: this.id }).then((resUser) => {
      this.beforeIconImage = resUser.icon_image;
      this.username = resUser.username;
      this.email = resUser.email;
      this.introduction = resUser.introduction;
    });
  },
};
</script>
<style scoped>
#form_custom {
  width: 100%;
  height: 370px;
}

.uk-placeholder {
  width: 100%;
  margin-bottom: 0px;
  height: 100%;
  padding: 0px 0px;
  background: 0 0;
  position: relative;
  border: 3px solid #ccc;
}

.camera-choice {
  position: absolute;
  top: 50%;
  left: 50%;
  display: table-cell;
  vertical-align: middle;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

#preview {
  position: absolute;
  /* 現在:, 変更:, クリア表示を隠す  */
  top: 0px;
  z-index: 100;
  pointer-events: none;
  width: 100%;
  height: 100%;
}

#preview_image {
  width: 100%;
  height: 364px;
}

.textarea-input {
  padding-left: 40px;
}

.uk-section {
  padding-top: 30px;
  /* padding-bottom: 70px; */
}
</style>
