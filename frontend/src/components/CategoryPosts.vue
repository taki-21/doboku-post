<template>
  <div>
    <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m" id="category_card">
      <div
        class="uk-grid-column-small uk-grid-row-small uk-child-width-1-5@s uk-text-center"
        uk-grid
      >
        <!-- <div> -->
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

    <div
      class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
      uk-grid
    >
      <router-link
        class="router-link"
        v-for="post in posts"
        :key="post.id"
        :to="{name: 'detail', params:{id: post.id }}"
      >
        <!-- <transition appear> -->
        <div class="uk-card uk-card-hover uk-card-default" id="card">
          <div class="uk-card-media-top">
            <img v-bind:src="post.image_change" />
          </div>
          <div class="uk-card-body">
            <div class="uk-comment-header uk-position-relative">
              <div>
                <a class="show_user" herf="#">
                  <div>
                    <img class="user_icon" v-bind:src="post.author.icon_image" />
                    <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                  </div>
                </a>
                <div class="timestamp">
                  <span>{{ post.published_at | moment }}</span>
                </div>
              </div>
            </div>
            <strong>{{ post.title }}</strong>
            <p class="post_content">
              <span>--</span>
              {{ post.content }}
            </p>
            <div class="comment_like_icon">
              <i id="heart-button" uk-icon="comment"></i>
              <span id="comment-count">{{ post.comments_count}}</span>
              <i id="heart-button" uk-icon="heart"></i>
              <span id="like-count">{{ post.likes_count}}</span>
            </div>
          </div>
        </div>
        <!-- </transition> -->
      </router-link>
    </div>
  </div>
</template>


<script>
import { mapGetters } from "vuex";
import moment from "moment";

export default {
  data() {
    return {
      query: {
        category: this.$route.query.category || ""
      }
    };
  },
  watch: {
    $route() {
      this.getPosts();
      this.query.category = this.$route.query.category || "";
    }
  },

  methods: {
    // selectedCategory(category) {
    //   this.query.category = category.id;
    // },
    getPosts() {
      this.$store.dispatch("post/getFilterPosts", this.$route.query);
    },
    search() {
      this.$router.push({
        name: "category",
        query: {
          category: this.query.category
        }
      });
    }
  },
  computed: {
    ...mapGetters("post", {
      latestposts: "latestPosts"
    }),
    ...mapGetters("post", {
      posts: "filterPosts"
    }),
    ...mapGetters("category", {
      categories: "categories"
    })
    // categoryPosts: function() {
    //   return this.posts.filter(x => x.category === this.selected.id);
    // }
  },
  created() {
    this.getPosts();
    this.$store.dispatch("category/getAllCategories");
  },
  filters: {
    moment: function(date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
    }
  }
};
</script>

<style scoped>
#category_card {
  margin-bottom: 20px;
}
#category_name {
  font-size: 20px;
}
.router-link {
  text-decoration: none;
}

.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

#card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #eaeeee;
  margin-bottom: 20px;
}

input[type="radio"] {
  display: none; /* ラジオボタンを非表示にする */
}

.timestamp {
  font-size: 12px;
  text-align: right;
}

.show_user {
  line-height: 45px;
  float: left;
  font-size: large;
  font-weight: bold;
  color: #333333;
}

.post_content {
  width: 100%;
  font-size: small;
  height: 40px;
}

p {
  margin: 0;
}

.comment_like_icon {
  text-align: right;
}

#comment-count {
  margin-right: 5px;
}

#like-count {
  line-height: 30px;
  font-size: 17px;
}

/* UIkitの上書き */

.uk-comment-header {
  display: flow-root;
  margin-bottom: 0px;
}
.uk-badge {
  box-sizing: border-box;
  min-width: 15px;
  height: 15px;
  padding: 0 5px;
  margin-left: 5px;
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
  padding: 10px 20px;
}
</style>
