<template>
  <div>
    <ul class="uk-flex-center" uk-tab>
      <li>
        <a class="uk-text-large uk-text-secondary">新着投稿</a>
      </li>
      <li>
        <a class="uk-text-large uk-text-secondary">人気投稿</a>
      </li>
      <li>
        <a class="uk-text-large uk-text-secondary">カテゴリ</a>
      </li>
      <li>
        <a class="uk-text-large uk-text-secondary">マップ</a>
      </li>
      <li>
        <a class="uk-text-large uk-text-secondary">検索</a>
      </li>
    </ul>
    <ul class="uk-switcher uk-margin">
      <li>
        <LatestPosts />
      </li>
      <li><PopularPosts/></li>
      <!-- <li><Category/></li> -->
      <!-- <li><Map/></li> -->
      <!-- <li><Search/></li>--> 
    </ul>
  </div>
</template>

<script>
import LatestPosts from "@/components/LatestPosts";
import PopularPosts from "@/components/PopularPosts";
export default {
  components: {
    LatestPosts,
    PopularPosts
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
