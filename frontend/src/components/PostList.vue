<template>
  <div>
    <div v-show="isLoading" class="text-center">
      <v-progress-circular
        indeterminate
        color="blue-gray"
      ></v-progress-circular>
    </div>
    <div v-show="!isLoading">
      <v-container>
        <v-row>
          <v-col
            class="pa-1 pa-sm-2"
            v-for="(post, key) in postType"
            :key="key"
            cols="6"
            lg="4"
            md="4"
            sm="6"
            xs="3"
          >
            <v-hover>
              <template v-slot:default="{ hover }">
                <v-card :elevation="hover ? 15 : 3" color="blue-grey lighten-5">
                  <router-link
                    style="text-decoration: none"
                    :to="{ name: 'detail', params: { post_id: post.id } }"
                  >
                    <v-img eager :src="post.image"></v-img>
                    <v-card-title class="pa-1 pa-sm-4">
                      <router-link
                        style="text-decoration: none"
                        :to="{
                          name: 'mypage',
                          params: { user_id: post.author.id },
                        }"
                      >
                        <v-btn
                          text
                          class="px-0"
                          style="text-transform: none; text-decoration: none"
                        >
                          <v-avatar size="24px" class="mr-2">
                            <img :src="post.author.icon_image" />
                          </v-avatar>
                          <span class="text-body-2 text-sm-h6">{{
                            post.author.username
                          }}</span>
                        </v-btn>
                      </router-link>
                    </v-card-title>
                    <v-card-subtitle
                      class="pb-0 text-center text-caption text-sm-h6"
                    >
                      {{ post.title }}
                    </v-card-subtitle>
                    <v-card-actions class="px-2 py-0 px-sm-4 py-sm-2">
                      <div
                        class="px-0 text-caption text-sm-body-2"
                        style="color: #263238"
                      >
                        <span class="px-1 px-sm-2">{{
                          post.published_at | moment
                        }}</span>
                      </div>
                      <div
                        class="text-caption text-sm-body-2"
                        style="color: #263238"
                      >
                        <span v-if="post.prefecture">{{
                          post.prefecture
                        }}</span>
                        <span v-else>---</span>
                      </div>

                      <v-spacer></v-spacer>
                      <div class="d-none d-sm-flex">
                        <v-icon medium class="pr-1">mdi-message-text</v-icon>
                        <span style="color: #263238">{{
                          post.comments_count
                        }}</span>
                        <v-icon medium class="ml-2 pr-1"
                          >mdi-heart-outline</v-icon
                        >
                        <span style="color: #263238">{{
                          post.likes_count
                        }}</span>
                      </div>
                      <div class="d-flex d-sm-none">
                        <v-icon small class="pr-0">mdi-message-text</v-icon>
                        <span style="color: #263238">{{
                          post.comments_count
                        }}</span>
                        <v-icon small class="ml-1 pr-0"
                          >mdi-heart-outline</v-icon
                        >
                        <span style="color: #263238">{{
                          post.likes_count
                        }}</span>
                      </div>
                    </v-card-actions>
                  </router-link>
                  <div v-if="post.author.id == user_id">
                    <v-divider class="mx-4 my-0"></v-divider>
                    <v-card-actions>
                      <v-btn
                        text
                        style="text-decoration: none"
                        :to="{
                          name: 'post_edit',
                          params: { post_id: post.id },
                        }"
                      >
                        <v-icon>mdi-pencil</v-icon>
                        編集
                      </v-btn>
                      <v-btn text @click.stop="onClickBtn(post)">
                        <v-icon>mdi-delete</v-icon>
                        削除
                      </v-btn>
                    </v-card-actions>
                    <v-dialog
                      v-model="dialog"
                      v-if="currentPost"
                      activator
                      max-width="600px"
                    >
                      <v-card class="pa-2">
                        <v-card-title>削除確認</v-card-title>
                        <v-card-text>
                          投稿：{{
                            currentPost.title
                          }}を削除します。よろしいですか？</v-card-text
                        >
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn @click="dialog = false"> キャンセル </v-btn>
                          <v-btn
                            color="blue-grey lighten-3"
                            @click="DestroyPost(currentPost.id)"
                            class="ml-4"
                          >
                            OK
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </div>
                </v-card>
              </template>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
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
import { watchScrollPosition, clearSession } from "@/mixins/utility";

export default {
  props: [
    "postType",
    "user_id",
    "isLoading",
    "nextPage",
    "postURL",
    "sessionKey",
  ],
  data() {
    return {
      page: 1,
      dialog: false,
      currentPost: null,
    };
  },
  mixins: [watchScrollPosition, clearSession],

  methods: {
    DestroyPost(post_id) {
      this.dialog = false;
      this.clearSession();
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
                $state.loaded();
              }
            }
          }, 500);
        });
    },
    onClickBtn(post) {
      this.currentPost = post;
      this.dialog = true;
    },
  },
  filters: {
    moment: function (date) {
      return moment(date).format("MM月DD日");
    },
  },
};
</script>
