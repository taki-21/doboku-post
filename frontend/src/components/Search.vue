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
            <option v-for="(prd,key) in period" :key="key" v-bind:value="prd.date">{{prd.name}}</option>
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
      <PostList :postType="posts" />
  </div>
</template>

<script>
import PostList from "@/components/PostList";
import { mapGetters } from "vuex";
import prefs from "../mixins/PrefsMixin";
import moment from "moment";

export default {
  components: {
    PostList,
  },
  mixins: [prefs],
  data() {
    return {
      query: {
        title: this.$route.query.title || "",
        category: this.$route.query.category || "",
        period: this.$route.query.published_at || "",
        prefecture: this.$route.query.prefecture || "",
      },
      period: [
        {
          name: "3日前",
          date: moment().subtract(3, "days").format("YYYY-MM-DD"),
        },
        {
          name: "1週間前",
          date: moment().subtract(1, "weeks").format("YYYY-MM-DD"),
        },
        {
          name: "1ヶ月前",
          date: moment().subtract(1, "months").format("YYYY-MM-DD"),
        },
      ],
    };
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
  created() {
    this.getPosts();
  },
  computed: {
    ...mapGetters("category", ["categories"]),
    ...mapGetters("post", { posts: "filterPosts" }),
  },
  methods: {
    getPosts() {
      this.$store.dispatch("post/getFilterPosts", this.$route.query);
    },
    search() {
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
#search_card {
  margin-bottom: 20px;
  padding: 20px;
  background-color: rgb(212, 217, 220);
  border-radius: 10px;
  border: 2px solid black;
}
</style>
