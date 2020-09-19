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
        <!-- <pre>{{pieChartData}}</pre> -->
        <div class="uk-width-3-4">
          <div class="uk-card-body">
            <div id="username">
              <h1 class="uk-heading-medium">
                <strong class="uk-margin-remove">{{ Person.username }}</strong>
              </h1>
              <div id="piechart">
                <PieChart :data="pieChartData" :options="options"></PieChart>
              </div>
            </div>
            <div class="profile_content">
              <p>{{ Person.introduction }}</p>
            </div>
            <div v-if="user_id == user.id">
              <router-link class="router-link" to="/profile_edit">
                <div class="uk-button uk-button-default" id="profile_edit_button">プロフィール編集</div>
              </router-link>
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
            data: [1374, 9072, 715, 6148, 1200, 500, 2222],
            backgroundColor: [
              "rgba(255, 100, 130, 0.2)",
              "rgba(100, 130, 255, 0.2)",
              "rgba(130, 255, 100, 0.2)",
              "rgba(230, 210, 85, 0.2)",
              "rgba(220, 110, 85, 0.2)",
              "rgba(211, 110, 85, 0.2)",
              "rgba(167, 110, 85, 0.2)",
            ],
            // borderColor: "transparent",
          },
        ],
      },
      // グラフオプション
      options: {
        title: {
          display: false,
          // text: "藩と人口",
        },
        legend: {
          // 凡例に関する設定
          display: false, // 凡例を表示します。
          // position: "bottom", // 凡例の位置
        },
        tooltips: {
          // ツールチップに関する設定
          display: true, // キャンバス上でツールチップを有効にします
        },
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
  },
  watch: {
    $route() {
      api.get("/users/" + this.user_id + "/").then((response) => {
        this.Person = response.data;
      });
    },
  },
  methods: {
    // ログアウトリンク押下
    clickLogout: function () {
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました。",
      });
      this.$router.replace("/login");
    },
  },
  mounted() {
    api.get("/users/" + this.user_id + "/").then((response) => {
      this.Person = response.data;
      this.$store.dispatch("post/getAllPosts");
    });
    const labels = this.categories.map((x) => x.name)
    this.pieChartData.labels = labels
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
  position: absolute;
  bottom: 25px;
  right: 50px;
}

#piechart {
  position: absolute;
  width: 180px;
  height: 180px;
  right: 50px;
}
</style>
