<template>
  <div>
    <MyHeader />
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <div id="content">
        <div class="uk-width-1-1">
          <div class="uk-container">
            <a @click="$router.back()" title="前ページへ戻る">
              <i
                id="back_icon"
                uk-icon="icon: chevron-double-left; ratio: 2"
              ></i>
            </a>
            <div
              id="new_post_card"
              class="uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <div v-if="post_id" class="uk-text-center" id="new_post_title">
                投稿編集
              </div>
              <div v-else class="uk-text-center" id="new_post_title">
                新規投稿
              </div>
              <ValidationObserver v-slot="{ invalid }">
                <form @submit.prevent="submitPost()">
                  <div uk-grid id="grid">
                    <div class="uk-width-1-2@s">
                      <div uk-form-custom id="form_custom">
                        <div class="uk-placeholder uk-text-center">
                          <input type="file" @change="selectedFile" />
                          <!-- <div id="preview"> -->
                            <div v-if="!post_id" id="preview">
                              <img
                                id="preview_image"
                                v-show="previewImage"
                                :src="previewImage"
                              />
                            </div>
                            <div v-else id="preview">
                              <img id="preview_image" :src="beforeImage" />
                            </div>
                          <!-- </div> -->
                          <div class="camera-choice">
                            <div
                              class="camera-icon uk-hidden-touch"
                              uk-icon="icon: camera; ratio: 5"
                            ></div>
                            <div
                              class="camera-icon uk-hidden-notouch"
                              uk-icon="icon: camera; ratio: 3"
                            ></div>
                            <p>画像を選択してください</p>
                          </div>
                        </div>
                      </div>
                      <p id="error_message">{{ message }}</p>
                    </div>
                    <div class="uk-width-1-2@s">
                      <div class="uk-inline uk-width-1-1">
                        <label>カテゴリ</label>
                        <ValidationProvider
                          mode="lazy"
                          name="カテゴリ"
                          rules="required"
                          v-slot="{ errors }"
                        >
                          <select class="uk-select" v-model="category">
                            <option
                              v-for="(ctg, key) in categories"
                              :key="key"
                              v-bind:value="ctg.id"
                            >
                              {{ ctg.name }}
                            </option>
                          </select>
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                      <div class="uk-inline uk-width-1-1">
                        <label>タイトル（15文字以下）</label>
                        <ValidationProvider
                          mode="aggressive"
                          name="タイトル"
                          rules="required|max:15"
                          v-slot="{ errors }"
                        >
                          <input
                            class="uk-input"
                            type="text"
                            v-model="title"
                            required
                          />
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                      <div class="uk-inline uk-width-1-1">
                        <label>キャプション</label>
                        <ValidationProvider
                          mode="aggressive"
                          name="キャプション"
                          rules="required"
                          v-slot="{ errors }"
                        >
                          <textarea
                            class="uk-textarea"
                            rows="3"
                            type="text"
                            v-model="content"
                            required
                          ></textarea>
                          <p id="error_message">{{ errors[0] }}</p>
                        </ValidationProvider>
                      </div>
                      <div class="uk-inline uk-width-1-1">
                        <label>場所（任意）</label>
                        <span id="select_way">: 指定方法は以下の2つです</span>
                        <div
                          uk-switcher="animation: uk-animation-fade; toggle: > *"
                        >
                          <button
                            class="uk-button uk-button-secondary uk-button-small"
                            :href="'#modal-center' + title"
                            @click="callChildMethod"
                            type="button"
                            uk-toggle
                          >
                            タイトルから検索
                          </button>
                          or
                          <button
                            class="uk-button uk-button-secondary uk-button-small"
                            type="button"
                          >
                            都道府県のみ
                          </button>
                        </div>
                        <div
                          :id="'modal-center' + title"
                          class="uk-flex-top .uk-width-large"
                          uk-modal
                        >
                          <div
                            class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical"
                          >
                            <button
                              class="uk-modal-close-default"
                              type="button"
                              uk-close
                            ></button>
                            <div>
                              <TitleSearchMap
                                ref="map"
                                :title="title"
                                @callParent="callParent"
                              />
                            </div>
                          </div>
                        </div>
                        <ul id="address_form" class="uk-switcher">
                          <li>
                            <input
                              placeholder="住所または都道府県名が入力されます"
                              class="uk-input"
                              type="text"
                              v-model="address"
                            />
                          </li>
                          <li>
                            <select class="uk-select" v-model="prefecture">
                              <option value>都道府県を選択してください</option>
                              <option v-for="item in prefs" :key="item.name">
                                {{ item.name }}
                              </option>
                            </select>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <button
                    id="send_button"
                    class="uk-button uk-button-large uk-width-1-1"
                    type="submit"
                    :disabled="invalid"
                  >
                    <span v-if="post_id">変更を保存</span>
                    <span v-else>投稿</span>
                  </button>
                  <!-- </div> -->
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
import MyHeader from "@/components/MyHeader";
import TitleSearchMap from "@/components/TitleSearchMap";
import prefs from "../mixins/PrefsMixin";
import { mapGetters } from "vuex";
import api from "@/services/api";
import {
  ValidationProvider,
  ValidationObserver,
  extend,
  localize,
} from "vee-validate";
import ja from "vee-validate/dist/locale/ja.json";
import { required, max, min, email, image } from "vee-validate/dist/rules";
import { clearSession } from "@/mixins/utility";

