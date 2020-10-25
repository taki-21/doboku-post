<template>
  <v-app>
    <v-app-bar app color="blue-grey lighten-2" clipped-left>
      <v-app-bar-nav-icon class="d-none"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link to="/" id="title">
          <v-btn icon class="mb-2" disable>
            <v-img
              src="./assets/doboku.png"
              max-width="35px"
              max-height="35px"
            />
          </v-btn>
          DOBOKU_Post
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div v-if="isLoggedIn && user.icon_image">
        <router-link class="router-link" id="post" to="/newpostpage">
          <v-btn depressed elevation="3" color="blue-grey lighten-4"
            ><v-icon>mdi-pencil-outline</v-icon>投稿する</v-btn
          >
        </router-link>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn text v-bind="attrs" v-on="on" class="ma-2">
              <v-avatar size="36px" class="ma-2">
                <img class="user_icon" :src="user.icon_image" />
              </v-avatar>
              <span>
                {{ user.username }}
              </span>
            </v-btn>
          </template>
          <v-card class="mx-auto">
            <v-list>
              <v-list-item-group>
                <router-link
                  class="router-link"
                  :to="{ name: 'mypage', params: { user_id: user.id } }"
                  v-if="user.id"
                >
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-account</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title> マイページ </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </router-link>
                <v-dialog v-model="dialog" width="500">
                  <template v-slot:activator="{ on, attrs }">
                    <v-list-item v-bind="attrs" v-on="on">
                      <v-list-item-icon>
                        <v-icon>mdi-logout</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content
                        ><v-list-item-title>
                          ログアウト
                        </v-list-item-title></v-list-item-content
                      >
                    </v-list-item>
                  </template>
                  <v-card>
                    <v-card-title class="headline grey lighten-2">
                      ログアウト確認
                    </v-card-title>
                    <v-card-text>
                      ログアウトします。よろしいですか？
                    </v-card-text>
                    <!-- <v-divider></v-divider> -->
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="dialog = false">
                        キャンセル
                      </v-btn>
                      <v-btn color="primary" text @click="clickLogout">
                        OK
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>
      </div>
      <div v-else>
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
    </v-app-bar>
    <GlobalMessage />
    <!-- <v-navigation-drawer app>
    <v-list-item>
      <v-list-item-title class="title">
        Application
      </v-list-item-title>
      <v-btn icon>
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
    </v-list-item>
    <v-divider />
    <v-list nav>
      <v-list-item v-for="menu in menus" :key="menu.title" :to="menu.url">
        <v-list-item-icon>
          <v-icon>{{ menu.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ menu.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer> -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
    <!-- <v-footer app color="blue-grey lighten-2">
      <v-col class="text-center"> 2020 - DOBOKU_Post </v-col></v-footer
    > -->
  </v-app>
</template>

<script>
// import HeaderSide from "./components/HeaderSide";
import GlobalMessage from "@/components/GlobalMessage.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    // HeaderSide,
    GlobalMessage,
  },
  data() {
    return {
      drawer: null,
      dialog: false,
      // items: [
      //   { title: "写真", icon: "mdi-image" },
      //   { title: "書籍", icon: "mdi-book-open-page-variant" },
      //   { title: "記事", icon: "mdi-newspaper-variant" },
      // ],
      // right: null,
    };
  },
  computed: {
    ...mapGetters("user", {
      user: "getUser",
    }),
    ...mapGetters("user", {
      user: "getUser",
    }),
    isLoggedIn: function () {
      return this.$store.getters["auth/isLoggedIn"];
    },
  },
  methods: {
    // ログアウトリンク押下
    clickLogout: function () {
      sessionStorage.clear();
      this.dialog = false;
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("user/logout");
      this.$store.dispatch("message/setInfoMessage", {
        message: "ログアウトしました",
      });
      this.$router.replace("/login");
    },
  },
};
</script>
<style>
@import "./assets/common.css";

/* html {
  overflow: overlay;
} */
/* v-app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
} */
#title {
  height: 50px;
  text-decoration: none;
  color: black;
  font-size: 40px;
  font-family: "Economica";
}

.v-enter-active {
  transition: opacity 0.4s;
}
.v-enter {
  opacity: 0;
}
.v-enter-to {
  opacity: 1;
}
.v-leave,
.v-leave-active,
.v-leave-to {
  opacity: 0;
}
</style>
