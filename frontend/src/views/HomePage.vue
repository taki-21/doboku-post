<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <GlobalMessage />
    <!-- メインエリア -->
    <router-link
      class="router-link"
      id="post"
      to="/newpostpage"
      v-if="isLoggedIn"
    >
      <div class="fixed_btn">+</div>
    </router-link>
    <v-bottom-navigation horizontal color="teal" grow>
      <v-btn to="/">
        <span>新着投稿</span>
        <v-icon>mdi-history</v-icon>
      </v-btn>
      <v-btn to="/popular">
        <span>人気投稿</span>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn to="/category">
        <span>カテゴリ</span>
        <v-icon>mdi-shape</v-icon>
      </v-btn>
      <v-btn to="/map">
        <span>マップ</span>
        <v-icon>mdi-map-marker</v-icon>
      </v-btn>
      <v-btn to="/search">
        <span>検索</span>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-bottom-navigation>
    <div class="content">
      <transition appear>
        <router-view />
      </transition>
    </div>
  </div>
</template>

<script>
import GlobalMessage from "@/components/GlobalMessage.vue";
import MyHeader from "@/components/MyHeader";

export default {
  components: {
    GlobalMessage,
    MyHeader,
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },
  mounted() {
    this.$store.dispatch("category/getAllCategories");
  },
};
</script>

<style scoped>
@import "../assets/common.css";
.v-bottom-navigation a {
  text-decoration: none;
}
.v-btn span {
  font-size: 16px;
}
.v-btn--active span{
  font-weight: bold;
}

.content {
  margin: 0px auto 20px;
  max-width: 1200px;
  padding: 10px 30px;
}
.fixed_btn {
  display: none;
}

/* UIkitの上書き */
.uk-tab {
  padding-top: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-wrap: wrap;
  margin-left: -20px;
  font-size: 22px;
  list-style: none;
  position: relative;
}

.uk-tab > * {
  float: left;
  padding: 0px 25px;
  position: relative;
}

@media (max-width: 640px) {
  .fixed_btn {
    display: block;
    text-decoration: none;
    background: rgb(116, 116, 116);
    color: #fff;
    width: 70px;
    height: 70px;
    line-height: 70px;
    border-radius: 50%;
    text-align: center;
    overflow: hidden;
    transition: 0.4s;
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-size: 30px;
    z-index: 100;
    box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.3);
  }
  .uk-tab {
    position: relative;
    top: -16px;
    padding-top: 9px;
    background-color: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-wrap: wrap;
    margin-left: -20px;
    list-style: none;
    position: relative;
    font-size: 14px;
    margin-bottom: 5px;
  }

  .uk-tab > * {
    float: left;
    padding: 0px 10px;
    position: relative;
  }
  .content {
    margin: 5px auto 10px;
    padding: 5px 15px;
  }
}
</style>
