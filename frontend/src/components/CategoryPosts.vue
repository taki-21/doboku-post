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
              <span id="category_name">{{ category.name }}</span>
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
import InfiniteLoading from "vue-infinite-loading";
import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  components: {
    PostList,
    InfiniteLoading,
  },
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
    };
  },
  watch: {
    $route() {
      this.query.category = this.$route.query.category || "";
      this.getPosts();
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
    if (sessionStorage.getItem("infinitePage_category")) {
      const page_infinite = sessionStorage.getItem("infinitePage_category");
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
      sessionStorage.removeItem("infinitePage_category");

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
      sessionStorage.setItem("infinitePage_category", this.page);

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
                this.page += 1;
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
