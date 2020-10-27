<template>
  <div>
    <div
      class="uk-card uk-card-default uk-card-body uk-width-1-1@m"
      tabindex="-1"
      uk-slider="finite: false"
      id="category_card"
    >
      <div class="uk-position-relative" id="category_card_content">
        <ul
          id="category_choice"
          class="uk-slider-items uk-grid uk-grid-column-small uk-child-width-1-2 uk-child-width-1-4@s uk-child-width-1-6@m uk-text-center"
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
            <label id="category_label" class="uk-width-1-1" :for="category.id">
              <span>{{ category.name }}</span>
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
      <div v-show="isLoading" class="loader">
        <span uk-spinner></span>
      </div>
      <div v-show="!isLoading">
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
import { clearSession } from "@/mixins/utility";

export default {
  components: {
    PostList,
  },
  mixins: [watchScrollPosition, clearSession],

  data() {
    return {
      postURL: "",
      page: 1,
      query: {
        category: this.$route.query.category || "",
      },
      filterPosts: [],
      isLoading: true,
      nextPage: false,
      infiniteId: 0,
      sessionKey: "infinitePage_category",
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
      this.isLoading = false;
    } else {
      this.clearSession();
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
      this.isLoading= false;
    },

    resetHandler() {
      this.isLoading = true;
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
  computed: {
    ...mapGetters("category", ["categories"]),
  },
};
</script>

<style scoped>
@import "../assets/common.css";

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
  /* border: 2px solid rgb(0, 0, 0); */
  background-color: rgb(145, 163, 174, 0.1);
}
#category_card_content {
  padding: 5px 40px;
}
#category_label {
  font-size: 20px;
  display: inline-block;
  padding: 0.3em 1em;
  border-radius: 10px;
  text-decoration: none;
  background: #f7f7f7;
  color: #000000; /*文字色*/
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.29);
}
#category_label:hover{
  cursor: pointer;
}
#previous_icon {
  margin-left: 0;
  padding-left: 10px;
  color: #000000;
}
#next_icon {
  margin-right: 0;
  padding-right: 10px;
  color: #000000;
}

@media (max-width: 640px) {
  #category_card {
    margin-bottom: 10px;
    padding: 2px 5px 3px 5px;
    outline: none;
    border: 1px solid rgb(0, 0, 0);
    /* background-color: rgb(236, 231, 225); */
  }

  #category_label {
    font-size: 15px;
    height: 22px;
    line-height: 22px;
    padding: 0.1em 1em;
    margin-top: 0.1em;
    text-decoration: none;
    box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.29);
  }
  #category_card_content {
    padding: 0px 40px;
  }
}
</style>
