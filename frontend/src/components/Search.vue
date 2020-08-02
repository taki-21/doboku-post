<template>
  <div>
    <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m" id="category_card">
      <form class="uk-grid-small" uk-grid>
        <div class="uk-width-1-5@s">
          <input
            v-model="filterQuery.title"
            @change="handleChangeQuery"
            class="uk-input"
            type="search"
            placeholder="タイトル"
          />
        </div>
        <div class="uk-width-1-5@s">
          <input class="uk-input" type="search" placeholder="カテゴリ" />
        </div>
        <div class="uk-width-1-5@s">
          <input class="uk-input" type="search" placeholder="投稿日" />
        </div>
        <div class="uk-width-1-5@s">
          <input class="uk-input" type="search" placeholder="都道府県" />
        </div>
        <div class="uk-width-1-5@s">
          <input class="uk-input" type="search" placeholder="市区町村" />
        </div>
      </form>
    </div>
    <div>{{ filterQuery }}</div>
    <div>{{ filteredPosts }}</div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      filterQuery: {
        title: ""
      }
    };
  },
  computed: {
    ...mapGetters("post", ["filteredPosts"])
  },
  mounted() {
    this.$store.commit("post/setFilterQuery", this.filterQuery);
    // this.setFilterQuery(this.filterQuery)
  },
  methods: {
    handleChangeQuery() {
      this.$store.commit("post/setFilterQuery", this.filterQuery);
    }
  }
};
</script>
