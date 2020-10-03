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
      // infinite: false,
      // infiniteId: 0,
    };
  },
  beforeRouteLeave(to, form, next) {
    // ストアのポストをクリア
    next();
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
    // latestPosts() {
    //   sessionStorage.setItem("posts", [this.latestPosts]);
    // },
    // infinite() {
    //   // if (this.infiniteId >= 2) {
    //     var positionY = sessionStorage.getItem("positionY");
    //     console.log(positionY);
    //     // scrollTo(0, positionY);
    //     setTimeout(function () {
    //       scrollTo(0, positionY);
    //     },500);
    //   // }
    // },
  },
  mounted() {
    this.nextPage = JSON.parse(sessionStorage.getItem("nextpage"));
    // sessionStorage.removeItem('posts')
    // const session_posts = sessionStorage.getItem("posts");
    if (sessionStorage.getItem("posts")) {
      console.log("session");
      this.latestPosts = JSON.parse(sessionStorage.getItem("posts"));
      this.loading = false;
    } else {
      console.log("else");
      api.get("/posts/").then((response) => {
        this.latestPosts = response.data.results;
        this.loading = false;
        if (response.data.next !== null) {
          this.nextPage = true;
          sessionStorage.setItem("nextpage", JSON.stringify(this.nextPage));
        }
        sessionStorage.setItem("posts", JSON.stringify(this.latestPosts));
      });
    }
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
            // this.loading = false;
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                sessionStorage.setItem(
                  "nextpage",
                  JSON.stringify(this.nextPage)
                );
                this.latestPosts.push(...data.results);
                sessionStorage.setItem(
                  "posts",
                  JSON.stringify(this.latestPosts)
                );
                $state.complete();
              } else {
                this.latestPosts.push(...data.results);
                sessionStorage.setItem(
                  "posts",
                  JSON.stringify(this.latestPosts)
                );
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
          // this.infiniteId++;
          // this.infinite = true;
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
