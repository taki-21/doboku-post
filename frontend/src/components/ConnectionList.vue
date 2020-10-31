<template>
  <v-list>
    <v-list-item
      v-for="(user, key) in connectionList"
      :key="key"
      @click="closeModal()"
      :to="{
        name: 'mypage',
        params: { user_id: user.id },
      }"
      style="text-decoration: none"
    >
      <v-list-item-avatar>
        <v-img :src="user.icon_image"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title v-text="user.username"></v-list-item-title>
      </v-list-item-content>
      <v-list-item-icon v-if="loginUserFollowingList.includes(user.id)">
        <v-btn
          block
          dark
          class="text-sm-body-1 font-weight-black"
          color="blue-grey darken-2"
        >
          フォロー中
        </v-btn>
      </v-list-item-icon>
      <v-list-item-icon v-else> </v-list-item-icon>
    </v-list-item>
    <v-list-item v-if="!connectionList[0]">
      ユーザーが存在しません
    </v-list-item>
  </v-list>
</template>

<script>
import api from "@/services/api";
import { mapGetters } from "vuex";
export default {
  props: ["connectionList"],
  data() {
    return {
      loginUserFollowingList: [],
    };
  },
  computed: {
    ...mapGetters("user", {
      login_user_id: "id",
    }),

    isFollowing() {
      return function (user_id) {
        return this.confirmFollowing(user_id);
      };
    },
  },
  mounted() {
    this.getLoginUserFollowingList();
  },
  methods: {
    closeModal() {
      this.$emit("closeModal");
    },

    getLoginUserFollowingList() {
      api
        .get("/connections/", {
          params: {
            following: this.login_user_id,
          },
        })
        .then((response) => {
          if (response.data[0]) {
            this.loginUserFollowingList = response.data.map(
              (user) => user.follower.id
            );
          }
        });
    },
  },
};
</script>
