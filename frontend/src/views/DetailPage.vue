<template>
  <div>
    <div v-show="isLoading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!isLoading">
      <div id="content">
        <div class="uk-width-1-1">
          <div class="uk-container">
            <v-btn text @click="$router.back()" title="前ページへ戻る">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-card elevation="3" shaped class="mx-lg-auto" max-width="1100px">
              <v-container class="grey lighten-5">
                <v-row>
                  <v-col cols="12" md="7">
                    <v-card> .col-12 .col-md-7 </v-card>
                    <v-card-title>
                      {{ post.title }}
                    </v-card-title>
                    <v-card-subtitle>
                      <v-avatar size="36px">
                        <img class="user_icon" :src="author.icon_image" />
                      </v-avatar>
                      <span>
                        {{ author.username }}
                      </span>
                    </v-card-subtitle>
                    <v-card-text>
                      {{ post.content }}
                    </v-card-text>
                    <div uk-lightbox>
                      <a :href="post.raw_image">
                        <v-img :src="post.image"></v-img>
                      </a>
                    </div>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-card> .col-12 .col-md-4 </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
            <div
              id="detail_post"
              class="uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <div uk-grid>
                <div class="uk-width-3-5@s">
                  <div>
                    <router-link
                      class="show_user"
                      v-if="author.id"
                      :to="{ name: 'mypage', params: { user_id: author.id } }"
                    >
                      <img class="user_icon" :src="author.icon_image" />
                      <span id="author_name">{{ author.username }}</span>
                    </router-link>
                    <div class="timestamp">
                      <span>{{ post.published_at | moment }}</span>
                    </div>
                    <div class="prefecture">
                      <span v-if="post.prefecture">{{ post.prefecture }}</span>
                      <span v-else>---</span>
                    </div>
                  </div>
                  <div id="title-content">
                    <div id="post_title">{{ post.title }}</div>
                    <div id="post_content">{{ post.content }}</div>
                  </div>

                  <div uk-lightbox>
                    <a :href="post.raw_image">
                      <img id="post_image" :src="post.image" />
                    </a>
                  </div>
                  <div v-if="post.address">
                    <button
                      id="location_button"
                      class="uk-button"
                      :href="modal_href"
                      type="button"
                      @click="showMap"
                      uk-toggle
                    >
                      <i uk-icon="location"></i>
                      場所を確認
                    </button>
                    <div :id="modal" class="uk-modal-flex" uk-modal>
                      <div
                        id="location_modal"
                        class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical"
                      >
                        <button
                          class="uk-modal-close-default"
                          type="button"
                          uk-close
                        ></button>
                        <div>
                          <Map ref="map" :post="post" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div id="like_buttun">
                    <div v-if="isLiked">
                      <div>
                        <span @click="toggleLike" :disabled="isProcessing">
                          <v-btn class="ma-2" text icon color="red lighten-2">
                            <v-icon x-large>mdi-heart</v-icon>
                          </v-btn>
                        </span>
                        <span class="like_count">{{ likeCount }}</span>
                      </div>
                    </div>
                    <div v-else>
                      <div>
                        <span @click="toggleLike">
                          <v-btn class="ma-2" text icon>
                            <v-icon x-large>mdi-heart-outline</v-icon>
                          </v-btn>
                        </span>
                        <span class="like_count">{{ likeCount }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="uk-width-2-5@s">
                  <div>
                    <div>
                      <CommentForm :post="post" @CommentGet="CommentGet" />
                    </div>
                  </div>
                  <div v-if="comments == ''">
                    <p id="none_message">まだコメントがありません</p>
                  </div>
                  <div v-else>
                    <div class="logbox">
                      <ul class="uk-comment-list">
                        <li v-for="comment in comments" :key="comment.id">
                          <article
                            class="uk-comment uk-comment-primary uk-visible-toggle"
                            tabindex="-1"
                          >
                            <header
                              class="uk-comment-header uk-position-relative"
                            >
                              <div>
                                <router-link
                                  class="show_user"
                                  :to="{
                                    name: 'mypage',
                                    params: { user_id: comment.author.id },
                                  }"
                                >
                                  <img
                                    class="comment_user_icon"
                                    :src="comment.author.icon_image"
                                  />
                                  <strong>{{ comment.author.username }}</strong>
                                </router-link>
                                <div class="timestamp">
                                  <span>{{ comment.timestamp | moment }}</span>
                                </div>
                              </div>
                            </header>
                            <div>
                              <div>{{ comment.text }}</div>
                            </div>
                            <div
                              id="delete-icon"
                              v-if="comment.author.id == login_user_id"
                            >
                              <a
                                class="router-link"
                                :href="'#modal-' + comment.id"
                                uk-toggle
                              >
                                <i id="delete-icon" uk-icon="icon: trash"></i>
                              </a>
                              <div :id="'modal-' + comment.id" uk-modal>
                                <div
                                  id="delete_modal"
                                  class="uk-modal-dialog uk-modal-body"
                                >
                                  <h2 class="uk-modal-title">削除確認</h2>
                                  <p>
                                    コメント：{{
                                      comment.text
                                    }}を削除します。よろしいですか？
                                  </p>
                                  <p class="uk-text-right">
                                    <button
                                      class="uk-button uk-button-default uk-modal-close"
                                      type="button"
                                    >
                                      キャンセル
                                    </button>
                                    <button
                                      id="ok_button"
                                      class="uk-button uk-button-default uk-modal-close"
                                      type="button"
                                      @click="deleteComment(comment.id)"
                                    >
                                      OK
                                    </button>
                                  </p>
                                </div>
                              </div>
                            </div>
                          </article>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <!-- </div> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import CommentForm from "@/components/CommentForm";
