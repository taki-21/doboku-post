<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList
        :postType="previousPosts"
        :user_id="auth_id"
        @parentPostDelete="parentPostDelete"
      />
      <div v-if="previousPosts == ''">
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
import { watchScrollPosition } from "@/mixins/utility";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },
  mixins: [watchScrollPosition],
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
      this.getPosts();
    },
    loading() {
      this.$nextTick(() => {
        var positionY = sessionStorage.getItem("positionY");
        console.log(positionY);
        scrollTo(0, positionY);
        setTimeout(function () {
          scrollTo(0, positionY);
        });
      });
    },
  },
  async mounted() {
    if (sessionStorage.getItem("infinitePage_previous")) {
      const page_infinite = sessionStorage.getItem("infinitePage_previous");
      for (let i = 1; i <= page_infinite; i++) {
        console.log("page:" + page_infinite);
        await api
          .get("/posts/", {
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
            this.previousPosts.push(...data.results);
          });
      }
      this.loading = false;
    } else {
      this.getPosts();
    }

    // this.getPosts();
  },
  methods: {
    async getPosts() {
      await api.get("/posts/?author=" + this.user_id).then((response) => {
        this.previousPosts = response.data.results;
        if (response.data.next !== null) {
          this.nextPage = true;
        }
      });
      this.loading = false;
    },
    parentPostDelete(post_id) {
      api.delete("/posts/" + post_id + "/").then(this.getPosts);
    },
    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem("infinitePage_previous", this.page);

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
                this.nextPage = false;
                this.previousPosts.push(...data.results);
                $state.complete();
              } else {
                this.previousPosts.push(...data.results);
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
#none_message {
  font-size: 18px;
  text-align: center;
}

.loader {
  text-align: center;
  position: relative;
  top: 20px;
}
</style>
