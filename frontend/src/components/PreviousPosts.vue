<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="previousPosts" :user_id="auth_id" @parentPostDelete="parentPostDelete" />
    </div>
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
      loading: true,
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
      api.delete("/posts/" + post_id + "/").then(this.getPreviousPosts);
    },
    getPreviousPosts() {
      api.get("/posts/?author=" + this.user_id).then((response) => {
        this.previousPosts = response.data;
        this.loading = false;
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
