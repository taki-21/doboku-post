<template>
  <div class="uk-grid-column-small uk-grid-row-large uk-child-width-1-3@s uk-text-center" uk-grid>
    <div v-for="(post, key) in likedPosts" :key="key">
      <div class="uk-card uk-card-hover uk-card-default" id="card">
        <div class="uk-card-media-top">
          <img :src="post.image_change" />
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
            <span id="like-count">{{ post.like_count }}</span>
          </div>
        </div>
      </div>
      <pre>{{ posts }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      posts: [],
      id: this.$store.getters["auth/id"]
    };
  },
  mounted() {
    this.axios.get("http://127.0.0.1:8000/api/v1/posts/").then(response => {
      this.posts = response.data;
    });
  },
  computed: {
    username: function() {
      return this.$store.getters["auth/username"];
    },
    likedPosts: function() {
      return this.posts.filter(x =>
        x.like.includes(this.id)
      );
    },
  }
};
</script>


<style scoped>
.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

#card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #f7fcfc;
  margin-bottom: 20px;
}
</style>
