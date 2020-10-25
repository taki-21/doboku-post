<template>
  <div>
    <form @submit.prevent="submitText()" @click="post_comment">
      <div>
        <div class="mb-5">
          <v-textarea
            class="ma-0 pa-0"
            solo
            rows="2"
            v-model="text"
            placeholder="コメントを入力してください"
            hide-details
          >
          </v-textarea>
            <v-btn type="submit" block class="mt-1" dark color="blue-grey darken-1">
              <v-icon>mdi-send</v-icon>
              送信
            </v-btn>
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
      if (this.text) {
        api
          .post("/comments/", {
            post: this.post.id,
            author_name: this.author_name,
            text: this.text,
          })
          .then((response) => {
            // 親コンポーネントでCommentGetメソッドを実行
            this.$emit("CommentGet");
            console.log("送信内容: " + response.data);
          })
          .catch((error) => {
            console.log("response: ", error.response.data);
          });
        // 入力後、フォーム内の文字列をクリア
        this.text = "";
      }
    },
    post_comment() {
      if (this.isLoggedIn == false) {
        this.$router.replace("/login");
      }
    },
  },
};
</script>
