<template>
  <div>
    <MyHeader />
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <div id="detail_post">
        <div class="uk-width-1-1">
          <div class="uk-container">
            <div class>
              <a @click="$router.back()" title="前ページへ戻る">
                <i id="back_icon" uk-icon="icon: chevron-double-left; ratio: 2"></i>
              </a>
              <div class="uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large">
                <div uk-grid>
                  <div class="uk-width-3-5">
                    <div>
                      <router-link
                        class="show_user"
                        v-if="author.id"
                        :to="{name: 'mypage', params:{user_id: author.id}}"
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
                      <div id="post_title">{{post.title}}</div>
                      <div id="post_content">{{post.content}}</div>
                    </div>

                    <div uk-lightbox>
                      <a :href="post.raw_image">
                        <img :src="post.image" />
                      </a>
                    </div>
                    <div>
                      <button
                        id="location_button"
                        class="uk-button uk-button-default uk-button-large"
                        :href="modal_href"
                        type="button"
                        @click="callChildMethod"
                        uk-toggle
                      >場所を確認する</button>
                      <div :id="modal" class="uk-flex-top .uk-width-large" uk-modal>
                        <div class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
                          <button class="uk-modal-close-default" type="button" uk-close></button>
                          <div>
                            <Map ref="map" :post="post" />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div id="like_buttun">
                      <div v-if="isLiked">
                        <div>
                          <span class="like_icon" @click="toggleLike">
                            <svg
                              width="50"
                              height="50"
                              viewBox="0 0 20 20"
                              xmlns="http://www.w3.org/2000/svg"
                              data-svg="heart"
                            >
                              <path
                                fill="indianred"
                                stroke="currentcolor"
                                stroke-width="1"
                                d="M10,4 C10,4 8.1,2 5.74,2 C3.38,2 1,3.55 1,6.73 C1,8.84 2.67,10.44 2.67,10.44 L10,18 L17.33,10.44 C17.33,10.44 19,8.84 19,6.73 C19,3.55 16.62,2 14.26,2 C11.9,2 10,4 10,4 L10,4 Z"
                              />
                            </svg>
                          </span>
                          <span class="like_count">{{ likeCount }}</span>
                        </div>
                      </div>
                      <div v-else>
                        <div>
                          <span
                            class="like_icon"
                            uk-icon="icon: heart; ratio: 2.5"
                            @click="toggleLike"
                          ></span>
                          <span class="like_count">{{ likeCount }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="uk-width-2-5">
                    <div class="right_column">
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
                                <header class="uk-comment-header uk-position-relative">
                                  <div>
                                    <router-link
                                      class="show_user"
                                      :to="{name: 'mypage', params:{user_id: comment.author.id}}"
                                    >
                                      <img
                                        class="comment_user_icon"
                                        :src="comment.author.icon_image"
                                      />
                                      <strong>{{comment.author.username}}</strong>
                                    </router-link>
                                    <div class="timestamp">
                                      <span>{{comment.timestamp | moment }}</span>
                                    </div>
                                  </div>
                                </header>
                                <div>
                                  <div>{{comment.text}}</div>
                                </div>
                                <div id="delete-icon" v-if="comment.author.id == login_user_id">
                                  <a class="delete-link" :href="'#modal-' + comment.id" uk-toggle>
                                    <i id="delete-icon" uk-icon="icon: trash"></i>
                                  </a>
                                  <div :id="'modal-' + comment.id" uk-modal>
                                    <div class="uk-modal-dialog uk-modal-body">
                                      <h2 class="uk-modal-title">削除確認</h2>
                                      <p>コメント：{{ comment.text }}を削除します。よろしいですか？</p>
                                      <p class="uk-text-right">
                                        <button
                                          id="cancel_button"
                                          class="uk-button uk-button-default uk-modal-close"
                                          type="button"
                                        >キャンセル</button>
                                        <button
                                          class="uk-button uk-button-primary uk-modal-close"
                                          type="button"
                                          @click="deleteComment(comment.id)"
                                        >OK</button>
                                      </p>
                                    </div>
                                  </div>
                                </div>
                              </article>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
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
import MyHeader from "@/components/MyHeader";
import CommentForm from "@/components/CommentForm";
import Map from "@/components/Map";
import api from "@/services/api";

export default {
  name: "detail",
  components: {
    MyHeader,
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
      loading: true,
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
  methods: {
    confirmLiked() {
      if (this.login_user_id) {
        api
          .get("/likes/", {
            params: {
              user: this.login_user_id,
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
        this.loading = false;
      });
    },
    toggleLike() {
      if (this.isLoggedIn) {
        this.isLiked ? this.removeLike() : this.addLike();
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
      api.patch("/posts/" + this.post_id + "/", {
        likes_count: this.likeCount,
      });
      api
        .post("/likes/", {
          user: this.login_user_id,
          post_id: this.post_id,
        })
        .then(this.getLikeCount)
        .then(this.confirmLiked);
    },
    removeLike() {
      console.log("removeLike");
      this.likeCount -= 1;
      this.isLiked = false;
      this.confirmLiked;
      this.getLikeCount;
      api.patch("/posts/" + this.post_id + "/", {
        likes_count: this.likeCount,
      });

      api
        .delete("/likes/" + this.likeId + "/")
        .then(this.getLikeCount)
        .then(this.confirmLiked);
    },
    CommentGet() {
      api.get("/comments/?post=" + this.post_id).then((response) => {
        this.comments = response.data;

        console.log("this.comments: " + response.data);
      });
    },
    deleteComment(comment_id) {
      api.delete("/comments/" + comment_id + "/").then(this.CommentGet);
    },

    callChildMethod() {
      this.$refs.map.initializeMap();
    },
    back() {
      // 1つ前へ
      this.$router.back();
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
};
</script>

<style scoped>
.loader {
  text-align: center;
  position: relative;
  top: 20px;
}
html {
  overflow: overlay;
}
#back_icon {
  color: rgba(139, 138, 135, 0.85);
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
  padding-top: 10px;
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
}

.uk-comment-primary {
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

#location_button {
  float: left;
  margin-top: 10px;
  /* width: 40%; */
}

#location_button.uk-button-default {
  background-color: rgb(238, 237, 235);
  color: #333;
  font-size: 20px;
  border: 2px solid #696464;
  border-radius: 15px;
}
#like_buttun {
  max-width: 640px;
  text-align: right;
}
.like_icon {
  position: relative;
  right: 8px;
}
.like_icon:hover {
  cursor: pointer;
}
.like_count {
  font-size: 40px;
  position: relative;
  top: 8px;
  /* left: 8px; */
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
.right_column {
  height: 100%;
}

.logbox {
  /* border: solid 1px #808080; */
  /* margin-top: 40px; */
  height: 560px;
  /* max-height: -webkit-fill-available; */
  overflow-y: scroll;
  overflow-y: overlay;
}
.logbox::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-thumb {
  background-color: rgba(208, 210, 212, 0.993);
  /* border: 1px solid #ccc; */
  border-right: none;
}
::-webkit-scrollbar-track {
  background: transparent;
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
  background: #fff;
  /* opacity: 0; */
  /* transform: translateY(-100px); */
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#none_message {
  text-align: center;
  margin-top: 20px;
}
#delete-icon {
  text-align: right;
}
.delete-link {
  text-decoration: none;
  color: rgb(51, 51, 51);
}
.uk-modal-body {
  display: flow-root;
  padding: 30px 30px;
  border-radius: 5px;
}
</style>
