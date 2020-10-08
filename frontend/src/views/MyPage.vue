<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div class="content_profilecard">
      <div
        id="profile_card"
        class="uk-card uk-card-default uk-grid-collapse uk-margin"
        uk-grid
      >
        <div class="uk-width-1-5@s uk-width-1-3">
          <div class="uk-card-media-left uk-cover-container">
            <img class="mypage_user_icon" :src="Person.icon_image" uk-cover />
            <canvas width="400" height="400"></canvas>
          </div>
        </div>
        <div class="uk-width-2-5@s uk-width-2-3">
          <!-- <div class="uk-card-body"> -->
          <div id="username_content">
            <!-- <h1 class="uk-heading-medium"> -->
            <div id="username">{{ Person.username }}</div>
            <!-- </h1> -->
            <div v-if="user_id == login_user_id"></div>
            <router-link class="router-link" to="/profile_edit">
              <div
                class="uk-button uk-button-small uk-button-default"
                id="profile_edit_button"
              >
                編集
              </div>
            </router-link>
          </div>
          <div id="profile_content">
            <div v-if="Person.introduction === null"></div>
            <div v-else>{{ Person.introduction }}</div>
          </div>
          <!-- </div> -->
        </div>
        <div class="uk-width-2-5@s uk-width-1-4">
          <div v-if="previousPosts[0]" class="uk-hidden-touch">
            <div id="piechart">
              <PieChart
                v-if="loaded"
                :data="pieChartData"
                :options="options"
              ></PieChart>
            </div>
          </div>
        </div>
      </div>
      <!-- <pre>{{user_id}}</pre> -->
      <div class="content">
        <ul class="uk-flex-center" id="nav" uk-tab>
          <router-link
            class="router-link"
            :to="{ name: 'mypage', params: { user_id: user_id } }"
            >これまでの投稿<span class="uk-badge">{{
              previousPostsNum
            }}</span></router-link
          >
          <router-link
            class="router-link"
            :to="{ name: 'liked', params: { user_id: user_id } }"
            >いいねした投稿<span class="uk-badge">{{
              likedPostsNum
            }}</span></router-link
          >
          <router-link
            class="router-link"
            :to="{ name: 'mymap', params: { user_id: user_id } }"
            >マイマップ</router-link
          >
        </ul>
        <div>
          <transition appear>
            <router-view @deletePost="get_previous_posts" />
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
      loaded: false,
      previousPostsNum: 0,
      likedPostsNum: 0,
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
        animation: { animateRotate: false },
      },
      Person: {},
      previousPosts: [],
    };
  },
  computed: {
    ...mapGetters("user", {
      login_user_id: "id",
    }),
    ...mapGetters("category", {
      categories: "categories",
    }),
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
      // this.getPosts();
      this.get_liked_posts();
    },

    user_id() {
      console.log("watch!!!!");
      this.setPerson();
      this.loaded = false;
      // this.options.animation.animateRotate = true;
      this.get_previous_posts();
      // this.options.animation.animateRotate = false;
    },
  },
  created() {
    console.log("created!!!!");
    this.get_previous_posts();
    this.get_liked_posts();
    // this.setPerson();
  },
  async mounted() {
    console.log("mounted!!!!");
    this.setPerson();
    const labels = this.categories.map((x) => x.name);
    this.options.animation.animateRotate = true;
    this.pieChartData.labels = labels;
    this.loaded = false;
    await api.get("/posts/?author=" + this.user_id).then((response) => {
      this.previousPosts = response.data.results;
      this.options.animation.animateRotate = true;
      this.set_category_data();
      this.options.animation.animateRotate = false;
    });
  },
  methods: {
    get_liked_posts() {
      console.log("get_liked_posts!!!!");
      api
        .get("/likes/", {
          params: {
            user: this.user_id,
          },
        })
        .then((response) => {
          this.likedPostsNum = response.data.results.length;
        });
    },
    get_previous_posts() {
      console.log("get_previous_posts!!!!");
      api.get("/posts/?author=" + this.user_id).then((response) => {
        this.previousPosts = response.data.results;
        this.previousPostsNum = response.data.results.length;
        this.set_category_data();
      });
    },
    set_category_data() {
      console.log("set_category_data!!!!");
      this.pieChartData.datasets[0].data = this.categoriesNum;
      this.loaded = true;
    },
    setPerson() {
      api.get("/users/" + this.user_id + "/").then((response) => {
        this.Person = response.data;
      });
    },
  },
};
</script>

<style scoped>
#username_content {
  display: flex;
  padding: 30px 30px 5px 30px;
}
#username {
  font-size: 40px;
  font-weight: bold;
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
  font-size: 20px;
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
  top: 15px;
  margin-left: 20px;
  /* bottom: 0px; */
  /* right: 50px; */
}
#profile_content {
  max-width: 300px;
  padding: 0px 0px 0px 30px;
  white-space: pre-wrap;
}

#piechart {
  position: absolute;
  width: 350px;
  height: 350px;
  right: 30px;
  top: -53px;
  /* bottom: -50px; */
}
.uk-badge {
  box-sizing: border-box;
  min-width: 25px;
  height: 25px;
  padding: 0 5px;
  margin-left: 10px;
  margin-bottom: 4px;
  border-radius: 500px;
  vertical-align: middle;
  background: rgba(90, 84, 75, 0.85);
  color: #fff;
  font-size: 0.875rem;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
@media (max-width: 640px) {
  #nav {
    font-size: 12px;
    margin-bottom: 10px;
  }
  .uk-tab > * {
    float: left;
    padding: 0px 10px;
    position: relative;
  }
  #username_content {
    display: flex;
    padding: 5px 10px 1px 10px;
  }
  #username {
    font-size: 22px;
    font-weight: bold;
  }

  #profile_edit_button {
    font-size: 10px;
    position: relative;
    top: 3px;
    margin-left: 10px;
  }
  .uk-button-small {
    padding: 0 4px;
    line-height: 15px;
    font-size: 0.875rem;
  }
  #profile_content {
    font-size: 10px;
    max-width: 300px;
    padding: 0px 0px 0px 10px;
    white-space: pre-wrap;
  }
  .uk-badge {
    box-sizing: border-box;
    min-width: 15px;
    height: 15px;
    padding: 0 5px;
    margin-left: 10px;
    margin-bottom: 2px;
    border-radius: 50%;
    vertical-align: middle;
    background: rgba(90, 84, 75, 0.85);
    color: #fff;
    font-size: 0.7rem;
    display: inline-flex;
    justify-content: center;
    align-items: center;
  }
}
@media (max-width: 1200px) {
  #piechart {
    position: absolute;
    width: 300px;
    height: 300px;
    right: 20px;
    top: -50px;
  }
}
</style>
