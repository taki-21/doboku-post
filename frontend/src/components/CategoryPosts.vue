<template>
  <div>
    <div
      class="uk-card uk-card-default uk-card-body uk-width-1-1@m"
      tabindex="-1"
      uk-slider="finite: false"
      id="category_card"
    >
      <div class="uk-position-relative" id="category_card_contnet">
        <ul
          id="category_choice"
          class="uk-slider-items uk-grid uk-grid-column-small uk-child-width-1-4@s uk-child-width-1-6@m uk-text-center"
          uk-grid
        >
          <li v-for="category in categories" :key="category.id">
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
              <!-- <span class="uk-badge">{{latestposts.filter(x => x.category === category.id).length}}</span> -->
            </label>
          </li>
        </ul>
        <a
          id="previous_icon"
          class="uk-position-center-left uk-position-small uk-hidden-hover"
          href="#"
          uk-slidenav-previous
          uk-slider-item="previous"
        ></a>
        <a
          id="next_icon"
          class="uk-position-center-right uk-position-small uk-hidden-hover"
          href="#"
          uk-slidenav-next
          uk-slider-item="next"
        ></a>
      </div>
    </div>
    <div>
      <div v-show="loading" class="loader">
        <span uk-spinner="ratio: 1.5"></span>
      </div>
      <div v-show="!loading">
        <PostList :postType="filterPosts" />
      </div>
      <div v-if="loading"></div>
      <div v-else-if="filterPosts == ''">
        <p id="none_message">まだ投稿がありません</p>
      </div>
    </div>
  </div>
</template>


<script>
import PostList from "@/components/PostList";
import api from "@/services/api";
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
      filterPosts: [],
      // categories: [],
      loading: true,
    };
  },
  watch: {
    $route() {
      this.getPosts();
      this.query.category = this.$route.query.category || "";
    },
  },
  mounted() {
    this.getPosts();
    // api.get("/posts/").then((response) => {
    //   this.latestPosts = response.data;
    //   this.loading = false;
    // });
    // api.get("/categories/").then((response) => {
    //   this.categories = response.data;
    // });
  },
  methods: {
    getPosts() {
      let postURL = process.env.VUE_APP_ROOT_API + "posts/";
      const params = this.$route.query;
      const queryString = Object.keys(params)
        .map((key) => key + "=" + params[key])
        .join("&");
      if (queryString) {
        postURL += "?" + queryString;
      }
      console.log(postURL);
      api
        .get(postURL, {
          credentials: "include",
        })
        .then((response) => {
          this.filterPosts = response.data;
          this.loading = false;
        });
    },

    // this.$store.dispatch("post/getFilterPosts", this.$route.query);

    search() {
      this.loading = true;
      this.$router.push({
        name: "category",
        query: {
          category: this.query.category,
        },
      });
    },
  },

  computed: {
    // ...mapGetters("post", {
    //   latestposts: "latestPosts",
    // }),
    // ...mapGetters("post", {
    //   posts: "filterPosts",
    // }),
    ...mapGetters("category", {
      categories: "categories",
    }),
  },
  // created() {
  //   this.getPosts();
  //   this.$store.dispatch("category/getAllCategories");
  // },
};
</script>

<style scoped>
.loader {
  text-align: center;
  position: relative;
  top: 20px;
}
#category_card {
  margin-bottom: 20px;
  padding: 10px 5px;
  outline: none;
}
#category_card_contnet {
  padding: 5px 40px;
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
#none_message {
  font-size: 18px;
  text-align: center;
}
#previous_icon {
  margin-left: 0;
  padding-left: 10px;
}
#next_icon {
  margin-right: 0;
  padding-right: 10px;
}
</style>
