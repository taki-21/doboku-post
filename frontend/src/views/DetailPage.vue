<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div id="detail_post">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class>
            <a @click="$router.back()" title="前ページへ戻る">
              <i uk-icon="icon: chevron-double-left; ratio: 2"></i>
            </a>
            <div class="uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large">
              <div uk-grid>
                <div class="uk-width-3-5">
                  <router-link
                    class="show_user"
                    :to="{name: 'mypage', params:{user_id: post.author.id}}"
                  >
                    <img class="user_icon" :src="post.author.icon_image" />
                    <span id="author_name">{{ post.author.username }}</span>
                  </router-link>
                  <div class="timestamp">
                    <span>{{ post.published_at | moment }}</span>
                  </div>
                  <div class="prefecture">
                    <span>{{ post.prefecture }}</span>
                  </div>

                  <div id="title-content">
                    <p id="post_title">{{post.title}}</p>
                    <p id="post_content">{{post.content}}</p>
                  </div>

                  <div uk-lightbox>
                    <a :href="post.image">
                      <img :src="post.image_change" />
                    </a>
                  </div>
                  <div>
                    <button
                      id="location_button"
                      class="uk-button uk-button-default uk-button-large"
                      href="#modal-gmap"
                      type="button"
                      uk-toggle
                    >場所を確認する</button>
                    <div id="modal-gmap" class="uk-flex-top .uk-width-large" uk-modal>
                      <div class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
                        <button class="uk-modal-close-default" type="button" uk-close></button>
                        <div>
                          <Map ref="map" :post="post" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- <div id="like"> -->
                  <div id="like_buttun">
                    <div
                      v-if="this.likes.map((obj) => obj.user).includes(this.$store.getters['auth/id'])"
                    >
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
                  <!-- </div> -->
                </div>
                <div class="uk-width-2-5">
                  <div class="right_column">
                    <div>
                      <button
                        class="uk-button uk-button-default comment_button"
                        type="button"
                        uk-toggle="target: .toggle-usage"
                        @click="post_comment"
                      >
                        <span uk-icon="icon: comment"></span>
                        コメントを投稿する
                      </button>
                      <div class="toggle-usage" hidden>
                        <CommentForm :post="post" @CommentGet="CommentGet" />
                      </div>
                    </div>
                    <div class="logbox">
                      <ul class="uk-comment-list">
                        <li v-for="comment in comments" :key="comment.id">
                          <article
                            class="uk-comment uk-comment-primary uk-visible-toggle"
                            tabindex="-1"
                          >
                            <header class="uk-comment-header uk-position-relative">
                              <div>
                                <!-- <pre>{{comment.author.id}}</pre> -->
                                <router-link
                                  class="show_user"
                                  :to="{name: 'mypage', params:{user_id: comment.author.id}}"
                                >
                                  <img class="comment_user_icon" :src="comment.author.icon_image" />
                                  <strong>{{comment.author.username}}</strong>
                                </router-link>
                                <div class="timestamp">
                                  <span>{{comment.timestamp | moment }}</span>
                                </div>
                              </div>
                            </header>
                            <div>
                              <p>{{comment.text}}</p>
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
</template>

<script>
import moment from "moment";
import MyHeader from "@/components/MyHeader";
import CommentForm from "@/components/CommentForm";
import Map from "@/components/Map";

import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  name: "detail",
  components: {
    MyHeader,
    CommentForm,
    Map,
  },
  props: {
    id: { type: Number },
  },
  data() {
    return {
      comments: [],
    };
  },
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY/MM/DD HH:mm");
    },
  },
  computed: {
    ...mapGetters("post", ["latestPosts"]),
    post() {
      return this.latestPosts.find((post) => post.id === this.id);
    },
    ...mapGetters("post", {
      likeCount: "likeCount",
      likes: "likes",
    }),
    isLoggedIn: function () {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },

  mounted() {
    api.get("/comments/").then((response) => {
      this.comments = response.data.filter((x) => x.post === this.id);
    });
    this.$store.dispatch("post/getAllLikes", { post_id: this.id });
  },
  methods: {
    toggleLike() {
      const userIdList = this.likes.map((obj) => obj.user);
      userIdList.includes(this.$store.getters["auth/id"])
        ? this.removeLike()
        : this.addLike();
    },
    addLike() {
      if (this.isLoggedIn) {
        api
          .post("/likes/", {
            user: this.$store.getters["auth/id"],
            post_id: this.post.id,
          })
          .then(() => {
            this.$store.dispatch("post/getAllLikes", { post_id: this.id });
          });
      } else {
        this.$router.replace("/login");
      }
    },
    removeLike() {
      const path = this.likes.filter(
        (x) => x.user == this.$store.getters["auth/id"]
      )[0].id;
      api.delete("/likes/" + path + "/").then(() => {
        this.$store.dispatch("post/getAllLikes", { post_id: this.id });
      });
    },
    CommentGet() {
      api.get("/comments/").then((response) => {
        this.comments = response.data.filter((x) => x.post === this.id);
      });
    },
    post_comment() {
      if (this.isLoggedIn == false) {
        console.log("aaaaaaaaaaaaaaa");
        this.$router.replace("/login");
      }
    },
    back() {
      // 1つ前へ
      this.$router.back();
    },
  },
};
</script>

<style scoped>
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
  padding-top: 20px;
  font-size: 35px;
  font-weight: bold;
  margin-bottom: 0px;
}
#post_content {
  margin: 0px 0px 10px 0px;
  border-radius: 5px;
  background-color: rgb(238, 237, 235);
  padding: 10px 10px 10px 30px;
  max-width: 640px;
  font-size: 15px;
  font-weight: bold;
}

.uk-comment-primary {
  padding: 15px;
  border-left: 4px solid black;
  border-bottom: 1px solid black;
}
.uk-comment-header {
  margin-bottom: 10px;
}

.uk-comment-list > :nth-child(n + 2) {
  margin-top: 0px;
}

.comment_button {
  width: 100%;
}

#location_button {
  float: left;
  margin-top: 10px;
  width: 40%;
}

#location_button.uk-button-default {
  background-color: rgb(238, 237, 235);
  color: #333;
  font-size: 20px;
  border: 2px solid #696464;
  border-radius: 5px;
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
  height: 585px;
}
.logbox {
  /* border: solid 1px #808080; */
  margin-top: 20px;
  width: 100%;
  max-height: -webkit-fill-available;
  overflow: auto;
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
</style>
