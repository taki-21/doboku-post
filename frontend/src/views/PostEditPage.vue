<template>
  <div>
    <MyHeader />
    <!-- ヘッダー -->
    <div id="new_post">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-grid-margin uk-grid-stack">
            <div
              class="uk-margin uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <h2 class="uk-text-center" id="new_post_title">投稿編集</h2>
              <!-- <pre>{{image}}</pre> -->
              <form @submit.prevent="submitPost()">
                <div uk-grid>
                  <div class="uk-width-1-2">
                    <div uk-form-custom id="form_custom">
                      <div class="uk-placeholder uk-text-center">
                        <input type="file" @change="selectedFile" />
                        <div id="preview">
                          <div v-if="previewImage">
                            <img id="preview_image" :src="previewImage" />
                          </div>
                          <div v-else>
                            <img id="preview_image" :src="beforeImage " />
                          </div>
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
                        {{category}}
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
                        {{title}}
                        <input
                          class="uk-input"
                          type="text"
                          v-model="title"
                          required
                        />
                      </div>
                    </div>
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>キャプション</label>
                        {{content}}
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
                        <!-- <div class="uk-flex"> -->
                        <label>場所</label>
                        <!-- <div> -->
                        <!-- <div uk-switcher="animation: uk-animation-fade; toggle: > *"> -->
                        <!-- <ul
                          class="uk-subnav uk-subnav-pill"
                          uk-switcher="animation: uk-animation-slide-left-medium"
                        >
                        <li>-->
                        <div uk-switcher="animation: uk-animation-fade; toggle: > *">
                          <button
                            class="uk-button uk-button-secondary uk-button-small"
                            href="#modal-center"
                            @click="callChildMethod"
                            type="button"
                            uk-toggle
                          >タイトルから検索</button>
                          or
                          <button
                            class="uk-button uk-button-secondary uk-button-small"
                            type="button"
                          >手動</button>
                          or
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
                        <ul id="address_form" class="uk-switcher">
                          <li>
                            <input class="uk-input" type="text" v-model="address" />
                          </li>
                          <li>
                            <input
                              id="manual_search"
                              class="uk-input"
                              type="text"
                              v-model="address"
                            />
                          </li>
                          <li>
                            <select class="uk-select" v-model="prefecture">
                              <option>都道府県を選択してください</option>
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
                    class="uk-button uk-button-primary uk-button-large uk-width-1-1 post-button"
                    type="submit"
                  >投稿</button>
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
import MyHeader from "@/components/MyHeader";
import TitleSearchMap from "@/components/TitleSearchMap";

import api from "@/services/api";
import prefs from "../mixins/PrefsMixin";

import { mapGetters } from "vuex";

export default {
  components: {
    MyHeader,
    TitleSearchMap
  },
  mixins: [prefs],
  props: ["post_id"],
  data() {
    return {
      // categories: [],
      beforeImage: null,
      previewImage: null,
      category: "",
      title: "",
      content: "",

      address: "",
      prefecture: "",
      lat: "",
      lng: "",

      loading: false
    };
  },
  computed: {
    ...mapGetters("category", ["categories"])
  },
  mounted() {
    api.get("/posts/" + this.post_id + "/").then(response => {
      this.beforeImage = response.data.image;
      this.category = response.data.category;
      this.title = response.data.title;
      this.content = response.data.content;
      this.prefecture = response.data.prefecture;
      this.address = response.data.address;
      this.lat = response.data.lat;
      this.lng = response.data.lng;
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
    submitPost: function() {
      const formData = new FormData();
      if (this.image) formData.append("image", this.image);

      formData.append("category", this.category);
      formData.append("title", this.title);
      formData.append("content", this.content);
      formData.append("prefecture", this.prefecture);
      if(this.address){formData.append("address", this.address);}
      if(this.lat){formData.append("lat", this.lat);}
      if(this.lng){formData.append("lng", this.lng);}

      api
        .patch(
          "http://127.0.0.1:8000/api/v1/posts/" + this.post_id + "/",
          formData
        )
        .then(response => {
          console.log("送信内容: " + response.data);
          this.$router.replace("/");
        })
        .catch(error => {
          console.log("response: ", error.response.data);
        });
    },
    createImage(file) {
      const reader = new FileReader();
      reader.onload = event => {
        this.previewImage = event.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
};
</script>

<style scoped>
#new_post {
  padding-top: 50px;
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
  width: 521px;
  height: 387px;
}
.uk-form-custom:hover {
  cursor: pointer;
  background-color: #e6e6fa;
}

.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: #fff;
  opacity: 0;
  transform: translateY(-100px);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#address_form {
  margin-top: 4px;
}
</style>
