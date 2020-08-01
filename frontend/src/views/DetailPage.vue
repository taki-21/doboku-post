<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader />
    <div id="detail_post">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class>
            <a @click="$router.back()" title="前ページへ戻る">
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
                  <div uk-lightbox>
                    <a :href="post.image">
                      <img :src="post.image_change" />
                    </a>
                  </div>
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
                      <CommentForm :post="post" />
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
                            <img class="comment_user_icon" :src="comment.author.icon_image" />
                            <strong>{{comment.author.username}}</strong>
                            <span>{{comment.timestamp | moment }}</span>
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
import moment from "moment";
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
  filters: {
    moment: function(date) {
      return moment(date).format("YYYY/MM/DD HH:mm");
    }
  },
  // watch: {
  //   comments: {
  //     immediate: true,
  //     handler: function() {
  //       api.get("/comments/").then(response => {
  //         this.comments = response.data.filter(x => x.post === this.id);
  //       });
  //     }
  //   }
  // },
  created() {
    api.get("/posts/" + this.id + "/").then(response => {
      this.post = response.data;
    });
    // api.get("/comments/").then(response => {
    //   this.comments = response.data.filter(x => x.post === this.id);
    // });
  },
  methods: {
    back() {
      // 1つ前へ
      this.$router.back();
    }
  }
};
</script>

<style scoped>
.v-application ol,
.v-application ul {
  padding-left: 0px;
}
.user_icon {
  width: 40px;
  height: 40px;
  margin-right: 5px;
  border-radius: 50%;
}
.comment_user_icon {
  width: 30px;
  height: 30px;
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
.uk-comment-header {
  margin-bottom: 10px;
}

.uk-comment-list > :nth-child(n + 2) {
  margin-top: 0px;
}

.comment_button {
  width: 100%;
}
</style>
