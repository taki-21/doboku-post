<template>
  <div>
    <v-form>
      <v-container>
        <v-row>
          <v-col cols="12" xs="6" sm="6" md="3">
            <v-text-field
              v-model="query.title"
              @change="search"
              clearable
              label="タイトル"
              placeholder="キーワードを入力してください"
            ></v-text-field>
          </v-col>
          <v-col cols="12" xs="6" sm="6" md="3">
            <v-select
              :items="categories"
              item-text="name"
              item-value="id"
              v-model="query.category"
              @change="search"
              clearable
              label="カテゴリ"
              placeholder="選択してください"
            ></v-select>
          </v-col>
          <v-col cols="12" xs="6" sm="6" md="3">
            <v-select
              :items="periods"
              item-text="name"
              item-value="date"
              v-model="query.period"
              @change="search"
              clearable
              label="投稿日"
              placeholder="選択してください"
            ></v-select>
          </v-col>
          <v-col cols="12" xs="6" sm="6" md="3">
            <v-select
              :items="prefs"
              item-text="name"
              item-value="name"
              v-model="query.prefecture"
              @change="search"
              clearable
              label="都道府県"
              placeholder="選択してください"
            ></v-select>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
    <div>
      <div v-show="isLoading" class="text-center">
        <v-progress-circular
          indeterminate
          color="blue-gray"
        ></v-progress-circular>
      </div>
      <div v-show="!isLoading">
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
        category: Number(this.$route.query.category) || "",
        period: this.$route.query.published_at || "",
        prefecture: this.$route.query.prefecture || "",
      },
      isLoading: true,
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
    isLoading() {
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
      this.isLoading = false;
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
      this.isLoading = false;
    },

    resetHandler() {
      this.isLoading = true;
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
      this.$router.push({
        name: "search",
        query: {
          title: this.query.title || "",
          category: this.query.category || "",
          published_at: this.query.period || "",
          prefecture: this.query.prefecture || "",
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
          this.isLoading = false;
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
            if (data.results.length) {
              if (data.next === null) {
                this.nextPage = false;
                this.filterPosts.push(...data.results);
                $state.complete();
              } else {
                this.filterPosts.push(...data.results);
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
</style>
