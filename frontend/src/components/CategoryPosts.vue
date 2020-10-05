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
              id="category_label"
              class="uk-button uk-width-1-1"
              :for="category.id"
            >
              <span id="category_name">{{ category.name }}</span>
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
        <span uk-spinner></span>
      </div>
      <div v-show="!loading">
        <PostList :postType="filterPosts" />
        <div v-if="filterPosts == ''">
          <p id="none_message">まだ投稿がありません</p>
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
import api from "@/services/api";
import { mapGetters } from "vuex";
import { watchScrollPosition } from "@/mixins/utility";

export default {
  components: {
    PostList,
  },
  mixins: [watchScrollPosition],

  data() {
    return {
      postURL: "",
      page: 1,
      query: {
        category: this.$route.query.category || "",
      },
      filterPosts: [],
      loading: true,
      nextPage: false,
      infiniteId: 0,
      sessionKey: "infinitePage_category"
    };
  },
  watch: {
    $route() {
      this.query.category = this.$route.query.category || "";
      this.getPosts();
    },
  },
  async mounted() {
    if (sessionStorage.getItem(this.sessionKey)) {
      const page_infinite = sessionStorage.getItem(this.sessionKey);
      for (let i = 1; i <= page_infinite; i++) {
        await api
          .get("/posts/", {
            params: {
              page: i,
              category: this.query.category,
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
      this.getPosts();
    }
  },
  methods: {
    async getPosts() {
      await api
        .get("/posts/", {
          params: {
            page: this.page,
            category: this.query.category,
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
    search() {
      this.resetHandler();
      this.$router.push({
        name: "category",
        query: {
          category: this.query.category,
        },
      });
    },
    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem(this.sessionKey, this.page);

      api
        .get("/posts/", {
          params: {
            page: this.page,
            category: this.query.category,
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
  computed: {
    ...mapGetters("category", ["categories"]),
  },
};
</script>

<style scoped>
@import '../assets/common.css';

input[type="radio"] {
  display: none; /* ラジオボタンを非表示にする */
}

#category_choice input[type="radio"]:checked + label {
  font-weight: bold;
  color: rgb(0, 0, 0);
  background-color: rgb(228, 228, 228);
}

#category_card {
  margin-bottom: 20px;
  padding: 5px 5px;
  outline: none;
  /* border-radius:5px; */
  border: 2px solid rgb(0, 0, 0);
  background-color: rgb(236, 231, 225);
}
#category_card_contnet {
  padding: 5px 40px;
}

#previous_icon {
  margin-left: 0;
  padding-left: 10px;
}
#next_icon {
  margin-right: 0;
  padding-right: 10px;
}
/* UIkitの上書き */
.uk-button {
  padding: 0 20px;
  border-radius: 30px;
  background-color: rgb(255, 255, 255);
  border: 1px solid black;
  font-size: 20px;
  color: black;
}
</style>
