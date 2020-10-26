<template>
  <v-container>
    <h3 class="h3 text-center pt-8">プロフィール編集</h3>
    <v-row justify="center">
      <v-col justify="center">
        <v-card
          elevation="5"
          shaped
          color="blue-grey lighten-5"
          class="mx-auto"
          max-width="800px"
        >
          <div class="pa-8">
            <span v-if="id == 2" style="color: red"
              >※
              申し訳ございません。GuestUserは編集及びアカウント削除ができません。</span
            >
            <ValidationObserver v-slot="{ invalid }">
              <form @submit.prevent="submitPost()">
                <v-row>
                  <v-col cols="12" md="6">
                    <div uk-form-custom id="form_custom">
                      <div class="uk-placeholder uk-text-center">
                        <input
                          :disabled="disabled"
                          type="file"
                          @change="selectedFile"
                        />
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
                  </v-col>
                  <v-col cols="12" md="6">
                    <ValidationProvider
                      mode="lazy"
                      name="ユーザー名"
                      rules="required|max:10"
                      v-slot="{ errors }"
                    >
                      <v-text-field
                        :disabled="disabled"
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
                        :disabled="disabled"
                        v-model="email"
                        :error-messages="errors"
                        required
                        placeholder="メールアドレス"
                        prepend-inner-icon="mdi-email"
                      ></v-text-field>
                    </ValidationProvider>
                    <ValidationProvider
                      mode="lazy"
                      name="入力内容"
                      rules="required"
                      v-slot="{ errors }"
                    >
                      <v-textarea
                        label="自己紹介"
                        rows="4"
                        v-model="introduction"
                        :error-messages="errors"
                        :disabled="disabled"
                        required
                        placeholder="自分のことについて簡単に書きましょう！"
                      ></v-textarea>
                    </ValidationProvider>
                    <v-btn
                      block
                      large
                      elevation="2"
                      class="mr-4 mt-4"
                      type="submit"
                      :disabled="invalid || disabled"
                    >
                      変更を保存する
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row no-gutters>
                  <v-col class="text-right">
                    <v-dialog v-model="dialog" width="500">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          small
                          elevation="2"
                          color="red accent-1"
                          v-bind="attrs"
                          v-on="on"
                          :disabled="disabled"
                        >
                          アカウント削除
                        </v-btn>
                      </template>
                      <v-card>
                        <div>
                          <v-card-title class="headline grey lighten-2">
                            アカウント削除確認
                          </v-card-title>

                          <v-card-text>
                            アカウントを削除します。よろしいですか？
                          </v-card-text>

                          <v-divider></v-divider>

                          <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="primary" text @click="deleteAccount">
                              OK
                            </v-btn>
                          </v-card-actions>
                        </div>
                      </v-card>
                    </v-dialog>
                  </v-col>
                </v-row>
              </form>
            </ValidationObserver>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
import { required, max, min, email } from "vee-validate/dist/rules";

extend("required", required);
extend("max", max);
extend("min", min);
extend("email", email);
localize("ja", ja);

export default {
  components: {
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
      disabled: false,
      dialog: false,
    };
  },
  mounted() {
    if (this.username === "GuestUser") {
      this.disabled = true;
    }
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
        this.$router.replace("/mypage/" + this.id + "/");
      });
    },
    createImage(file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        this.previewImage = event.target.result;
      };
      reader.readAsDataURL(file);
    },
    async deleteAccount() {
      this.dialog = false;
      await api
        .delete("/users/" + this.id + "/")
        .then(
          this.$store.dispatch("message/setInfoMessage", {
            message: "アカウントを削除しました",
          })
        )
        .catch((error) => {
          console.log(error);
        });
      this.$store.dispatch("user/logout"),
        this.$store.dispatch("auth/logout"),
        this.$router.replace("/");
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

#preview {
  position: relative;
  /* position: absolute; */
  /* 現在:, 変更:, クリア表示を隠す  */
  top: 0px;
  z-index: 1;
  pointer-events: none;
  width: 100%;
  height: auto;
}

#preview_image {
  position: relative;
  width: 100%;
  height: auto;
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
