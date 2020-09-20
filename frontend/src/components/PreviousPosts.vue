<template>
  <div>
    <pre>{{user_id}}</pre>
    <PostList :postType="previousPosts" :user_id="auth_id" @parentPostDelete="parentPostDelete" />
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
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
    // $store() {
    //   this.$store.dispatch("post/getAllPosts");
    // },
    $route() {
      this.getPreviousPosts();
    },
  },
  // computed: {
  //   ...mapGetters("post", {
  //     posts: "latestPosts",
  //   }),
  //   previousPosts: function () {
  //     return this.posts.filter((x) => x.author.id == this.user_id);
  //   },
  // },
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
