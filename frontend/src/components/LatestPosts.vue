<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <!-- <div v-if="display"> -->
    <div v-show="!loading">
      <PostList :postType="latestPosts" />
      <infinite-loading spinner="spiral" @infinite="infiniteHandler">
        <span id="no_results" slot="no-results">投稿は以上です</span>
      </infinite-loading>
    </div>

    <!-- </div> -->
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
      // display:false,
      page: 1,
      latestPosts: [],
      loading: true,
    };
  },
  // watch: {

  // },
  // computed: {
  //   display() {
  //     return true;
  //   },
  // },
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
              this.latestPosts.push(...data.results);
              if ($state) {
                $state.loaded();
              }
            } else {
              $state.complete();
            }
            if (data.results.length < 12) {
              this.latestPosts.push(...data.results);
              $state.complete();
            }
          }, 500);
        })
        .catch(() => {
          console.log("おおお");
          $state.complete();
        });
    },
  },
  created() {
    this.infiniteHandler();

    // this.$nextTick(function () {
    //   this.loading = false;
    // });
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