extend("required", required);
extend("max", max);
extend("min", min);
extend("email", email);
extend("image", image);
localize("ja", ja);

export default {
  mixins: [prefs, clearSession],
  components: {
    MyHeader,
    TitleSearchMap,
    ValidationProvider,
    ValidationObserver,

    // ManualSearchMap,
  },
  props: ["post_id"],
  data() {
    return {
      category: "",
      author_name: this.$store.getters["auth/id"],
      image: null,
      previewImage: null,
      beforeImage: null,
      title: "",
      content: "",
      address: "",
      prefecture: "",
      lat: "",
      lng: "",
      message: "",
      loading: true,
    };
  },
  watch: {
    image() {
      if (this.image || this.beforeImage) {
        return (this.message = "");
      }
    },
    $route() {
      (this.category = ""),
        (this.author_name = this.$store.getters["auth/id"]),
        (this.image = null),
        (this.previewImage = null),
        (this.beforeImage = null),
        (this.title = ""),
        (this.content = ""),
        (this.address = ""),
        (this.prefecture = ""),
        (this.lat = ""),
        (this.lng = ""),
        (this.message = "");
    },
  },
  computed: {
    ...mapGetters("category", ["categories"]),
  },
  methods: {
    callChildMethod() {
      this.$refs.map.mapSearch();
    },
    callParent(address, prefecture, lat, lng) {
      this.address = address;
      this.prefecture = prefecture[0].long_name;
      this.lat = lat;
      this.lng = lng;
    },
    selectedFile(event) {
      event.preventDefault();
      this.image = event.target.files[0];
      this.createImage(event.target.files[0]);
    },
    submitPost() {
      const formData = new FormData();
      formData.append("category", this.category);
      formData.append("author_name", this.author_name);
      formData.append("title", this.title);
      formData.append("content", this.content);
      if (this.image) formData.append("raw_image", this.image);
      formData.append("prefecture", this.prefecture);
      if (this.address) formData.append("address", this.address);
      if (this.lat) formData.append("lat", this.lat);
      if (this.lng) formData.append("lng", this.lng);
      if (this.post_id) {
        if (this.image || this.beforeImage) {
          api
            .patch("/posts/" + this.post_id + "/", formData)
            .then((response) => {
              console.log("送信内容: " + response.data);
              this.$router.replace("/");
            });
        } else {
          console.log("エラー");
          this.message = "画像ファイルを選択してください";
        }
      } else {
        if (this.image || this.beforeImage) {
          api.post("/posts/", formData).then((response) => {
            console.log("送信内容: " + response.data);
            this.$router.replace("/");
          });
        } else {
          console.log("エラー");
          this.message = "画像ファイルを選択してください";
        }
      }
      // .catch((error) => {
      //   console.log("エラー");
      //   console.log("response: ", error.response.data);
      // },
    },
    createImage(file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        this.previewImage = event.target.result;
      };
      reader.readAsDataURL(file);
    },
  },
  created() {
    this.clearSession();
    if (this.post_id) {
      console.log("投稿編集");
      api.get("/posts/" + this.post_id + "/").then((response) => {
        this.beforeImage = response.data.image;
        this.category = response.data.category;
        this.title = response.data.title;
        this.content = response.data.content;
        this.prefecture = response.data.prefecture;
        this.address = response.data.address;
        this.lat = response.data.lat;
        this.lng = response.data.lng;
        this.loading = false;
      });
    } else {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
@import "../assets/common.css";

#content {
  margin-top: 10px;
}

#grid {
  margin-bottom: 20px;
}
#new_post_title {
  font-size: 30px;
  margin-bottom: 20px;
}

#form_custom {
  width: 540px;
  /* padding-top: 0%; */
  background-color: #fff;
  border: 2px solid #ccc;
  /* box-sizing: border-box; */
}
#form_custom:hover {
  background-color: rgba(0, 0, 0, 0.041);
  z-index: 100;
}

.uk-placeholder {
  /* width: 100%; */
  padding-top: 75%;
  padding-bottom: 0px;
  margin-bottom: 0px;
  /* height: 100%; */
  /* padding: 0px 0px; */
  /* background: 0 0; */
  /* position: relative; */
  /* box-sizing: border-box; */
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
  width: 100%;
  height:100%;
  right: 0px;
  top: 0px;
  z-index: 100;
  pointer-events: none;
}
#preview_image {
  width: 100%;
  height: 100%;
  /* padding-top:75%; */

}
.uk-modal-body {
  border-radius: 5px;
}

.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: rgb(240, 240, 240);
  transform: translateY(-100px);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#address_form {
  margin-top: 4px;
}

#new_post_card {
  background-color: rgba(225, 215, 205, 0.247);
  border-radius: 10px;
}
#select_way {
  font-size: 14px;
  color: rgb(145, 91, 56);
}
</style>
