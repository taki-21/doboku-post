<template>
  <div
    class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
    uk-grid
  >
    <router-link
      class="router-link"
      :to="{name: 'detail', params:{id: post.id }}"
      v-for="(post, key) in posts"
      :key="key"
    >
      <div class="uk-card uk-card-hover uk-card-default" id="card">
        <div class="uk-card-media-top">
          <img v-bind:src="post.image_change" />
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
            <span id="like-count">{{ post.like_count}}</span>
          </div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed:{
    ...mapState('post', {'posts':'posts'})
  },
  created() {
    this.$store.dispatch("post/getAllPosts");
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
  background-color: #f7fcfc;
  margin-bottom: 20px;
}
</style>
