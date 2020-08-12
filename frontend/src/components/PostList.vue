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
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: ["postType"],
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
  font-weight: bold;
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
