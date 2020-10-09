<template>
  <div>
    <div class="uk-card uk-card-default uk-width-1-1@s" id="search_card">
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
          <input type="text" style="display: none" />
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
            <option
              v-for="(ctg, key) in categories"
              :key="key"
              v-bind:value="ctg.id"
            >
              {{ ctg.name }}
            </option>
          </select>
        </div>
        <div class="uk-width-1-5@s">
          <strong>投稿日</strong>
          <select
            class="uk-select"
            type="text"
            v-model="query.period"
            @change="search"
            clearable
          >
            <option value>選択してください</option>
            <option
              v-for="(prd, key) in periods"
              :key="key"
              v-bind:value="prd.date"
            >
              {{ prd.name }}
            </option>
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
            <option v-for="item in prefs" :key="item.name">
              {{ item.name }}
            </option>
          </select>
        </div>
      </form>
    </div>
    <div>
      <div v-show="loading" class="loader">
        <span uk-spinner></span>
      </div>
      <div v-show="!loading">
        <PostList :postType="filterPosts" />
        <div v-if="filterPosts == ''">
          <p id="none_message">条件に一致する投稿がありません</p>
        </div>
        <div v-if="nextPage">
          <infinite-loading
            :identifier="infiniteId"
            spinner="spiral"
            @infinite="infiniteHandler"
          >
            <span id="no_results" slot="no-results"></span>
          </infinite-loading>
        </div>
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
import { watchScrollPosition, clearSession } from "@/mixins/utility";

export default {
  components: {
    PostList,
  },
  mixins: [prefs, periods, watchScrollPosition, clearSession],
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
      nextPage: false,
      infiniteId: 0,
      page: 1,
      postURL: "",
      sessionKey: "infinitePage_search",
    };
  },
  computed: {
    ...mapGetters("category", ["categories"]),
  },
  watch: {
    $route() {
      this.query.title = this.$route.query.title || "";
      this.query.category = this.$route.query.category || "";
      this.query.period = this.$route.query.published_at || "";
      this.query.prefecture = this.$route.query.prefecture || "";
      this.getPostURL();
      this.searchHandler();
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
    if (sessionStorage.getItem(this.sessionKey)) {
      this.getPostURL();
      const page_infinite = sessionStorage.getItem(this.sessionKey);
      for (let i = 1; i <= page_infinite; i++) {
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
            this.filterPosts.push(...data.results);
          });
      }
      this.loading = false;
    } else {
      this.clearSession();
      this.getPosts();
    }
  },
  methods: {
    async getPosts() {
      this.getPostURL();
      await api
        .get(this.postURL, {
          params: {
            page: this.page,
          },
        })
        .then((response) => {
          this.filterPosts = response.data.results;
          if (response.data.next !== null) {
            this.nextPage = true;
          }
        });
      this.loading = false;
    },

    resetHandler() {
      this.loading = true;
      this.filterPosts = [];
      this.page = 1;
      this.nextPage = false;
      this.infiniteId++;
      sessionStorage.removeItem(this.sessionKey);
    },

    getPostURL() {
      let postURL = process.env.VUE_APP_ROOT_API + "posts/";
      const params = this.$route.query;
      const queryString = Object.keys(params)
        .map((key) => key + "=" + params[key])
        .join("&");
      if (queryString) {
        this.postURL = postURL + "?" + queryString;
      } else {
        this.postURL = postURL;
      }
      console.log(postURL);
    },
    search() {
      this.resetHandler();
      // this.loading = true;
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
    searchHandler() {
      console.log("searchHandler");
      api
        .get(this.postURL, {
          params: {
            page: this.page,
          },
        })
        .then((response) => {
          this.filterPosts = response.data.results;
          this.loading = false;
          if (response.data.next !== null) {
            this.nextPage = true;
          }
        });
    },
    infiniteHandler($state) {
      console.log("infiniteHandler");
      console.log(this.page);
      this.page += 1;
      sessionStorage.setItem(this.sessionKey, this.page);

      api
        .get(this.postURL, {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            // this.loading = false;
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                this.filterPosts.push(...data.results);
                $state.complete();
              } else {
                this.filterPosts.push(...data.results);
                // this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
};
</script>

<style scoped>
@import "../assets/common.css";

#search_card {
  margin-bottom: 20px;
  padding: 20px;
  background-color: rgb(212, 217, 220);
  border-radius: 10px;
  border: 2px solid black;
  font-size: 18px;
}
</style>
