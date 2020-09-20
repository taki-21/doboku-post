<template>
  <div>
    <MyHeader />
    <!-- ヘッダー -->
    <div class="uk-section">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <a @click="$router.back()" title="前ページへ戻る">
            <i id="back_icon" uk-icon="icon: chevron-double-left; ratio: 2"></i>
          </a>
          <div
            class="uk-margin uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
          >
            <h2 class="uk-text-center" id="new_post_title">新規投稿</h2>
            <!-- <pre>{{image}}</pre> -->
            <form @submit.prevent="submitPost()">
              <div uk-grid>
                <div class="uk-width-1-2">
                  <div uk-form-custom id="form_custom">
                    <div class="uk-placeholder uk-text-center">
                      <input type="file" @change="selectedFile" />
                      <div id="preview">
                        <img id="preview_image" v-show="previewImage" :src="previewImage" />
                      </div>
                      <div class="camera-choice">
                        <div class="camera-icon" uk-icon="icon: camera; ratio: 5"></div>
                        <p>画像を選択してください</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="uk-width-1-2">
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <label>カテゴリ</label>
                      <select
                        class="uk-select"
                        type="text"
                        v-model="category"
                        required
                      >
                        <option
                          v-for="(ctg,key) in categories"
                          :key="key"
                          v-bind:value="ctg.id"
                        >{{ctg.name}}</option>
                      </select>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <label>タイトル</label>
                      <input class="uk-input" type="text" v-model="title" required />
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <label>キャプション</label>
                      <textarea
                        class="uk-textarea"
                        rows="3"
                        type="text"
                        v-model="content"
                        required
                      ></textarea>
                    </div>
                  </div>
                  <div class="uk-margin">
                    <div class="uk-inline uk-width-1-1">
                      <label>場所</label>
                      <div uk-switcher="animation: uk-animation-fade; toggle: > *">
                        <button
                          class="uk-button uk-button-secondary uk-button-small"
                          href="#modal-center"
                          @click="callChildMethod"
                          type="button"
                          uk-toggle
                        >タイトルから検索</button>
                        or
                        <!-- <button
                            class="uk-button uk-button-secondary uk-button-small"
                            href="#modal-center"
                            type="button"
                            uk-toggle
                          >手動</button>
                        or-->
                        <button
                          class="uk-button uk-button-secondary uk-button-small"
                          type="button"
                        >都道府県のみ</button>
                        <!-- </li> -->
                        <!-- </ul> -->
                      </div>
                      <div id="modal-center" class="uk-flex-top .uk-width-large" uk-modal>
                        <div class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
                          <button class="uk-modal-close-default" type="button" uk-close></button>
                          <div>
                            <TitleSearchMap ref="map" :title="title" @callParent="callParent" />
                          </div>
                        </div>
                      </div>
                      <!-- <div id="modal-manual" class="uk-flex-top .uk-width-large" uk-modal>
                          <div class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
                            <button class="uk-modal-close-default" type="button" uk-close></button>
                            <div>
                              <TitleSearchMap ref="map" :title="title" @callParent="callParent" />
                            </div>
                          </div>
                      </div>-->
                      <ul id="address_form" class="uk-switcher">
                        <li>
                          <input class="uk-input" type="text" v-model="address" />
                        </li>
                        <!-- <li>
                            <input
                              id="manual_search"
                              class="uk-input"
                              type="text"
                              v-model="address"
                            />
                        </li>-->
                        <li>
                          <select class="uk-select" v-model="prefecture">
                            <option value>都道府県を選択してください</option>
                            <option v-for="item in prefs" :key="item.name">{{item.name}}</option>
                          </select>
                        </li>
                      </ul>
                      <!-- </div> -->
                    </div>
                  </div>
                </div>
              </div>
              <div class="uk-margin">
                <button
                  class="uk-button uk-button-default uk-button-large uk-width-1-1 post-button"
                  type="submit"
                >投稿</button>
              </div>
            </form>
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
import api from "@/services/api";
export default {
  mixins: [prefs],
  components: {
    MyHeader,
    TitleSearchMap,
    // ManualSearchMap,
  },
  data() {
    return {
      categories: [],
      category: "",
      author_name: this.$store.getters["auth/id"],
      image: null,
      previewImage: null,
      title: "",
      content: "",

      address: "",
      prefecture: "",
      lat: "",
      lng: "",

      loading: false,
    };
  },
  mounted() {
    api.get("/categories/").then((response) => {
      this.categories = response.data;
    });
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
    submitPost: function () {
      const formData = new FormData();
      formData.append("category", this.category);
      formData.append("author_name", this.author_name);
      formData.append("title", this.title);
      formData.append("content", this.content);
      formData.append("image", this.image);
      formData.append("prefecture", this.prefecture);
      formData.append("address", this.address);
      formData.append("lat", this.lat);
      formData.append("lng", this.lng);
      // formData.append("location",this.location);
      // "prefecture": this.prefecture,
      // "address": this.address,
      // "lat": this.lat,
      // "lng": this.lng

      api
        .post("/posts/", formData)
        .then((response) => {
          console.log("送信内容: " + response.data);
          this.$router.replace("/");
        })
        .catch((error) => {
          console.log("response: ", error.response.data);
        });
    },
    createImage(file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        this.previewImage = event.target.result;
      };
      reader.readAsDataURL(file);
    },
  },
};
</script>

<style scoped>
#back_icon{
  color: rgba(139, 138, 135, 0.85);
}

.post-button {
  margin-top: 10px;
  font-size: 25px;
}

h2#new_post_title {
  position: relative;
  top: -15px;
}

#form_custom {
  width: 525px;
  height: 393px;
}

.uk-placeholder {
  width: 100%;
  margin-bottom: 0px;
  height: 100%;
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
  position: absolute;
  /* 現在:, 変更:, クリア表示を隠す  */
  top: 0px;
  z-index: 100;
  pointer-events: none;
}

#preview_image {
  width: 519px;
  height: 387px;
}
.uk-form-custom:hover {
  cursor: pointer;
  background-color: rgba(212, 217, 220, 0.3);
}

.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: #fff;
  transform: translateY(-100px);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#address_form {
  margin-top: 4px;
}
/* #title_search {
  margin-left: 40px;
  margin-right: 20px;
}
#manual_search {
  margin-left: 20px;
  margin-right: 20px;
}
#prefecture_search {
  margin-left: 20px;
} */
.uk-button-default {
  background-color: rgba(212, 217, 220, 0.4);
  color: #333;
  border: 2px solid rgb(112, 110, 110);
  border-radius: 7px;
}
.uk-button-default:hover {
  background-color: rgb(212, 217, 220);
  color: #333;
  border: 2px solid #333;
  border-radius: 7px;
}

.uk-section {
  padding-top: 30px;
}
</style>
