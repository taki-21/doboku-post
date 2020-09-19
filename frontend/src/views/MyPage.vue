<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div class="content_profilecard">
      <div id="profile_card" class="uk-card uk-card-default uk-grid-collapse uk-margin" uk-grid>
        <div class="uk-width-1-4">
          <div class="uk-card-media-left uk-cover-container">
            <img class="mypage_user_icon" :src="Person.icon_image" uk-cover />
            <canvas width="500" height="500"></canvas>
          </div>
        </div>
        <div class="uk-width-3-4">
          <div class="uk-card-body">
            <div id="username">
              <h1 class="uk-heading-medium">
                <strong class="uk-margin-remove">{{ Person.username }}</strong>
              </h1>
              <div v-if="user_id == user.id">
                <router-link class="router-link" to="/profile_edit">
                  <div
                    class="uk-button uk-button-small uk-button-default"
                    id="profile_edit_button"
                  >編集</div>
                </router-link>
              </div>
              <div id="piechart">
                <PieChart :data="pieChartData" :options="options"></PieChart>
              </div>
            </div>
            <div class="profile_content">
              <p>{{ Person.introduction }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <ul class="uk-flex-center" id="nav" uk-tab>
          <router-link
            class="router-link"
            :to="{name: 'mypage', params: {user_id: user_id}}"
          >これまでの投稿</router-link>
          <router-link class="router-link" :to="{name: 'liked', params: {user_id: user_id}}">いいねした投稿</router-link>
          <router-link class="router-link" :to="{name: 'mymap', params: {user_id: user_id}}">マイマップ</router-link>
        </ul>
        <div>
          <transition appear>
            <router-view />
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import MyHeader from "@/components/MyHeader";
import PieChart from "@/components/PieChart";
import * as palette from "google-palette";
import api from "@/services/api";

export default {
  components: {
    MyHeader,
    PieChart,
  },
  props: ["user_id"],
  data() {
    return {
      // グラフ描画用データ
      pieChartData: {
        // ラベル
        labels: [],
        // データ詳細
        datasets: [
          {
            // label: "藩と人口",
            data: [],
            backgroundColor: palette("mpn65", 30).map(function (hex) {
              return "#" + hex + 30;
            }),
            borderColor: "transparent",
          },
        ],
      },
      // グラフオプション
      options: {
        legend: {
          // 凡例に関する設定
          display: true, // 凡例を表示します。
          position: "right", // 凡例の位置
        },
        animation: false,
      },
      Person: {},
    };
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser",
    }),
    ...mapGetters("category", {
      categories: "categories",
    }),
    ...mapGetters("post", {
      posts: "latestPosts",
    }),
    previousPosts() {
      return this.posts.filter((x) => x.author.id == this.user_id);
    },
    myCategories() {
      return this.previousPosts.map((x) => x.category);
    },
    categoriesNum() {
      var categories_num = [];
      for (var i = 1; i < this.categories.length + 1; i++) {
        categories_num.push(this.myCategories.filter((num) => num == i).length);
      }
      return categories_num;
    },
  },
  watch: {
    $route() {
      api.get("/users/" + this.user_id + "/").then((response) => {
        this.Person = response.data;
      });
      this.set_category_data();
    },
  },
  methods: {
    set_category_data() {
      this.pieChartData.datasets[0].data = this.categoriesNum;
    },
  },
  mounted() {
    this.$store.dispatch("category/getAllCategories");
    api.get("/users/" + this.user_id + "/").then((response) => {
      this.Person = response.data;
      this.$store.dispatch("post/getAllPosts");
    });
  },
  created() {
    const labels = this.categories.map((x) => x.name);
    this.pieChartData.labels = labels;
    this.set_category_data();
  },
};
</script>

<style scoped>
#username {
  display: flex;
}
.router-link {
  text-decoration: none;
  color: black;
  font-size: 20px;
}

.router-link-exact-active {
  border-bottom: solid 3px rgba(90, 84, 75, 0.85);
}
.uk-tab > * {
  flex: none;
  padding: 0px 20px;
  position: relative;
}

.content_profilecard {
  margin: 20px auto;
  max-width: 1200px;
  padding: 0px 30px;
}
.content {
  margin: 20px auto;
  max-width: 1200px;
  /* padding: 0px 30px; */
}

#profile_card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #f3f5f5;
  /* margin-top: 20px; */
  margin-bottom: 30px;
}
.uk-tab > .uk-active > a {
  color: #333;
  border-color: rgba(90, 84, 75, 0.85);
}

.uk-tab > * > a {
  display: block;
  text-align: center;
  padding: 5px 10px;
  color: #999;
  border-bottom: 3px solid transparent;
  /* font-size: .875rem; */
  text-transform: uppercase;
  transition: color 0.1s ease-in-out;
  font-size: 120%;
}

#profile_edit_button {
  position: relative;
  top: 30px;
  margin-left: 20px;
  /* bottom: 0px; */
  /* right: 50px; */
}

#piechart {
  position: absolute;
  width: 350px;
  height: 350px;
  right: 25px;
  top: -20px;
  /* bottom: -50px; */
}
</style>