import Map from "@/components/Map";
import api from "@/services/api";

export default {
  name: "detail",
  components: {
    CommentForm,
    Map,
  },
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY/MM/DD HH:mm");
    },
  },
  props: ["post_id"],
  data() {
    return {
      comments: [],
      post: [],
      author: [],
      likeId: "",
      isLiked: false,
      likeCount: "",
      isLoading: true,
      isProcessing: false,
    };
  },
  computed: {
    login_user_id() {
      return this.$store.getters["auth/id"];
    },
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },
    modal_href() {
      return "#" + "map_modal" + this.post.id;
    },
    modal() {
      return "map_modal" + this.post.id;
    },
  },
  mounted() {
    api.get("/posts/" + this.post_id + "/").then((response) => {
      this.author = response.data.author;
      this.post = response.data;
    });
    this.confirmLiked();
    this.getLikeCount();
    this.CommentGet();
  },
  methods: {
    async confirmLiked() {
      if (this.login_user_id) {
        await api
          .get("/likes/", {
            params: {
              author: this.login_user_id,
              post: this.post_id,
            },
          })
          .then((response) => {
            console.log(response.data.results);
            if (response.data.results[0]) {
              this.likeId = response.data.results[0].id;
              this.isLiked = true;
            }
          });
      }
    },
    getLikeCount() {
      api.get("/posts/" + this.post_id + "/").then((response) => {
        this.likeCount = response.data.likes_count;
        this.isLoading = false;
      });
    },
    toggleLike() {
      if (this.isLoggedIn) {
        if (this.isProcessing) return;
        this.isProcessing = true;
        this.isLiked ? this.removeLike() : this.addLike();
        return new Promise((resolve) => {
          setTimeout(() => {
            this.isProcessing = false;
            resolve();
          }, 500);
        });
      } else {
        this.$router.replace("/login");
      }
    },
    addLike() {
      console.log("addLike");
      this.likeCount += 1;
      this.isLiked = true;
      this.confirmLiked;
      this.getLikeCount;
      api
        .patch("/posts/like/" + this.post_id + "/", {
          likes_count: this.likeCount,
        })
        .then(this.getLikeCount)
        .then(this.confirmLiked);
      api.post("/likes/", {
        author: this.login_user_id,
        post_id: this.post_id,
      });
    },
    removeLike() {
      console.log("removeLike");
      this.likeCount -= 1;
      this.isLiked = false;
      this.confirmLiked;
      this.getLikeCount;
      api
        .patch("/posts/like/" + this.post_id + "/", {
          likes_count: this.likeCount,
        })
        .then(this.getLikeCount)
        .then(this.confirmLiked);

      api.delete("/likes/" + this.likeId + "/");
    },
    CommentGet() {
      api.get("/comments/?post=" + this.post_id).then((response) => {
        this.comments = response.data;
      });
    },
    deleteComment(comment_id) {
      api.delete("/comments/" + comment_id + "/").then(this.CommentGet);
    },

    async showMap() {
      await this.$refs.map.initializeMap();
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

html {
  overflow: overlay;
}
#content {
  margin: 0px auto 10px;
}
.show_user {
  text-decoration: none;
  line-height: 45px;
  font-size: large;
  float: left;
  color: #333333;
}
.show_user:hover {
  color: rgba(90, 84, 75, 0.7);
}

.v-application ol,
.v-application ul {
  padding-left: 0px;
}
.user_icon {
  width: 35px;
  height: 35px;
  margin-right: 5px;
  border-radius: 50%;
}
.comment_user_icon {
  width: 30px;
  height: 30px;
  margin-right: 5px;
  border-radius: 50%;
}
#detail_post {
  background-color: rgba(225, 215, 205, 0.247);
}

