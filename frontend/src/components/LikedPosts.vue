<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner="ratio: 1.5"></span>
    </div>
    <div v-show="!loading">
      <PostList :postType="likedPosts" />
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
      likedPosts: [],
      loading: true,
    };
  },
  computed: {},
  mounted() {
    api
      .get("/likes/", {
        params: {
          user: this.user_id,
        },
      })
      .then((response) => {
        this.likedPosts = response.data.map((like) => like.post);
        this.loading = false;
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
