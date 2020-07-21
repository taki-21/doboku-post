<template>
  <div>
    <MyHeader></MyHeader>
    <div>
      <div class="uk-grid-column-small uk-grid-row-large uk-child-width-1-3@s uk-text-center" uk-grid>
        <div v-for="(post, key) in posts" :key="key">
          <div class="uk-card uk-card-hover uk-card-default" id="card">
            <div class="uk-card-media-top">
              <img v-bind:src="post.image">
            </div>
            <div class="uk-card-body">
              <div class="uk-comment-header uk-position-relative">
                <div>
                  <span class="uk-comment-title uk-margin-remove">{{ post.author }}</span>
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

<script>
import MyHeader from "../components/MyHeader";
export default {
  components: {
    MyHeader
  },
  data() {
    return {
      posts: null
    };
  },
  mounted() {
    this.axios.get("http://127.0.0.1:8000/api/posts/").then(response => {
      this.posts = response.data;
    });
  }
};
</script>
