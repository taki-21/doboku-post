<template>
  <div v-if="isLoggedIn && user.icon_image">
    <div class="d-none d-sm-flex">
      <router-link class="router-link" id="post" to="/newpostpage">
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
      <!-- <v-switch
      v-model="closeOnContentClick"
      label="Close on content click"
    ></v-switch> -->
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

<style scoped>
@import "../assets/common.css";
#post {
  padding-left: 0;
}

#userlist_button {
  background-color: rgba(204, 194, 149, 0.5);
}
#post_button {
  background-color: rgba(225, 225, 225, 0.5);
}
#signup_button {
  background-color: rgba(230, 160, 160, 0.4);
}
#login_button {
  background-color: rgba(150, 210, 200, 0.4);
}
.show_user {
  font-size: large;
  font-weight: bold;
  color: #333333;
  text-decoration: none;
}

li {
  list-style: none;
}

#logout {
  color: black;
  text-decoration: none;
}

.dropdown {
  margin: 10px auto;
}

/* UIkitの上書き */

.uk-modal-body {
  display: flow-root;
  padding: 30px 30px;
  border-radius: 5px;
}
</style>
