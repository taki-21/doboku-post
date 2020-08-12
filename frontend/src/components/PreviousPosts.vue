<template>
  <div>
    <div
      class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
      uk-grid
    >
      <router-link
        class="router-link"
        :to="{name: 'detail', params:{id: post.id }}"
        v-for="(post, key) in previousPosts"
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
            <div v-if="user_id == auth_id">
              <div>
                <router-link :to="{name: 'post_edit', params:{post_id: post.id }}">
                  <i uk-icon="icon: pencil"></i>
                </router-link>
                <!-- @click="DestroyPost(post.id)"" -->
                <a :href="'#modal-' + post.id" uk-toggle>
                  <i uk-icon="icon: trash"></i>
                </a>
                <div :id="'modal-' + post.id" uk-modal>
                  <div class="uk-modal-dialog uk-modal-body">
                    <h2 class="uk-modal-title">削除確認</h2>
                    <p>投稿：{{ post.title }}を削除します。よろしいですか？</p>
                    <p class="uk-text-right">
                      <button
                        class="uk-button uk-button-default uk-modal-close"
                        type="button"
                      >Cancel</button>
                      <button
                        class="uk-button uk-button-primary uk-modal-close"
                        type="button"
                        @click="DestroyPost(post.id)"
                      >OK</button>
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="comment_like_icon">
              <i id="heart-button" uk-icon="comment"></i>
              <span id="comment-count">{{ post.comments_count}}</span>
              <i id="heart-button" uk-icon="heart"></i>
              <span id="like-count">{{ post.likes_count }}</span>
            </div>
          </div>
        </div>
        <!-- <pre>{{ posts }}</pre> -->
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";
import moment from "moment";

export default {
  props: ["user_id"],
  data() {
    return {
      auth_id: this.$store.getters["auth/id"]
    };
  },
  computed: {
    ...mapGetters("post", {
      posts: "latestPosts"
    }),
    previousPosts: function() {
      return this.posts.filter(x => x.author.id == this.user_id);
    }
  },
  methods: {
    DestroyPost: function(post_id) {
      api.delete("/posts/" + post_id + "/").then(
        this.$store.dispatch("post/getAllPosts"),
        // ↓マイページにに飛ばしたいけどパラメータの付け方がわからない
        this.$router.replace("/")
      );
    }
  },
  created() {
    this.$store.dispatch("post/getAllPosts");
  },

  filters: {
    moment: function(date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
    }
  }
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
