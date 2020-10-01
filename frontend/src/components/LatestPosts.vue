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
      infinite: false,
      // infiniteId: 0,
    };
  },
  beforeRouteLeave(to, form, next) {
    // ストアのポストをクリア
    next();
  },
  watch: {
    loading: function () {
      this.$nextTick(() => {
        var positionY = sessionStorage.getItem("positionY");
        console.log(positionY);
        scrollTo(0, positionY);
        setTimeout(function () {
          scrollTo(0, positionY);
        });
      });
    },
    infinite() {
      // if (this.infiniteId >= 2) {
        var positionY = sessionStorage.getItem("positionY");
        console.log(positionY);
        // scrollTo(0, positionY);
        setTimeout(function () {
          scrollTo(0, positionY);
        },500);
      // }
    },
  },
  mounted() {
    api.get("/posts/").then((response) => {
      this.latestPosts = response.data.results;
      this.loading = false;
      if (response.data.next !== null) {
        this.nextPage = true;
      }
    });
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
                this.latestPosts.push(...data.results);
                $state.complete();
              } else {
                this.latestPosts.push(...data.results);
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
          // this.infiniteId++;
          this.infinite = true;
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
