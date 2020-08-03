<template>
  <div>
      <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m" id="category_card">
        <div
          class="uk-grid-column-small uk-grid-row-small uk-child-width-1-5@s uk-text-center"
          uk-grid
        >
          <div v-for="category in categories" :key="category.id">
            <button
              class="uk-button uk-button-default uk-button-large uk-width-1-1"
              @click="selectedCategory(category)"
            >
              <span>{{category.name}}
              <span class="uk-badge">{{posts.filter(x => x.category === category.id).length}}</span>
              </span>
            </button>
          </div>
        </div>
      </div>

    <div
      class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
      uk-grid
    >
      <router-link
        class="router-link"
        :to="{name: 'detail', params:{id: post.id }}"
        v-for="post in categoryPosts"
        :key="post.id"
      >
        <div class="uk-card uk-card-hover uk-card-default" id="card">
          <div class="uk-card-media-top">
            <img v-bind:src="post.image_change" />
          </div>
          <div class="uk-card-body">
            <div class="uk-comment-header uk-position-relative">
              <div>
                <img class="user_icon" v-bind:src="post.author.icon_image" />
                <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
              </div>
            </div>
            <strong>{{ post.title }}</strong>
            <p class="post_content">
              <span>--</span>
              {{ post.content }}
            </p>
            <div class="comment_like_icon">
              <i id="heart-button" uk-icon="comment"></i>
              <span id="comment-count"></span>
              <i id="heart-button" uk-icon="heart"></i>
              <span id="like-count">{{ post.like_count}}</span>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>


<script>
import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      categories: [],
      selected: [],
    };
  },
  mounted() {
    api.get("http://127.0.0.1:8000/api/v1/categories/").then(response => {
      this.categories = response.data;
    });
  },
  methods: {
    selectedCategory(category) {
      this.selected = category;
    }
  },
  computed: {
    ...mapGetters("post",{
      'posts': "latestPosts"
    }),
    categoryPosts: function() {
      return this.posts.filter(x => x.category === this.selected.id);
    }
  }
};
</script>

<style scoped>

#category_card{
  margin-bottom: 20px;
}


span {
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
  background-color: #f7fcfc;
  margin-bottom: 20px;
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
    font-size: .875rem;
    font-weight: bold;
    display: inline-flex;
    justify-content: center;
    align-items: center;
}
.uk-button-large {
    padding: 0 20px;
    line-height: 53px;
    font-size: .875rem;
}
.uk-card-body {
    padding: 20px 20px;
}
</style>
