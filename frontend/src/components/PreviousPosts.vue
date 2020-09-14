<template>
  <div>
    <PostList :postType="previousPosts" :user_id="auth_id" @parentPostDelete="parentPostDelete" />
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
      auth_id: this.$store.getters["auth/id"],
    };
  },
  watch: {
    $store(){
      this.$store.dispatch("post/getAllPosts");
    }
  },
  computed: {
    ...mapGetters("post", {
      posts: "latestPosts",
    }),
    previousPosts: function () {
      return this.posts.filter((x) => x.author.id == this.user_id);
    },
  },
  methods: {
    parentPostDelete() {
      this.$store.dispatch("post/getAllPosts");

    },
  },
};
</script>
