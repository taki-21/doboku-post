<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="popularPosts" />
    </div>
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import api from "@/services/api";

export default {
  components: {
    PostList,
  },
  data() {
    return {
      latestPosts: [],
      loading: true,
    };
  },
  mounted() {
    api.get("/posts/").then((response) => {
      this.latestPosts = response.data;
      this.loading = false;
    });
  },
  computed: {
    popularPosts() {
      return this.latestPosts.slice().sort(function (a, b) {
        return a.likes_count < b.likes_count
          ? 1
          : a.likes_count > b.likes_count
          ? -1
          : 0;
      });
    },
  },
};
</script>

<style scoped>
.loader {
  text-align: center;
  position: relative;
  top: 20px;
}
</style>
