<template>
  <div v-if="isLoggedIn && user.icon_image">
    <div class="d-none d-sm-flex">
      <router-link class="router-link" to="/newpostpage">
        <v-btn
          depressed
          elevation="3"
          color="blue-grey lighten-4"
          large
          class="ma-1"
          ><v-icon>mdi-pencil-outline</v-icon>投稿する</v-btn
        >
      </router-link>
      <v-menu offset-y close-on-click>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            text
            v-bind="attrs"
            v-on="on"
            class="ma-2 pl-0"
            style="text-transform: none"
          >
            <v-avatar size="36px" class="ma-2">
              <img :src="user.icon_image" />
            </v-avatar>
            <span style="font-size: 20px">
              {{ user.username }}
            </span>
            <span>
              <v-icon>mdi-chevron-down</v-icon>
            </span>
          </v-btn>
        </template>
        <HeaderSideDropdown />
      </v-menu>
    </div>
    <div class="d-sm-none">
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on" style="text-transform: none">
            <v-avatar size="40px">
              <img :src="user.icon_image" />
            </v-avatar>
          </v-btn>
        </template>
        <HeaderSideDropdown />
      </v-menu>
    </div>
  </div>
  <div v-else>
    <div class="d-none d-sm-flex">
      <router-link class="router-link" id="post" to="/signup">
        <v-btn depressed elevation="3" color="blue-grey lighten-4" class="ma-2"
          ><v-icon>mdi-account-plus</v-icon>新規登録</v-btn
        >
      </router-link>
      <router-link class="router-link" id="post" to="/login">
        <v-btn depressed elevation="3" color="blue-grey lighten-4" class="ma-2"
          ><v-icon>mdi-login</v-icon>ログイン</v-btn
        >
      </router-link>
    </div>
    <div class="d-sm-none">
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on" style="text-transform: none">
            <v-icon size="40px">
              mdi-menu
            </v-icon>
          </v-btn>
        </template>
        <HeaderSideDropdown />
      </v-menu>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import HeaderSideDropdown from "@/components/HeaderSideDropdown";
export default {
  components: {
    HeaderSideDropdown,
  },
  data() {
    return {
      dialog: false,
      closeOnContentClick: true,
    };
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser",
    }),
    isLoggedIn: function () {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },
};
</script>