#post_title {
  padding-top: 10px;
  font-size: 35px;
  font-weight: bold;
  margin-bottom: 0px;
}
#post_content {
  word-break: break-all;
  margin: 0px 0px 10px 0px;
  border-radius: 5px;
  background-color: rgba(224, 215, 196, 0.432);
  padding: 5px 5px 5px 10px;
  max-width: 625px;
  font-size: 15px;
  font-weight: bold;
  white-space: pre-wrap;
}
#post_image {
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
}

#location_button {
  float: left;
  margin-top: 18px;
  background-color: rgba(135, 165, 179, 0.829);
  color: #333;
  font-size: 20px;
  border-radius: 5px;
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.3);
}
#like_buttun {
  max-width: 640px;
  text-align: right;
}

.like_count {
  font-size: 40px;
  position: relative;
  top: 8px;
}

#author_name {
  position: relative;
  top: 3px;
  margin-left: 10px;
  font-size: 20px;
}

.timestamp {
  max-width: 640px;
  font-size: 12px;
  text-align: right;
}
.prefecture {
  max-width: 640px;
  font-size: 18px;
  text-align: right;
}

.logbox {
  height: 590px;
  overflow-y: scroll;
  overflow-y: overlay;
}

#location_modal.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: rgb(240, 240, 240);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#location_modal.uk-modal-body {
  display: flow-root;
  padding: 0px 0px;
  border-radius: 10px;
}
#delete_modal.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 5px auto;
  width: 600px;
  max-width: calc(100% - 0.01px) !important;
  background: rgb(240, 240, 240);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#delete_modal.uk-modal-body {
  display: flow-root;
  border-radius: 5px;
}

#delete-icon {
  text-align: right;
}

/* UIkitの上書き */
.uk-card-body {
  padding: 20px 40px;
}

.uk-comment-primary {
  background-color: #fff;
  padding: 15px 15px 5px 15px;
  border-left: 4px solid black;
  border-bottom: 1px solid black;
}
.uk-comment-header {
  margin-bottom: 10px;
}

.uk-comment-list > :nth-child(n + 2) {
  margin-top: 0px;
}
ul.uk-comment-list {
  margin: 0;
}

@media (max-width: 640px) {
  #location_modal.uk-modal-body {
    display: flow-root;
    padding: 0px 0px;
    border-radius: 10px;
  }
}
</style>
