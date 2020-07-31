<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div id="detail_post">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class>
            <a @click="goBack" title="前ページへ戻る">
              <i uk-icon="icon: chevron-double-left; ratio: 2"></i>
            </a>
            <div class="uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large">
              <div uk-grid>
                <div class="uk-width-3-5">
                  <div>
                    <img class="user_icon" v-bind:src="post.author.icon_image" />
                    <span class="uk-comment-title uk-margin-remove">{{ post.author.username }}</span>
                  </div>
                  <p id="post_title">{{post.title}}</p>
                  <img :src="post.image_change" alt />
                </div>
                <div class="uk-width-2-5">
                  <div>
                    <button
                      class="uk-button uk-button-default comment_button"
                      type="button"
                      uk-toggle="target: .toggle-usage"
                    >
                      <span uk-icon="icon: comment"></span>
                      コメントを投稿する
                    </button>
                    <div class="toggle-usage"></div>
                    <div class="toggle-usage" hidden>
                      <CommentForm/>
                    </div>

                  </div>

                  <ul class="uk-comment-list">
                    <li v-for="comment in comments" :key="comment.id">
                      <article
                        class="uk-comment uk-comment-primary uk-visible-toggle"
                        tabindex="-1"
                      >
                        <header class="uk-comment-header uk-position-relative">
                          <div>
                            <img class="user_icon" :src="comment.author.icon_image" />
                            <strong>{{comment.author.username}}</strong>
                            <span>{{comment.timestamp}}</span>
                          </div>
                        </header>
                        <div>
                          <p>{{comment.text}}</p>
                        </div>
                      </article>
                    </li>
                  </ul>
                  <!-- <p>{{comments}}</p> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MyHeader from "@/components/MyHeader";
import CommentForm from "@/components/CommentForm";

import api from "@/services/api";

export default {
  name: "detail",
  components: {
    MyHeader,
    CommentForm
  },
  props: {
    id: { type: Number }
  },
  data() {
    return {
      post: "",
      comments: []
    };
  },
  mounted() {
    api.get("/posts/" + this.id + "/").then(response => {
      this.post = response.data;
    });
    api.get("/comments/").then(response => {
      this.comments = response.data.filter(x => x.post === this.id);
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
.v-application ol, .v-application ul {
    /* padding-left: 24px; */
}
.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}

#detail_post {
  padding-top: 10px;
}
#post_title {
  font-size: 20px;
  font-weight: bold;
}

.uk-comment-primary {
  padding: 15px;
  border-left: 4px solid black;
  border-bottom: 1px solid black;
}
</style>
