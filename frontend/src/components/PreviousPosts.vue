<template>
  <div>
    <PostList :postType="previousPosts" :user_id="auth_id" @parentPostDelete="parentPostDelete" />
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import api from "@/services/api";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },
  data() {
    return {
      auth_id: this.$store.getters["auth/id"],
      previousPosts: [],
    };
  },
  watch: {
    $route() {
      this.getPreviousPosts();
    },
  },
  mounted() {
    this.getPreviousPosts();
  },
  methods: {
    parentPostDelete(post_id) {
      api.delete("/posts/" + post_id + "/").then(
        this.getPreviousPosts
      )
    },
    getPreviousPosts() {
      api.get("/posts/?author=" + this.user_id).then((response) => {
        this.previousPosts = response.data;
      });
    },
  },
};
</script>
