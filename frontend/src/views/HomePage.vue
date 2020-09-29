<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <GlobalMessage />
    <!-- メインエリア -->

    <div class="content">
      <ul class="uk-flex-center" id="nav" uk-tab>
        <router-link class="router-link" to="/">新着投稿</router-link>
        <router-link class="router-link" to="/popular">人気投稿</router-link>
        <router-link id="category" class="router-link" to="/category">カテゴリ</router-link>
        <router-link id="map" class="router-link" to="/map">マップ</router-link>
        <router-link id="search" class="router-link" to="/search">検索</router-link>
      </ul>
      <div>
        <transition appear>
          <router-view />
        </transition>
      </div>
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
    this.$store.dispatch('category/getAllCategories')
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
#map.router-link-active,
#search.router-link-active,
#category.router-link-active {
  border-bottom: solid 3px rgba(90, 84, 75, 0.85);
}

.uk-tab > * {
  float: left;
  padding: 0px 20px;
  position: relative;
}
.content {
  margin: 25px auto;
  max-width: 1200px;
  padding: 0px 30px;
}
</style>
