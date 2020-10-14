<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <GlobalMessage />
    <!-- メインエリア -->
    <div id="nav" style="z-index: 90;" uk-sticky="offset: 70; bottom: #top">
      <ul class="uk-flex-center" uk-tab>
        <router-link class="router-link" to="/">新着投稿</router-link>
        <router-link class="router-link" to="/popular">人気投稿</router-link>
        <router-link id="category" class="router-link" to="/category"
          >カテゴリ</router-link
        >
        <router-link id="map" class="router-link" to="/map">マップ</router-link>
        <router-link id="search" class="router-link" to="/search"
          >検索</router-link
        >
      </ul>
    </div>
    <div class="content">
      <!-- <div id="view_content"> -->
      <transition appear>
        <router-view />
      </transition>
      <!-- </div> -->
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
  mounted() {
    this.$store.dispatch("category/getAllCategories");
  },
};
</script>

<style scoped>
@import "../assets/common.css";
.router-link {
  color: rgba(90, 84, 75, 0.80);
}
.router-link-exact-active,
#map.router-link-active,
#search.router-link-active,
#category.router-link-active {
  border-bottom: solid 4px rgba(90, 84, 75, 0.85);
  color: rgb(90, 84, 75);
}

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
.content {
  margin: 0px auto 20px;
  max-width: 1200px;
  padding: 10px 30px;
}

@media (max-width: 640px) {
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
