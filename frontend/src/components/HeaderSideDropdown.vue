<template>
  <v-card class="mx-auto">
    <v-list>
      <v-list-item-group>
        <router-link class="router-link d-sm-none" id="post" to="/newpostpage" v-if="isLoggedIn">
        <v-list-item>
          <v-list-item-icon>
              <v-icon>mdi-pencil-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title> 投稿する </v-list-item-title>
            </v-list-item-content>
        </v-list-item>
        </router-link>

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
        <v-dialog v-model="dialog" width="500" v-if="isLoggedIn">
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
            <v-card-text> ログアウトします。よろしいですか？ </v-card-text>
            <!-- <v-divider></v-divider> -->
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="dialog = false">
                キャンセル
              </v-btn>
              <v-btn color="primary" text @click="clickLogout"> OK </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
                <router-link
          class="router-link"
          to='/signup'
        >
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-account-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title> 新規登録 </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
                <router-link
          class="router-link"
          to='/login'
        >
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-login</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title> ログイン </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>

      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      dialog: false,
    };
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
