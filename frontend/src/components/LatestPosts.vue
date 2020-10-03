<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="latestPosts" />
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
      latestPosts: [],
      loading: true,
      nextPage: false,
      infinite_num: 1,
      // infiniteId: 0,
    };
  },
  watch: {
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
    // this.getPosts();
    if (sessionStorage.getItem("infinitePage")) {
      const page_infinite = sessionStorage.getItem("infinitePage");
      for (let i = 1; i <= page_infinite; i++) {
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
            this.latestPosts.push(...data.results);
            console.log("latestPosts" + this.latestPosts);
          });
      }
      this.loading = false;
    } else {
      this.getPosts();
    }
    // this.loading = false;

    // this.nextPage = JSON.parse(sessionStorage.getItem("nextpage"));
    // sessionStorage.removeItem('posts')
    // const session_posts = sessionStorage.getItem("posts");
    // if (sessionStorage.getItem("posts")) {
    //   console.log("session");
    //   this.latestPosts = JSON.parse(sessionStorage.getItem("posts"));
    //   this.loading = false;
    // } else {
    // api.get("/posts/").then((response) => {
    //   this.latestPosts = response.data.results;
    //   this.loading = false;
    //   if (response.data.next !== null) {
    //     this.nextPage = true;
    //     // sessionStorage.setItem("nextpage", JSON.stringify(this.nextPage));
    //   }
    //   // sessionStorage.setItem("posts", JSON.stringify(this.latestPosts));
    // });
  },
  methods: {
    async getPosts() {
      await api.get("/posts/").then((response) => {
        this.latestPosts = response.data.results;
        if (response.data.next !== null) {
          this.nextPage = true;
        }
      });
      this.loading = false;
    },
    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem("infinitePage", this.page);
      api
        .get("/posts/", {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            // this.loading = false;
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                // sessionStorage.setItem(
                //   "nextpage",
                //   JSON.stringify(this.nextPage)
                // );
                this.latestPosts.push(...data.results);
                // sessionStorage.setItem(
                //   "posts",
                //   JSON.stringify(this.latestPosts)
                // );
                $state.complete();
              } else {
                this.latestPosts.push(...data.results);
                // sessionStorage.setItem(
                //   "posts",
                //   JSON.stringify(this.latestPosts)
                // );
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
          // this.infiniteId++;
          // this.infinite++;
        });
    },
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
#no_results {
  font-weight: bold;
}
</style>
