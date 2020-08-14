<template>
  <div>
    <PostList :postType="previousPosts" :user_id="auth_id" />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import PostList from "@/components/PostList";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },
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
