<template>
  <div>
    <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m" id="category_card">
      <form class="uk-grid-small" uk-grid>
        <div class="uk-width-1-5@s">
          <label>タイトル</label>
          <input
            v-model="filterQuery.title"
            @change="handleChangeQuery"
            class="uk-input"
            type="search"
            placeholder
          />
          <div>{{ filterQuery.title }}</div>
        </div>
        <div class="uk-width-1-5@s">
          <label>カテゴリ</label>
          <select
            class="uk-select"
            type="text"
            v-model="filterQuery.category"
            @change="handleChangeQuery"
            placeholder
          >
            <option v-for="(ctg,key) in categories" :key="key" v-bind:value="ctg.id">{{ctg.name}}</option>
          </select>
          <div>{{ filterQuery.category }}</div>
        </div>
        <div class="uk-width-1-5@s">
          <label>投稿日</label>
          <select
            class="uk-select"
            type="text"
            v-model="filterQuery.category"
            @change="handleChangeQuery"
            placeholder
          >
            <option v-for="(prd,key) in period" :key="key" v-bind:value="prd.id">{{prd.name}}</option>
          </select>
        </div>
        <div class="uk-width-1-5@s">
          <label>都道府県</label>
          <input class="uk-input" type="search" placeholder />
        </div>
        <div class="uk-width-1-5@s">
          <label>市町村</label>
          <input class="uk-input" type="search" placeholder />
        </div>
      </form>
    </div>
    <div
      class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
      uk-grid
    >
      <router-link
        class="router-link"
        v-for="post in filteredPosts"
        :key="post.id"
        :to="{name: 'detail', params:{id: post.id }}"
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

    <div>{{ filteredPosts }}</div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";

export default {
  data() {
    return {
      categories: [],
      filterQuery: {
        title: "",
        category: ""
      },
      period: [
        {
          name: "3日前",
          date: 3
        },
        {
          name: "1週間前",
          date: 7
        },
        {
          name: "1ヶ月前",
          date: 30
        }
      ]
    };
  },
  computed: {
    ...mapGetters("post", ["filteredPosts"])
  },
  mounted() {
    this.$store.commit("post/setFilterQuery", this.filterQuery);
    api.get("http://127.0.0.1:8000/api/v1/categories/").then(response => {
      this.categories = response.data;
    });
  },
  methods: {
    handleChangeQuery() {
      this.$store.commit("post/setFilterQuery", this.filterQuery);
    }
  }
};
</script>

<style scoped>
.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}
</style>
