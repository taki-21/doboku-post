<template>
  <div
    class="uk-grid-column-small uk-child-width-1-3@l uk-child-width-1-2@m uk-child-width-1-1@s uk-text-center"
    uk-grid
  >
    <router-link
      class="router-link"
      :to="{name: 'detail', params:{id: post.id }}"
      v-for="(post, key) in postType"
      :key="key"
    >
      <div class="uk-card uk-card-hover uk-card-default" id="card">
        <div class="uk-card-media-top">
          <img :src="post.image_change" />
        </div>
        <div class="uk-card-body">
          <div class="uk-comment-header uk-position-relative">
            <div>
              <router-link
                class="show_user"
                :to="{name: 'mypage', params:{user_id: post.author.id}}"
              >
                <div>
                  <img class="user_icon" v-bind:src="post.author.icon_image" />
                  <span id="author_name">{{ post.author.username }}</span>
                </div>
              </router-link>
              <div class="timestamp">
                <span>{{ post.published_at | moment }}</span>
              </div>
              <div class="prefecture">
                <span>{{ post.prefecture }}</span>
              </div>
            </div>
          </div>
          <strong>{{ post.title }}</strong>
          <div class="comment_like_icon">
            <i id="comment-button" uk-icon="comment"></i>
            <span id="comment-count">{{ post.comments_count}}</span>
            <i id="heart-button" uk-icon="heart"></i>
            <span id="like-count">{{ post.likes_count}}</span>
          </div>
          <div v-if="post.author.id == user_id">
            <div id="edit-delete">
              <router-link class="edit-link" :to="{name: 'post_edit', params:{post_id: post.id }}">
                <i id="edit-icon" uk-icon="icon: pencil"></i>
                <span id="edit-word">編集</span>
              </router-link>
              <a class="delete-link" :href="'#modal-' + post.id" uk-toggle>
                <i id="delete-icon" uk-icon="icon: trash"></i>
                <span id="delete-word">削除</span>
              </a>
              <div :id="'modal-' + post.id" uk-modal>
                <div class="uk-modal-dialog uk-modal-body">
                  <h2 class="uk-modal-title">削除確認</h2>
                  <p>投稿：{{ post.title }}を削除します。よろしいですか？</p>
                  <p class="uk-text-right">
                    <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                    <button
                      class="uk-button uk-button-primary uk-modal-close"
                      type="button"
                      @click="DestroyPost(post.id)"
                    >OK</button>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: ["postType", "user_id"],
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY/MM/DD HH:MM");
    },
  },
};
</script>


<style scoped>
.router-link {
  text-decoration: none;
}
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
  line-height: 45px;
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
  margin-bottom: 5px;
}
#comment-count {
  margin-left: 3px;
  margin-right: 7px;
}
#heart-button {
  position: relative;
  top: -1px;
}
#like-count {
  margin-left: 3px;
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
  color: rgb(51, 51, 51);
}
.edit-link:hover,
.delete-link:hover {
  text-decoration: none;
  color: rgba(51, 51, 51, 0.5);
}

#edit-delete {
  padding-top: 5px;
  border-top: 1px solid #b1aeae;
}

#edit-icon {
  margin-right: 3px;
}
#edit-word {
  position: relative;
  top: 3px;
  margin-right: 5px;
}
#delete-icon {
  margin-left: 5px;
  margin-right: 3px;
}

#delete-word {
  position: relative;
  top: 3px;
  margin-right: 10px;
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
</style>
