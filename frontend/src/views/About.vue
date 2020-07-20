<template>
  <div>
    <MyHeader></MyHeader>
    <h1>About.vue</h1>
    <div>
      <p>{{ posts }}</p>
      <ul>
        <li v-for="(post, key) in posts" :key="key">
          {{ post.title}}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import MyHeader from "../components/MyHeader";
export default {
  components: {
    MyHeader
  },
  data() {
    return {
      posts: null
    };
  },
  mounted() {
    this.axios.get("http://127.0.0.1:8000/api/posts/")
    .then(response => {
      this.posts = response.data
    });
  }
};
</script>
