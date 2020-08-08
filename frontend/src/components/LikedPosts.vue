<template>
  <div class="uk-grid-column-small uk-grid-row-large uk-child-width-1-3@s uk-text-center" uk-grid>
    <!-- <pre>{{ likedPosts }}</pre> -->
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
      <!-- <pre>{{ posts }}</pre> -->
    </router-link>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
import api from "@/services/api";

export default {
  props: ["user_id"],
  data() {
    return{
      likedPosts:[]
    }
  },
  // computed: {
  //   ...mapGetters("post", ["likedPosts"])
  // },
  mounted() {
    // this.$store.dispatch("post/getAllLikes", { user_id: this.user_id });
    api.get('/likes/', {
      params: {
        user: this.user_id
      }
    }).then(response => {
      this.likedPosts = response.data.map(like => like.post)
    })
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
