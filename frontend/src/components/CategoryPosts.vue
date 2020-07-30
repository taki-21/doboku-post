<template>
  <div>
    <pre>{{selected}}</pre>
    <div v-if="selected == false">
      <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m">
        <div
          class="uk-grid-column-small uk-grid-row-small uk-child-width-1-2@s uk-text-center"
          uk-grid
        >
          <div v-for="category in categories" :key="category.id">
            <button
              class="uk-button uk-button-default uk-button-large uk-width-1-1"
              @click="selectedCategory(category)"
              key="input"
            >
              <span>{{category.name}}</span>
            </button>
          </div>
          <!-- <span>Selected: {{ selected }}</span> -->
        </div>
      </div>
    </div>
    <button
      class="uk-button uk-button-default"
      type="button"
      id="selected_category"
      uk-toggle="target: #modal-center"
    >{{ selected.name }}</button>

    <div id="modal-center" class="uk-flex-top" uk-modal>
      <div class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
        <div
          class="uk-grid-column-small uk-grid-row-small uk-child-width-1-2@s uk-text-center"
          uk-grid
        >
          <div v-for="category in categories" :key="category.id">
            <button
              class="uk-button uk-button-default uk-button-large uk-width-1-1 uk-modal-close"
              @click="selectedCategory(category)"
            >
              <span>{{category.name}}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- <pre>Selected: {{ selected }}</pre> -->

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

export default {
  data() {
    return {
      categories: [],
      selected: [],
      posts: []
    };
  },
  mounted() {
    api.get("http://127.0.0.1:8000/api/v1/categories/").then(response => {
      this.categories = response.data;
    });
    api.get("http://127.0.0.1:8000/api/v1/posts/").then(response => {
      this.posts = response.data;
    });
  },
  methods: {
    selectedCategory(category) {
      console.log("代入前" + this.selected);
      this.selected = category;
      // this.$set(this.selected, 'id',  category.id);
      // this.$set(this.selected, 'name', category.name);
      console.log("代入後" + this.selected);
    }
  },
  computed: {
    categoryPosts: function() {
      return this.posts.filter(x => x.category === this.selected.id);
    }
  }
};
</script>

<style scoped>
#selected_category {
  font-size: 32px;
  color: black;
  padding: 5px 35px;
  margin-bottom: 20px;
}

a#selected_category :hover {
  background-color: red;
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

.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: #fff;
  opacity: 0;
  transform: translateY(-100px);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
</style>
