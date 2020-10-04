<template>
  <div>
    <PostList
      :postType="previousPosts"
      :user_id="auth_id"
      @parentPostDelete="parentPostDelete"
      :loading="loading"
      :nextPage="nextPage"
      :postURL="postURL"
      :sessionKey="sessionKey"
    />
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import api from "@/services/api";

export default {
  props: ["user_id"],
  components: {
    PostList,
  },
  data() {
    return {
      auth_id: this.$store.getters["auth/id"],
      page: 1,
      loading: true,
      nextPage: false,
      previousPosts: [],
      sessionKey: "infinitePage_previous",
    };
  },
  computed: {
    postURL() {
      var params = "?author=" + this.auth_id
      return "/posts/" + params;
    },
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
          .get(this.postURL, {
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
