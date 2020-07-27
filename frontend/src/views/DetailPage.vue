<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div id="detail_post">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="">
            <a @click="goBack" title="前ページへ戻る">
              <i uk-icon="icon: chevron-double-left; ratio: 2"></i>
            </a>
            <div
              class="uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <div>
                <p id="post_title">{{post.title}}</p>
                <img :src="post.image_change" alt />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <pre>{{ post }}</pre>
  </div>
</template>

<script>
import MyHeader from "@/components/MyHeader";
export default {
  name: "detail",
  components: {
    MyHeader
  },
  props: {
    id: { type: Number }
  },
  data() {
    return {
      post: ""
    };
  },
  created() {
    this.axios
      .get("http://127.0.0.1:8000/api/v1/posts/" + this.id + "/")
      .then(response => {
        this.post = response.data;
      });
  },
  methods: {
    goBack() {
      if (this.hasBefore) {
        this.$router.go(-1);
      } else {
        this.$router.push({ name: "homepage" });
      }
    }
  }
};
</script>

<style scoped>
#detail_post {
  padding-top: 10px;
}
#post_title {
  font-size: 20px;
  font-weight: bold;
}
</style>
