<template>
  <div>
    <div class="uk-card uk-card-default uk-width-1-1@m" id="search_card">
      <form class="uk-grid-small" uk-grid>
        <div class="uk-width-2-5@s">
          <strong>タイトル</strong>
          <input
            v-model="query.title"
            @change="search"
            class="uk-input"
            type="search"
            placeholder="キーワードを入力してください"
          />
          <input type="text" style="display: none;" />
        </div>
        <div class="uk-width-1-5@s">
          <strong>カテゴリ</strong>
          <select
            class="uk-select"
            type="text"
            v-model="query.category"
            @change="search"
            placeholder
          >
            <option value>選択してください</option>
            <option v-for="(ctg,key) in categories" :key="key" v-bind:value="ctg.id">{{ctg.name}}</option>
          </select>
        </div>
        <div class="uk-width-1-5@s">
          <strong>投稿日</strong>
          <select class="uk-select" type="text" v-model="query.period" @change="search" clearable>
            <option value>選択してください</option>
            <option v-for="(prd,key) in periods" :key="key" v-bind:value="prd.date">{{prd.name}}</option>
          </select>
        </div>
        <div class="uk-width-1-5@s">
          <strong>都道府県</strong>
          <select
            class="uk-select"
            type="text"
            v-model="query.prefecture"
            @change="search"
            clearable
          >
            <option value>選択してください</option>
            <option v-for="item in prefs" :key="item.name">{{item.name}}</option>
          </select>
        </div>
      </form>
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
        <p id="none_message">条件に一致する投稿がありません</p>
      </div>
    </div>
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import { mapGetters } from "vuex";
import api from "@/services/api";
import prefs from "../mixins/PrefsMixin";
import periods from "../mixins/PeriodsMixin";

export default {
  components: {
    PostList,
  },
  mixins: [prefs, periods],
  data() {
    return {
      filterPosts: [],
      query: {
        title: this.$route.query.title || "",
        category: this.$route.query.category || "",
        period: this.$route.query.published_at || "",
        prefecture: this.$route.query.prefecture || "",
      },
      loading: true,
    };
  },
  computed: {
    ...mapGetters("category", ["categories"]),
  },
  watch: {
    $route() {
      this.getPosts();
      this.query.title = this.$route.query.title || "";
      this.query.category = this.$route.query.category || "";
      this.query.period = this.$route.query.published_at || "";
      this.query.prefecture = this.$route.query.prefecture || "";
    },
  },
  mounted() {
    this.getPosts();
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
    search() {
      this.loading = true;
      this.$router.push({
        name: "search",
        query: {
          title: this.query.title,
          category: this.query.category,
          published_at: this.query.period,
          prefecture: this.query.prefecture,
        },
      });
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

#search_card {
  margin-bottom: 20px;
  padding: 20px;
  background-color: rgb(212, 217, 220);
  border-radius: 10px;
  border: 2px solid black;
}
#none_message {
  font-size: 18px;
  text-align: center;
}
</style>
