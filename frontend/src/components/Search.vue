<template>
  <div>
    <div class="uk-card uk-card-default uk-width-1-1@m" id="search_card">
      <form class="uk-grid-small" uk-grid>
        <div class="uk-width-1-5@s">
          <strong>タイトル</strong>
          <input
            v-model="filterQuery.title"
            @change="handleChangeQuery"
            class="uk-input"
            type="search"
            placeholder="キーワードを入力してください"
          />
          <!-- <div>{{ filterQuery.title }}</div> -->
        </div>
        <div class="uk-width-1-5@s">
          <strong>カテゴリ</strong>
          <select
            class="uk-select"
            type="text"
            v-model="filterQuery.category"
            @change="handleChangeQuery"
            placeholder
          >
            <option value>選択してください</option>
            <option v-for="(ctg,key) in categories" :key="key" v-bind:value="ctg.id">{{ctg.name}}</option>
          </select>
          <!-- <div>{{ filterQuery.category }}</div> -->
        </div>
        <div class="uk-width-1-5@s">
          <strong>投稿日</strong>
          <select
            class="uk-select"
            type="text"
            v-model="filterQuery.period"
            @change="handleChangeQuery"
            clearable
          >
            <option value>選択してください</option>
            <option v-for="(prd,key) in period" :key="key" v-bind:value="prd.date">{{prd.name}}</option>
          </select>
          <!-- <div>{{ filterQuery.period }}</div> -->
        </div>
        <div class="uk-width-1-5@s">
          <strong>都道府県</strong>
          <input class="uk-input" type="search" placeholder />
        </div>
        <div class="uk-width-1-5@s">
          <strong>市町村</strong>
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
                <a class="show_user" herf="#">
                  <div>
                    <img class="user_icon" v-bind:src="post.author.icon_image" />
                    <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                  </div>
                </a>
                <div class="timestamp">
                  <span>{{ post.published_at | moment }}</span>
                </div>
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

    <!-- <div>{{ filteredPosts }}</div> -->
  </div>
</template>

<script>
import moment from "moment";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      filterQuery: {
        title: "",
        category: "",
        period: ""
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
    ...mapGetters("post", ["filteredPosts"]),
    ...mapGetters("category", ["categories"])
  },
  mounted() {
    this.$store.commit("post/setFilterQuery", this.filterQuery);
  },
  methods: {
    handleChangeQuery() {
      this.$store.commit("post/setFilterQuery", this.filterQuery);
    }
  },
  filters: {
    moment: function(date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
    }
  }
};
</script>

<style scoped>
.router-link {
  text-decoration: none;
}

#search_card {
  margin-bottom: 20px;
  padding: 20px;
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

.timestamp {
  font-size: 12px;
  text-align: right;
}

.show_user {
  line-height: 45px;
  float: left;
  font-size: large;
  font-weight: bold;
  color: #333333;
}

.post_content {
  width: 100%;
  font-size: small;
  height: 40px;
}

p {
  margin: 0;
}

.comment_like_icon {
  text-align: right;
}

#comment-count {
  margin-right: 5px;
}

#like-count {
  line-height: 30px;
  font-size: 17px;
}

/* UIkitの上書き */
.uk-card-body {
  padding: 10px 20px;
}

.uk-comment-header {
  display: flow-root;
  margin-bottom: 0px;
}
</style>
