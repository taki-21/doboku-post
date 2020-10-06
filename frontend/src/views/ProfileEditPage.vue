<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div class="uk-section">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-margin uk-width-large uk-margin-auto">
            <a @click="$router.back()" title="前ページへ戻る">
              <i
                id="back_icon"
                uk-icon="icon: chevron-double-left; ratio: 2"
              ></i>
            </a>
            <div
              id="profile_edit_card"
              class="uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <h2 class="uk-card-title uk-text-center">プロフィール編集</h2>
              <ValidationObserver v-slot="{ invalid }">
                <form @submit.prevent="submitPost()">
                  <div uk-form-custom id="form_custom">
                    <div class="uk-placeholder uk-text-center">
                      <input type="file" @change="selectedFile" />
                      <div id="preview">
                        <div v-if="previewImage">
                          <img id="preview_image" :src="previewImage" />
                        </div>
                        <div v-else>
                          <img id="preview_image" :src="beforeIconImage" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <ValidationProvider
                        mode="lazy"
                        name="ユーザー名"
                        rules="required|max:10"
                        v-slot="{ errors }"
                      >
                        <span
                          id="form_icon"
                          class="uk-form-icon"
                          uk-icon="icon: user"
                        ></span>
                        <input
                          class="uk-input"
                          type="text"
                          placeholder="ユーザー名"
                          v-model="username"
                          required
                        />
                        <p id="error_message">{{ errors[0] }}</p>
                      </ValidationProvider>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <ValidationProvider
                        mode="lazy"
                        name="入力内容"
                        rules="required|email"
                        v-slot="{ errors }"
                      >
                        <span
                          id="form_icon"
                          class="uk-form-icon"
                          uk-icon="icon: mail"
                        ></span>
                        <input
                          class="uk-input"
                          type="email"
                          placeholder="メールアドレス"
                          v-model="email"
                          required
                        />
                        <p id="error_message">{{ errors[0] }}</p>
                      </ValidationProvider>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <span
                        class="uk-form-icon"
                        uk-icon="icon: file-edit"
                      ></span>
                      <textarea
                        class="uk-textarea textarea-input"
                        rows="8"
                        type="text"
                        placeholder="自己紹介文"
                        v-model="introduction"
                      ></textarea>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <button
                      id="send_button"
                      class="uk-button uk-button-primary uk-button-large uk-width-1-1"
                      :disabled="invalid"
                      type="submit"
                    >
                      変更を保存する
                    </button>
                  </div>
                </form>
              </ValidationObserver>
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
import {
  ValidationProvider,
  ValidationObserver,
  extend,
  localize,
} from "vee-validate";
import ja from "vee-validate/dist/locale/ja.json";
import { required, max, min, email } from "vee-validate/dist/rules";

extend("required", required);
extend("max", max);
extend("min", min);
extend("email", email);
localize("ja", ja);

export default {
  components: {
    MyHeader,
    ValidationProvider,
    ValidationObserver,
  },
  computed: {
    ...mapGetters("auth", {
      id: "id",
    }),
  },
  data() {
    return {
      beforeIconImage: this.$store.getters["user/icon_image"],
      icon_image: "",
      previewImage: "",
      username: this.$store.getters["user/username"],
      email: this.$store.getters["user/email"],
      introduction: this.$store.getters["user/introduction"],
    };
  },
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
      api.patch("/users/" + this.id + "/", formData).then(async () => {
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
};
</script>
<style scoped>
@import "../assets/common.css";

.uk-input,
.uk-textarea {
  border-color: rgba(150, 150, 150, 0.5);
}

/* #profile_edit_card {
  background-color: rgba(225, 215, 205, 0.247);
  border-radius: 10px;
} */
#form_icon {
  height: 40px;
}

#form_custom {
  width: 100%;
  height: auto;
}

.uk-placeholder {
  position: relative;
  width: 100%;
  margin-bottom: 0px;
  height: auto;
  padding: 0px 0px;
  background: 0 0;
  position: relative;
  border: 3px solid #ccc;
  box-sizing: border-box;
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
  position: relative;
  /* position: absolute; */
  /* 現在:, 変更:, クリア表示を隠す  */
  top: 0px;
  z-index: 100;
  pointer-events: none;
  width: 100%;
  height: auto;
}

#preview_image {
  position: relative;
  width: 100%;
  height: auto;
}

.textarea-input {
  padding-left: 40px;
}

.uk-section {
  padding-top: 30px;
  /* padding-bottom: 70px; */
}
@media (max-width: 640px) {
  #preview_image {
    position: relative;

    width: 100%;
    height: auto;
  }
  .uk-placeholder[data-v-2516ac38] {
    position: relative;
    width: 100%;
    margin-bottom: 0px;
    height: auto;
    padding: 0px 0px;
    background: 0 0;
    position: relative;
    border: 3px solid #ccc;
    box-sizing: border-box;
  }
}
</style>
