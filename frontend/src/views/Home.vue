<template>
  <div id="home-page">
    <GlobalHeader />
    <GlobalMessage />
    <MyHeader></MyHeader>
    <div>
      <div
        class="uk-grid-column-small uk-grid-row-large uk-child-width-1-3@s uk-text-center"
        uk-grid
      >
        <div v-for="(post, key) in posts" :key="key">
          <div class="uk-card uk-card-hover uk-card-default" id="card">
            <div class="uk-card-media-top">
              <img v-bind:src="post.image" />
            </div>
            <div class="uk-card-body">
              <div class="uk-comment-header uk-position-relative">
                <div>
                  <img class="user_icon" v-bind:src="post.author.icon_image" />
                  <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                </div>
              </div>
              <strong>{{ post.title }}</strong>
              <p class="post_content">
                <span>--</span>
                {{ post.content }}
              </p>
              <div class="comment_like_icon">
                <i id="heart-button" uk-icon="comment"></i>
                <span id="comment-count"></span>
                <i id="heart-button" uk-icon="heart"></i>
                <span id="like-count"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p>{{ posts }}</p>
  </div>
</template>

<style scoped>
.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}
</style>
<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";

import MyHeader from "../components/MyHeader";
import router from "../router";
export default {
  components: {
    MyHeader,
    GlobalHeader,
    GlobalMessage
  },
  data() {
    return {
      posts: null
    };
  },
  mounted() {
    this.axios.get("/posts/").then(response => {
      this.posts = response.data;
    });
    this.checkLoggedIn();
  },
  methods: {
    checkLoggedIn() {
      this.$session.start();
      if (!this.$session.has("token")) {
        router.push("/login");
      }
    }
  }
};
</script>
