<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="likedPosts" />
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
import moment from "moment";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },

  data() {
    return {
      page: 1,
      loading: true,
      nextPage: false,
      likedPosts: [],
    };
  },
  methods: {
    infiniteHandler($state) {
      this.page += 1;
      api
        .get("/posts/", {
          params: {
            page: this.page,
            user: this.user_id,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            // this.loading = false;
            if (data.results.length) {
              if (data.next === null) {
                this.likedPosts.push(
                  ...data.results.map((like) => like.post)
                );
                $state.complete();
              } else {
                this.likedPosts.push(
                  ...data.results.map((like) => like.post)
                );
                this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
  mounted() {
    api
      .get("/likes/", {
        params: {
          user: this.user_id,
        },
      })
      .then((response) => {
        this.likedPosts = response.data.results.map((like) => like.post);
        this.loading = false;
        if (response.data.next !== null) {
          this.nextPage = true;
        }
      });
  },
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
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
