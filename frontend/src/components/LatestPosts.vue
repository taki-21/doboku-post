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
    };
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
          if(data.results.length === 12){
            this.latestPosts.push(...data.results);
            this.page += 1;
            $state.loaded();
          }
          if (data.results.length < 12) {
            console.log("へいへい");
            this.latestPosts.push(...data.results);
            $state.complete();
          }}, 500)
        })
        .catch(() => {
          $state.complete();
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
</style>
