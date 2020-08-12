<template>
  <div>
    <PostList :postType="popularPosts" />
  </div>
</template>

<script>
import PostList from "@/components/PostList";

export default {
  components: {
    PostList,
  },
  computed: {
    popularPosts: function () {
      return this.$store.getters["post/popularPosts"];
    },
  },
};
</script>
