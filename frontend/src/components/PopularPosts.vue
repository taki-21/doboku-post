<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="popularPosts" />
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
import { watchScrollPosition } from "@/mixins/utility";

export default {
  components: {
    PostList,
  },
  mixins: [watchScrollPosition],
  data() {
    return {
      page: 1,
      popularPosts: [],
      loading: true,
      nextPage: false,
    };
  },
  async mounted() {
    if (sessionStorage.getItem("infinitePage_popular")) {
      const page_infinite = sessionStorage.getItem("infinitePage_popular");
      for (let i = 1; i <= page_infinite; i++) {
        await api
          .get("/posts/?order_by=-likes_count", {
            params: {
              page: i,
            },
          })
          .then(({ data }) => {
            if (data.next !== null) {
              this.nextPage = true;
            } else {
              this.nextPage = false;
            }
            this.popularPosts.push(...data.results);
          });
      }
      this.loading = false;
    } else {
      this.getPosts();
    }
  },
  methods: {
    async getPosts() {
      await api.get("/posts/?order_by=-likes_count").then((response) => {
        this.popularPosts = response.data.results;
        if (response.data.next !== null) {
          this.nextPage = true;
        }
      });
      this.loading = false;
    },
    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem("infinitePage_popular", this.page);
      api
        .get("/posts/?order_by=-likes_count", {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                this.popularPosts.push(...data.results);
                $state.complete();
              } else {
                this.popularPosts.push(...data.results);
                // this.page += 1;
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
