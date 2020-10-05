<template>
  <div>
    <div v-show="loading" class="loader">
      <span uk-spinner></span>
    </div>
    <div v-show="!loading">
      <div
        class="uk-grid-column-small uk-child-width-1-2 uk-child-width-1-2@s uk-child-width-1-2@m uk-child-width-1-3@l uk-text-center"
        uk-grid
      >
        <router-link
          class="router-link"
          v-for="(post, key) in postType"
          :key="key"
          :to="{ name: 'detail', params: { post_id: post.id } }"
        >
          <div class="uk-card uk-card-hover uk-card-default" id="card">
            <div class="uk-card-media-top">
              <img :src="post.image" />
            </div>
            <div class="uk-card-body">
              <div class="uk-comment-header uk-position-relative">
                <div>
                  <router-link
                    class="show_user"
                    :to="{
                      name: 'mypage',
                      params: { user_id: post.author.id },
                    }"
                  >
                    <!-- <div> -->
                      <img
                        class="user_icon"
                        v-bind:src="post.author.icon_image"
                      />
                      <span id="author_name">{{ post.author.username }}</span>
                    <!-- </div> -->
                  </router-link>
                  <div class="timestamp">
                    <span>{{ post.published_at | moment }}</span>
                  </div>
                  <div class="prefecture">
                    <span>{{ post.prefecture }}</span>
                  </div>
                </div>
              </div>
              <span id="post_title">{{ post.title }}</span>
              <div class="comment_like_icon">
                <i id="icon" uk-icon="comment"></i>
                <span id="comment-count">{{ post.comments_count }}</span>
                <i id="icon" uk-icon="heart"></i>
                <span id="like-count">{{ post.likes_count }}</span>
              </div>
              <div v-if="post.author.id == user_id">
                <div id="edit-delete">
                  <router-link
                    class="edit-link"
                    :to="{ name: 'post_edit', params: { post_id: post.id } }"
                  >
                    <i id="icon" uk-icon="icon: pencil"></i>
                    <span id="edit-word">編集</span>
                  </router-link>
                  <a class="delete-link" :href="'#modal-' + post.id" uk-toggle>
                    <i id="icon" uk-icon="icon: trash"></i>
                    <span id="delete-word">削除</span>
                  </a>
                  <div :id="'modal-' + post.id" uk-modal>
                    <div class="uk-modal-dialog uk-modal-body">
                      <h2 class="uk-modal-title">削除確認</h2>
                      <p>
                        投稿：{{ post.title }}を削除します。よろしいですか？
                      </p>
                      <p class="uk-text-right">
                        <button
                          class="uk-button uk-button-default uk-modal-close"
                          type="button"
                        >
                          キャンセル
                        </button>
                        <button
                          id="ok_button"
                          class="uk-button uk-button-default uk-modal-close"
                          type="button"
                          @click="DestroyPost(post.id)"
                        >
                          OK
                        </button>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </div>
      <div v-if="nextPage">
        <infinite-loading spinner="spiral" @infinite="infiniteHandler">
          <span slot="no-more"></span>
          <span slot="no-results"></span>
        </infinite-loading>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import api from "@/services/api";
import { watchScrollPosition } from "@/mixins/utility";

export default {
  props: [
    "postType",
    "user_id",
    "loading",
    "nextPage",
    "postURL",
    "sessionKey",
  ],
  data() {
    return {
      page: 1,
    };
  },
  mixins: [watchScrollPosition],

  methods: {
    DestroyPost(post_id) {
      sessionStorage.clear();
      this.$emit("parentPostDelete", post_id);
    },
    infiniteHandler($state) {
      this.page += 1;
      sessionStorage.setItem(this.sessionKey, this.page);
      api
        .get(this.postURL, {
          params: {
            page: this.page,
          },
        })
        .then(({ data }) => {
          setTimeout(() => {
            if (data.results.length) {
              if (data.next === null) {
                this.postType.push(...data.results);
                $state.complete();
              } else {
                this.postType.push(...data.results);
                // this.page += 1;
                $state.loaded();
              }
            }
          }, 500);
        });
    },
  },
  filters: {
    moment: function (date) {
      return moment(date).format("MM/DD HH:MM");
    },
  },
};
</script>


<style scoped>
@import "../assets/common.css";

.user_icon {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}
#card {
  overflow: hidden;
  border-radius: 5px;
  background-color: #eaeeee;
  margin-bottom: 20px;
  max-width: 640px;
  margin: 0px auto;
}
.timestamp {
  font-size: 12px;
  text-align: right;
}
.prefecture {
  font-size: 12px;
  text-align: right;
}
.show_user {
  text-decoration: none;
  /* line-height: 30px; */
  float: left;
  font-size: large;
  color: #333333;
}
.show_user:hover {
  color: rgba(90, 84, 75, 0.7);
}
.post_content {
  width: 100%;
  font-size: small;
  height: 40px;
}
.comment_like_icon {
  text-align: right;
  margin-bottom: 2px;
}
#comment-count {
  position: relative;
  top: 1px;
  margin-left: 2px;
  margin-right: 7px;
}
#like-count {
  position: relative;
  top: 1px;
  margin-left: 2px;
}
#author_name {
  position: relative;
  top: 3px;
  margin-left: 10px;
  font-size: 20px;
}
.edit-link,
.delete-link {
  text-decoration: none;
  color: rgb(50, 50, 50);
}
.edit-link:hover,
.delete-link:hover {
  text-decoration: none;
  color: rgba(50, 50, 50, 0.5);
}

#edit-delete {
  /* padding-top: 0px; */
  border-top: 1px solid #b1aeae;
}

#edit-word {
  position: relative;
  top: 1px;
  margin-left: 2px;
  margin-right: 10px;
  font-size: 16px;
}

#delete-word {
  position: relative;
  top: 1px;
  margin-left: 2px;
  font-size: 16px;
}

/* UIkitの上書き */
.uk-card-body {
  padding: 10px 20px;
}
.uk-comment-header {
  display: flow-root;
  margin-bottom: 0px;
}
* + .uk-grid-margin,
.uk-grid + .uk-grid,
.uk-grid > .uk-grid-margin {
  margin-top: 20px;
}
.uk-modal-body {
  display: flow-root;
  padding: 30px 30px;
  border-radius: 5px;
}
/*レスポンシブ*/
@media (max-width: 640px) {
  /* .timestamp, */
  .prefecture,
  .comment_like_icon {
    display: none;
  }
  .timestamp{
    font-size: 5px;
  }
  .user_icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
  }
  .show_user {
    text-decoration: none;
    line-height: 20px;
    float: left;
    /* font-size: large; */
    color: #333333;
  }

  #author_name {
    position: relative;
    top: 0px;
    margin-left: 5px;
    font-size: 12px;
  }
  .uk-card-body {
  padding: 5px 5px 3px 5px;
}
#post_title{
  font-size: 12px;
}

}
</style>
