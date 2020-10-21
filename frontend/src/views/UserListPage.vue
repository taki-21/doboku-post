<template>
  <div>
    <MyHeader />
    <div class="uk-section uk-flex uk-flex-middle">
      <div class="uk-width-1-1">
        <div class="uk-container">
          <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid>
            <div class="uk-width-1-1@m">
              <!-- <div
                id="userlist_card"
                class="uk-margin uk-card uk-card-default uk-card-body uk-box-shadow-large"
              > -->
                <router-link
                  class="router-link"
                  v-for="(user, key) in userLists"
                  :key="key"
                  :to="{ name: 'mypage', params: { user_id: user.id } }"
                >
                  <div
                    id="profile_card"
                    class="uk-card uk-card-default uk-grid-collapse uk-margin"
                    uk-grid
                  >
                    <div class="uk-width-1-5@s uk-width-1-3">
                      <div class="uk-card-media-left uk-cover-container">
                        <img
                          class="mypage_user_icon"
                          :src="user.icon_image"
                          uk-cover
                        />
                        <canvas width="400" height="400"></canvas>
                      </div>
                    </div>
                    <div class="uk-width-2-5@s uk-width-2-3">
                      <div id="username_content">
                        <div id="username">{{ user.username }}</div>
                      </div>
                      <div id="profile_introduction">
                        <div>
                          <div>{{ user.introduction }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-2-5@s uk-width-1-4">
                      <div id="date_joined_word">登録日</div>
                      <div>{{user.date_joined | moment}}</div>
                      <!-- <div v-if="previousPosts[0]" class="chart">
                        <div id="piechart">
                          <PieChart
                            v-if="loaded"
                            :data="pieChartData"
                            :options="options"
                            style="
                              position: relative;
                              width: 460px;
                              height: 220px;
                            "
                          ></PieChart>
                        </div>
                      </div> -->
                    </div>
                  </div>
                </router-link>
              <!-- </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MyHeader from "@/components/MyHeader.vue";
import api from "@/services/api";
import moment from "moment";


export default {
  components: {
    MyHeader,
  },
  data() {
    return {
      userLists: [],
      postURL: "/users/",
    };
  },
  mounted() {
    api.get(this.postURL).then((response) => {
      this.userLists = response.data;
    });
  },
    filters: {
    moment: function (date) {
      return moment(date).format("Y/MM/DD HH:MM");
    },
  },

};
</script>

<style scoped>
@import "../assets/common.css";

.uk-section {
  padding:20px 60px;
  /* padding-right: 60px;
  padding-left: 60px; */
}

#profile_card {
  overflow: hidden;
  border-radius: 5px;
  background-color: rgb(250, 250, 250, 0.98);
  margin-bottom: 30px;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.15);
}
#username_content {
  display: flex;
  padding: 30px 30px 5px 30px;
}
#username {
  font-size: 40px;
  font-weight: bold;
}
#profile_introduction {
  max-width: 300px;
  padding: 0px 0px 0px 30px;
  white-space: pre-wrap;
}
#date_joined_word{
  font-size:20px;
  font-weight: bold;
}


</style>
