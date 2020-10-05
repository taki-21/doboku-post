<template>
  <div>
    <form @submit.prevent="submitText()" @click="post_comment">
      <div>
        <div class="uk-inline uk-width-1-1">
          <textarea
            class="uk-textarea"
            row="4"
            type="text"
            v-model="text"
            placeholder="コメントを入力してください"
          ></textarea>
          <button
            class="uk-button uk-button-default uk-button-small"
            type="submit"
            id="comment-btn"
          >
            <span uk-icon="icon: comment"></span>
            送信
          </button>
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
  computed: {
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },

  },
  methods: {
    submitText: function () {
      api
        .post("/comments/", {
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
    post_comment() {
      if (this.isLoggedIn == false) {
        this.$router.replace("/login");
      }
    },
  },
};
</script>

<style scoped>
#comment-btn {
  width: 100%;
  background-color: rgba(140, 140, 135, 0.3);
  margin-bottom: 20px;
}
</style>
