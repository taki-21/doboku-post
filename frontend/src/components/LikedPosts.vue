<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
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
// import moment from "moment";

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
    if (sessionStorage.getItem("infinitePage_liked")) {
      const page_infinite = sessionStorage.getItem("infinitePage_liked");
      for (let i = 1; i <= page_infinite; i++) {
        await api
          .get("/likes/", {
            params: {
              page: i,
              user: this.user_id,
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
      this.loading = false;
    } else {
      this.getPosts();
    }

    // api
    //   .get("/likes/", {
    //     params: {
    //       user: this.user_id,
    //     },
    //   })
    //   .then((response) => {
    //     this.likedPosts = response.data.results.map((like) => like.post);
    //     this.loading = false;
    //     if (response.data.next !== null) {
    //       this.nextPage = true;
    //     }
    //   });
  },
  methods: {
    async getPosts() {
      await api
        .get("/likes/", {
          params: {
            user: this.user_id,
          },
        })
        .then((response) => {
          this.likedPosts = response.data.results.map((like) => like.post);
          if (response.data.next !== null) {
            this.nextPage = true;
          }
        });
      this.loading = false;
    },

    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem("infinitePage_liked", this.page);
      api
        .get("/likes/", {
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
                this.nextPage = false;
                this.likedPosts.push(...data.results.map((like) => like.post));
                $state.complete();
              } else {
                this.likedPosts.push(...data.results.map((like) => like.post));
                // this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
  // filters: {
  //   moment: function (date) {
  //     return moment(date).format("YYYY/MM/DD HH:MM");
  //   },
  // },
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
