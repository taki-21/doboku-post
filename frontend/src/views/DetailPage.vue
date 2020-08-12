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
                    class="router-link"
                    :to="{name: 'mypage', params:{user_id: post.author.id}}"
                  >
                    <img class="user_icon" :src="post.author.icon_image" />
                    <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                  </router-link>
                  <p id="post_title">{{post.title}}</p>
                  <div uk-lightbox>
                    <a :href="post.image">
                      <img :src="post.image_change" />
                    </a>
                  </div>
                  <div id="like_buttun">
                    <div
                      v-if="this.likes.map((obj) => obj.user).includes(this.$store.getters['auth/id'])"
                    >
                      <div>
                        <span @click="toggleLike">
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
                        <span uk-icon="icon: heart; ratio: 2.5" @click="toggleLike"></span>
                        <span class="like_count">{{ likeCount }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="uk-width-2-5">
                  <div>
                    <button
                      class="uk-button uk-button-default comment_button"
                      type="button"
                      uk-toggle="target: .toggle-usage"
                    >
                      <span uk-icon="icon: comment"></span>
                      コメントを投稿する
                    </button>
                    <div class="toggle-usage"></div>
                    <div class="toggle-usage" hidden>
                      <CommentForm :post="post" @CommentGet="CommentGet" />
                    </div>
                  </div>

                  <ul class="uk-comment-list">
                    <li v-for="comment in comments" :key="comment.id">
                      <article
                        class="uk-comment uk-comment-primary uk-visible-toggle"
                        tabindex="-1"
                      >
                        <header class="uk-comment-header uk-position-relative">
                          <div>
                            <img class="comment_user_icon" :src="comment.author.icon_image" />
                            <strong>{{comment.author.username}}</strong>
                            <span>{{comment.timestamp | moment }}</span>
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
</template>

<script>
import moment from "moment";
import MyHeader from "@/components/MyHeader";
import CommentForm from "@/components/CommentForm";

import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  name: "detail",
  components: {
    MyHeader,
    CommentForm,
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
      api
        .post("/likes/", {
          user: this.$store.getters["auth/id"],
          post_id: this.post.id,
        })
        .then(() => {
          this.$store.dispatch("post/getAllLikes", { post_id: this.id });
        });
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
    back() {
      // 1つ前へ
      this.$router.back();
    },
  },
};
</script>

<style scoped>
.router-link {
  text-decoration: none;
  color: black;
}

.v-application ol,
.v-application ul {
  padding-left: 0px;
}
.user_icon {
  width: 40px;
  height: 40px;
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
  font-size: 20px;
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

.like_count {
  font-size: 40px;
  position: relative;
  top: 8px;
  left: 8px;
}
</style>
