<template>
  <div>
    <ul class="uk-flex-center" uk-tab>
      <router-link class="router-link" to="/">新着投稿</router-link> |
      <router-link class="uk-text-large uk-text-secondary" to="/popular">人気投稿</router-link> |
      <router-link class="uk-text-large uk-text-secondary" to="/category">カテゴリ</router-link>
    </ul>
    <div>
      <router-view/>
    </div>
    <!-- <ul class="uk-flex-center" uk-tab>
      <li v-for="item in items" :key="item.id">
        <a class="uk-text-large uk-text-secondary" @click="tabIndex()">{{ item.name }}</a>
      </li>
    </ul>
    <ul class="uk-switcher uk-margin">
      <li>
        <LatestPosts />
      </li>
      <li>
        <PopularPosts />
      </li>
      <li>
        <CategoryPosts />
      </li>
      <li>
        <Map />
      </li>
      <li>
        <Search />
      </li>
    </ul>-->
  </div>
</template>

<script>
// import LatestPosts from "@/components/LatestPosts";
// import PopularPosts from "@/components/PopularPosts";
// import CategoryPosts from "@/components/CategoryPosts";
export default {
  components: {
    // LatestPosts,
    // PopularPosts,
    // CategoryPosts
  },
  data() {
    return {
      items: [
        { id: 1, name: "新着投稿" },
        { id: 2, name: "人気投稿" },
        { id: 3, name: "カテゴリ" },
        { id: 4, name: "マップ" },
        { id: 5, name: "検索" }
      ],
      isActive: ""
    };
  },
  methods: {
    tabIndex() {}
  },
  computed: {
    selectedItem() {
      // 選択されたアイテムのデータを取得する
      return this.items.find(item => item.id === this.selectedItemId);
    }
  },
  mounted() {
    console.log("あああ");
    window.addEventListener("hashchange", this.parseHash);
    console.log();
    this.parseHash();
    console.log("あああ");
  }
};
</script>
<style scoped>
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
