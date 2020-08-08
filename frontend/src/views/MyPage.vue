<template>
  <div>
    <MyHeader />
    <!-- ヘッダー -->
    <div class="content">
      <!-- <pre>{{person}}</pre> -->
      <div id="profile_card" class="uk-card uk-card-default uk-grid-collapse uk-margin" uk-grid>
        <div class="uk-width-1-4">
          <div class="uk-card-media-left uk-cover-container">
            <img class="mypage_user_icon" :src="Person.icon_image" uk-cover />
            <canvas width="500" height="500"></canvas>
          </div>
        </div>
        <div class="uk-width-3-4">
          <div class="uk-card-body">
            <h1 class="uk-heading-medium">
              <strong class="uk-margin-remove">{{ Person.username }}</strong>
            </h1>
            <div class="profile_content">
              <p>{{ Person.introduction }}</p>
            </div>
            <router-link class="router-link" to="/profile_edit">
              <div class="uk-button uk-button-default" id="profile_edit_button">プロフィール編集</div>
            </router-link>
          </div>
        </div>
      </div>
      <div class="content">
        <ul class="uk-flex-center" id="nav" uk-tab>
          <router-link class="router-link" :to="{name: 'mypage', params: {user_id: user_id}}">これまでの投稿</router-link>
          <router-link class="router-link" :to="{name: 'liked', params: {user_id: user_id}}">いいねした投稿</router-link>
          <router-link class="router-link" to="/category">マイマップ</router-link>
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
import api from "@/services/api";

export default {
  components: {
    MyHeader
  },
  props: ["user_id"],
  data() {
    return {
      Person: {},
    };
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser"
    })
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
  },
  mounted() {
    api.get("/users/" + this.user_id + '/').then(response => {
      this.Person = response.data
    })
  }
};
</script>

<style scoped>
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

.content {
  margin: 10px auto;
  max-width: 1040px;
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

#profile_edit_button {
  position: absolute;
  bottom: 50px;
  right: 50px;
}
</style>
