<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="previousPosts" :user_id="auth_id" @parentPostDelete="parentPostDelete" />
      <div v-if="nextPage">
        <infinite-loading spinner="spiral" @infinite="infiniteHandler">
          <span id="no_results" slot="no-results"></span>
        </infinite-loading>
      </div>
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
      page: 1,
      loading: true,
      nextPage: false,
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
    getPreviousPosts() {
      api.get("/posts/?author=" + this.user_id).then((response) => {
        this.previousPosts = response.data.results;
        this.loading = false;
        if (response.data.next !== null) {
          this.nextPage = true;
        }
      });
    },
    parentPostDelete(post_id) {
      api.delete("/posts/" + post_id + "/").then(this.getPreviousPosts);
    },
    infiniteHandler($state) {
      this.page += 1;
      api
        .get("/posts/", {
          params: {
            page: this.page,
            author: this.user_id,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            // this.loading = false;
            if (data.results.length) {
              if (data.next === null) {
                this.previousPosts.push(...data.results);
                $state.complete();
              } else {
                this.previousPosts.push(...data.results);
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
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
