<template>
  <div>
    <PostList :postType="latestPosts" />
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import { mapGetters } from "vuex";
export default {
  components: {
    PostList,
  },
  computed: mapGetters("post", ["latestPosts"]),
  created() {
    this.$store.dispatch("post/getAllPosts");
  },
};
</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
  -webkit-appearance: none;
}
</style>
