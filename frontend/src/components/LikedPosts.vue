<template>
  <div>
    <PostList :postType="likedPosts" />

    <!-- <div
      class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
      uk-grid
    >
      <router-link
        class="router-link"
        :to="{name: 'detail', params:{id: post.id }}"
        v-for="(post, key) in likedPosts"
        :key="key"
      >
        <div class="uk-card uk-card-hover uk-card-default" id="card">
          <div class="uk-card-media-top">
            <img :src="post.image_change" />
          </div>
          <div class="uk-card-body">
            <div class="uk-comment-header uk-position-relative">
              <div>
                <router-link
                  class="show_user"
                  :to="{name: 'mypage', params:{user_id: post.author.id}}"
                >
                  <div>
                    <img class="user_icon" v-bind:src="post.author.icon_image" />
                    <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                  </div>
                </router-link>
                <div class="timestamp">
                  <span>{{ post.published_at | moment }}</span>
                </div>
              </div>
            </div>
            <strong>{{ post.title }}</strong>
            <p class="post_content">
              <span>--</span>
              {{ post.content }}
            </p>
            <div class="comment_like_icon">
              <i id="heart-button" uk-icon="comment"></i>
              <span id="comment-count">{{ post.comments_count}}</span>
              <i id="heart-button" uk-icon="heart"></i>
              <span id="like-count">{{ post.likes_count }}</span>
            </div>
          </div>
        </div>
      </router-link>
    </div>-->
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
import PostList from "@/components/PostList";

import api from "@/services/api";
import moment from "moment";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },

  data() {
    return {
      likedPosts: [],
    };
  },
  computed: {
    // ...mapGetters("post", ["likedPosts"])
  },
  mounted() {
    // this.$store.dispatch("post/getAllLikes", { user_id: this.user_id });
    api
      .get("/likes/", {
        params: {
          user: this.user_id,
        },
      })
      .then((response) => {
        this.likedPosts = response.data.map((like) => like.post);
      });
  },
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
    },
  },
};
</script>


<style scoped>
.router-link {
  text-decoration: none;
}

.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

#card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #eaeeee;
  margin-bottom: 20px;
}

.timestamp {
  font-size: 12px;
  text-align: right;
}
.show_user {
  text-decoration: none;
  line-height: 45px;
  float: left;
  font-size: large;
  font-weight: bold;
  color: #333333;
}

.post_content {
  width: 100%;
  font-size: small;
  height: 40px;
}

p {
  margin: 0;
}

.comment_like_icon {
  text-align: right;
}

#comment-count {
  margin-right: 5px;
}

#like-count {
  line-height: 30px;
  font-size: 17px;
}

/* UIkitの上書き */
.uk-card-body {
  padding: 10px 20px;
}

.uk-comment-header {
  display: flow-root;
  margin-bottom: 0px;
}
</style>
