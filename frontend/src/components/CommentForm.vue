<template>
  <div>
    <form @submit.prevent="submitText()">
      <div class="uk-margin">
        <div class="uk-inline uk-width-1-1">
          <textarea class="uk-textarea" row="3" type="text" v-model="text"></textarea>
          <button
            type="submit"
            class="uk-button uk-button-primary uk-button-small"
            id="comment-btn"
          >送信</button>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import api from "@/services/api";

export default {
  props: ["post"],
  data() {
    return {
      text: "",
      author_name: this.$store.getters["auth/id"],
    };
  },
  methods: {
    submitText: function () {
      api
        .post("http://127.0.0.1:8000/api/v1/comments/", {
          post: this.post.id,
          author_name: this.author_name,
          text: this.text,
        })
        .then((response) => {
          this.$emit("CommentGet");
          console.log("送信内容: " + response.data);
        })
        .catch((error) => {
          console.log("response: ", error.response.data);
        });
      // 入力後、フォーム内の文字列をクリア
      this.text = "";
    },
  },
};
</script>

<style scoped>
.uk-textarea {
  margin-top: 10px;
  height: 100px;
}
#comment-btn {
  position: absolute;
  right: 0px;
  bottom: 0px;
}
</style>
