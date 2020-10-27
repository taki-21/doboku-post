<template>
  <div>
    <router-link
      class="router-link"
      id="post"
      to="/newpostpage"
      v-if="isLoggedIn"
    >
      <div class="fixed_btn">+</div>
    </router-link>
    <!-- <v-app-bar fixed> -->
    <!-- <v-app-bar app> -->
      <v-tabs color="blue-grey lighten-2" centered show-arrows>
        <v-tab to="/">
          <v-icon left>mdi-history</v-icon>
          <span>新着投稿</span>
        </v-tab>
        <v-tab to="/popular">
          <v-icon left>mdi-heart</v-icon>
          <span>人気投稿</span>
        </v-tab>
        <v-tab to="/category">
          <v-icon left>mdi-shape</v-icon>
          <span>カテゴリ</span>
        </v-tab>
        <v-tab to="/map">
          <v-icon left>mdi-map-marker</v-icon>
          <span>マップ</span>
        </v-tab>
        <v-tab to="/search">
          <v-icon left>mdi-magnify</v-icon>
          <span>検索</span>
        </v-tab>
      </v-tabs>
    <!-- </v-app-bar> -->
    <!-- </v-app-bar> -->
    <div class="content">
      <transition appear>
        <router-view />
      </transition>
    </div>
  </div>
</template>

<script>
// import GlobalMessage from "@/components/GlobalMessage.vue";
// import MyHeader from "@/components/MyHeader";

export default {
  components: {
    // GlobalMessage,
    // MyHeader,
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
.v-tabs {
  border-bottom: 1px solid rgb(223, 211, 211);
}
.v-tabs a {
  text-decoration: none;
}
.v-tab span {
  font-size: 16px;
}

.content {
  margin: 10px auto 20px;
  max-width: 1200px;
  padding: 10px 30px;
}
.fixed_btn {
  display: none;
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
  .content {
    margin: 5px auto 10px;
    padding: 5px 15px;
  }
}
</style>
