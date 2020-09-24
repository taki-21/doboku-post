<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="popularPosts" />
      <div v-if="nextPage">
        <infinite-loading spinner="spiral" @infinite="infiniteHandler">
          <span id="no_results" slot="no-results">投稿は以上です</span>
        </infinite-loading>
      </div>
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
      nextPage: false,
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
      this.page += 1;
      api
        .get("/posts/", {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            if (data.results.length) {
              if (data.next === null) {
                this.prePopularPosts.push(...data.results);
                $state.complete();
              } else {
                this.prePopularPosts.push(...data.results);
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
  mounted() {
    api.get("/posts/").then((response) => {
      this.prePopularPosts = response.data.results;
      this.loading = false;
      if (response.data.next !== null) {
        this.nextPage = true;
      }
    });
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
