<template>
  <div>
    <!-- <pre>{{ categories }}</pre> -->
    <div class="uk-card uk-card-default uk-card-body uk-width-1-1@m">
      <div
        class="uk-grid-column-small uk-grid-row-small uk-child-width-1-2@s uk-text-center"
        uk-grid
      >
        <div v-for="category in categories" :key="category.id">
          <button class="uk-button uk-button-default uk-button-large uk-width-1-1" @click='categoryPost(category.id)'>
            <span>{{category.name}}</span>
          </button>
        </div>
        <span>Selected: {{ selected }}</span>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      categories: [],
      selected: [],
      posts: [],
    };
  },
  mounted() {
    this.axios
      .get("http://127.0.0.1:8000/api/v1/categories/")
      .then(response => {
        this.categories = response.data;
      });
  },
  methods: {
    categoryPost(category_post){
      this.selected = category_post
    }
  }
};
</script>

<style scoped>
span {
  font-size: 20px;
}
</style>
