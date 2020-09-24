<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="popularPosts" />
      <infinite-loading spinner="spiral" @infinite="infiniteHandler">
        <span id="no_results" slot="no-results">投稿は以上です</span>
      </infinite-loading>
    </div>
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import InfiniteLoading from "vue-infinite-loading";
import api from "@/services/api";

export default {
  components: {
    PostList,
    InfiniteLoading,
  },
  data() {
    return {
      page: 1,
      prePopularPosts: [],
      loading: true,
    };
  },
  computed: {
    popularPosts() {
      return this.prePopularPosts.slice().sort(function (a, b) {
        return a.likes_count < b.likes_count
          ? 1
          : a.likes_count > b.likes_count
          ? -1
          : 0;
      });
    },
  },
  methods: {
    infiniteHandler($state) {
      api
        .get("/posts/", {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            this.loading = false;
            if (data.results.length === 12) {
              this.page += 1;
              this.prePopularPosts.push(...data.results);
              if ($state) {
                $state.loaded();
              }
            } else {
              $state.complete();
            }
            if (data.results.length < 12) {
              this.prePopularPosts.push(...data.results);
              $state.complete();
            }
          }, 500);
        })
        .catch(() => {
          $state.complete();
        });
    },
  },
  created() {
    this.infiniteHandler();
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
