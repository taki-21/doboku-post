<template>
  <div>
    <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m" id="category_card">
      <div
        id="category_choice"
        class="uk-grid-column-small uk-grid-row-small uk-child-width-1-4@s uk-child-width-1-6@m  uk-text-center"
        uk-grid
      >
        <div v-for="category in categories" :key="category.id">
          <input
            type="radio"
            :id="category.id"
            v-model="query.category"
            :value="category.id"
            @change="search"
          />
          <label
            class="uk-button uk-button-default uk-button-large uk-width-1-1"
            :for="category.id"
          >
            <span id="category_name">{{category.name}}</span>
            <span class="uk-badge">{{latestposts.filter(x => x.category === category.id).length}}</span>
          </label>
        </div>
      </div>
    </div>
    <div>
      <PostList :postType="posts" />
      <div v-if="posts == ''">
        <p>まだ投稿がありません</p>
      </div>
    </div>
  </div>
</template>


<script>
import PostList from "@/components/PostList";

import { mapGetters } from "vuex";

export default {
  components: {
    PostList,
  },

  data() {
    return {
      query: {
        category: this.$route.query.category || "",
      },
    };
  },
  watch: {
    $route() {
      this.getPosts();
      this.query.category = this.$route.query.category || "";
    },
  },

  methods: {
    getPosts() {
      this.$store.dispatch("post/getFilterPosts", this.$route.query);
    },
    search() {
      this.$router.push({
        name: "category",
        query: {
          category: this.query.category,
        },
      });
    },
  },
  computed: {
    ...mapGetters("post", {
      latestposts: "latestPosts",
    }),
    ...mapGetters("post", {
      posts: "filterPosts",
    }),
    ...mapGetters("category", {
      categories: "categories",
    }),
  },
  created() {
    this.getPosts();
    this.$store.dispatch("category/getAllCategories");
  },
};
</script>

<style scoped>
#category_card {
  margin-bottom: 20px;
}
#category_name {
  font-size: 20px;
}

input[type="radio"] {
  display: none; /* ラジオボタンを非表示にする */
}

#category_choice input[type="radio"]:checked + label {
  color: black;
  font-weight: bold;
  background-color: rgb(206, 204, 203);
  border: 1px solid black;
}

/* UIkitの上書き */

.uk-comment-header {
  display: flow-root;
  margin-bottom: 0px;
}
.uk-badge {
  position: relative;
  left: 15px;
  box-sizing: border-box;
  min-width: 15px;
  height: 15px;
  padding: 0 5px;
  /* margin-left: 15px; */
  border-radius: 500px;
  vertical-align: middle;
  background: black;
  color: #fff;
  font-size: 0.875rem;
  font-weight: bold;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
.uk-button-large {
  padding: 0 20px;
  line-height: 53px;
  font-size: 0.875rem;
}
.uk-card-body {
  padding: 20px 20px;
}
</style>
