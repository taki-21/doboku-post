<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="latestPosts" />
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
};
</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
  -webkit-appearance: none;
}
.loader {
  text-align: center;
  position: relative;
  top: 20px;
}
</style>
