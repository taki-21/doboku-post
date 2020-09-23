<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="latestPosts" />
      <infinite-loading spinner="spiral" @infinite="infiniteHandler"></infinite-loading>
    </div>
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import api from "@/services/api";

export default {
  components: {
    PostList,
  },
  data() {
    return {
      page: 1,
      latestPosts: [],
      loading: false,
    };
  },
  methods: {
    infiniteHandler($state) {
      //web.phpで設定したルーティング
      api
        .get("/posts/", {
          params: {
            page: this.page,
            // per_page: 1,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
          if(data.results.length === 12){
            console.log('おおおお')
            this.latestPosts.push(...data.results);
            this.page += 1;
            $state.loaded();

            console.log('たたたた')
          }
          if (data.results.length < 12) {
            console.log("へいへい");
            this.latestPosts.push(...data.results);
            // this.page += 1;
            $state.complete();
            // $state.loaded();
          }}, 500)
          // else {
          // }
        })
        .catch(() => {
          $state.complete();
        });
    },
  },
  mounted() {
    // this.infiniteHandler()
    // api.get("/posts/").then((response) => {
    //   this.latestPosts = response.data.results;
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
</style>
