<template>
  <div>
    <MyHeader />
    <!-- ヘッダー -->
    <div class="mypage">
      <!-- <pre>{{user}}</pre> -->
      <div id="profile_card" class="uk-card uk-card-default uk-grid-collapse uk-margin" uk-grid>
        <div class="uk-width-1-4">
          <div class="uk-card-media-left uk-cover-container">
            <img class="mypage_user_icon" :src="'http://127.0.0.1:8000' + user.icon_image" uk-cover />
            <canvas width="500" height="500"></canvas>
          </div>
        </div>
        <div class="uk-width-3-4">
          <div class="uk-card-body">
            <h1 class="uk-heading-medium">
              <strong class="uk-margin-remove">{{ user.username }}</strong>
            </h1>
            <div class="profile_content">
              <p>{{ user.introduction }}</p>
            </div>
            <div class="profile_edit_button" uk-margin>
              <div class="uk-button uk-button-default">プロフィール編集</div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <ul class="uk-flex-center" uk-tab>
          <li>
            <a class="uk-text-large uk-text-secondary">これまでの投稿</a>
          </li>
          <li>
            <a class="uk-text-large uk-text-secondary">いいねした投稿</a>
          </li>
          <li>
            <a class="uk-text-large uk-text-secondary">カテゴリ</a>
          </li>
          <li>
            <a class="uk-text-large uk-text-secondary">マイマップ</a>
          </li>
          <li>
            <a class="uk-text-large uk-text-secondary">検索</a>
          </li>
        </ul>
        <ul class="uk-switcher uk-margin">
          <li>
            <PreviousPosts/>
          </li>

        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import MyHeader from "@/components/MyHeader";
import PreviousPosts from "@/components/PreviousPosts";
export default {
  data() {
    return {
      user: "",
      id: this.$store.getters["auth/id"]
    };
  },
  components:{
    MyHeader,
    PreviousPosts
  },
  computed: {
    username: function() {
      return this.$store.getters["auth/username"];
    },
    isLoggedIn: function() {
      return this.$store.getters["auth/isLoggedIn"];
    }
    // id: function() {
    //   return this.$store.getters["auth/id"];
    // }
  },
  mounted() {
    this.axios
      .get("http://127.0.0.1:8000/api/v1/users/" + this.id + "/")
      .then(response => {
        this.user = response.data;
      });
  },
  methods: {
    // ログアウトリンク押下
    clickLogout: function() {
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました。"
      });
      this.$router.replace("/login");
    }
  }
};
</script>

<style scoped>
.mypage {
  margin: 10px 5%;
}
#profile_card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #f3f5f5;
  margin-top: 20px;
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
</style>
