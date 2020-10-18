<template>
  <div>
    <div v-show="isLoading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!isLoading">
      <PostList :postType="likedPosts" />
      <div v-if="likedPosts == ''">
        <p id="none_message">まだ投稿がありません</p>
      </div>
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
import { watchScrollPosition, clearSession } from "@/mixins/utility";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },
  mixins: [watchScrollPosition, clearSession],
  data() {
    return {
      page: 1,
      isLoading: true,
      nextPage: false,
      likedPosts: [],
      sessionKey: "infinitePage_liked",
    };
  },
  async mounted() {
    if (sessionStorage.getItem(this.sessionKey)) {
      const page_infinite = sessionStorage.getItem(this.sessionKey);
      for (let i = 1; i <= page_infinite; i++) {
        await api
          .get("/likes/", {
            params: {
              page: i,
              author: this.user_id,
            },
          })
          .then(({ data }) => {
            if (data.next !== null) {
              this.nextPage = true;
            } else {
              this.nextPage = false;
            }
            this.likedPosts.push(...data.results.map((like) => like.post));
          });
      }
      this.isLoading = false;
    } else {
      this.clearSession()
      this.getPosts();
    }
  },
  methods: {
    async getPosts() {
      await api
        .get("/likes/", {
          params: {
            author: this.user_id,
          },
        })
        .then((response) => {
          this.likedPosts = response.data.results.map((like) => like.post);
          if (response.data.next !== null) {
            this.nextPage = true;
          }
        });
      this.isLoading = false;
    },

    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem(this.sessionKey, this.page);
      api
        .get("/likes/", {
          params: {
            page: this.page,
            author: this.user_id,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                this.likedPosts.push(...data.results.map((like) => like.post));
                $state.complete();
              } else {
                this.likedPosts.push(...data.results.map((like) => like.post));
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
};
</script>

<style>
@import '../assets/common.css';
</style>
