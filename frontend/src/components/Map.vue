<template>
  <div>
    <div id="map" ref="googleMap"></div>
  </div>
</template>

<script>
import GoogleMapsApiLoader from "google-maps-api-loader";
import { mapGetters } from "vuex";

export default {
  name: "Map",
  props: ["post", "user_id"],
  data() {
    return {
      google: null,
      map: {},
      markers: [],
      infoWindow: [],
      mapConfig: {
        center: {
          lat: 36.8,
          lng: 139.69167,
        },
        zoom: 5,
        streetViewControl: false,
        mapTypeId: "roadmap",
      },
    };
  },
  computed: {
    ...mapGetters("post", ["latestPosts"]),
    markerData() {
      if(this.user_id){
        return this.latestPosts.filter((x) => x.author.id == this.user_id)
      }
      if (this.post) {
        // 後でmapで繰り返し処理をするため、配列の形にする。
        return [this.post];
      } else {
        return this.latestPosts;
      }
    },
  },

  async mounted() {
    this.google = await GoogleMapsApiLoader({
      apiKey: process.env.VUE_APP_GOOGLE_MAP_KEY,
    });
    this.initializeMap();
  },
  methods: {
    // 地図の作成
    initializeMap() {
      this.map = new this.google.maps.Map(this.$refs.googleMap, this.mapConfig);
      this.setMarkers();
    },
    // マーカーごとの処理
    setMarkers() {
      let currentWindow;
      var my_this = this; //thisを別名で退避しておく（あとでつかうので）
      this.markerData.map((data) => {
        const marker = new this.google.maps.Marker({
          position: {
            lat: Number(data.lat),
            lng: Number(data.lng),
          },
          map: this.map,
        });

        currentWindow && currentWindow.close();
        const infoWindow = new this.google.maps.InfoWindow({
          content:
            '<div style="font-size:15px; padding:0px 10px 10px 0px;" id="infobox_' +
            data.id +
            '" data-item-id="' +
            data.id +
            '">' +
            data.title +
            "</div>",
          boxClass: "infobox",
        });

        this.google.maps.event.addListener(infoWindow, "domready", function () {
          //infoWindowが持っている内部文字列をDOMに変換
          var dumy_dom = document.createElement("div"); //ダミーの要素を作成
          dumy_dom.innerHTML = this.content; //ダミー要素にinfoWindow内のHTML文字列を読み込ませてDOMに変換

          // 内部のDOMを取得
          var id_name = dumy_dom.children[0].id; //infoWindow内の要素のID名を取得
          console.log("id_name: " + id_name);

          var inner_dom = document.getElementById(id_name); //ID名からinfoWindow内の要素オブジェクトを取得
          console.log("inner_dom: " + inner_dom);

          // アイテムのid番号を取得
          var item_id = inner_dom.dataset.itemId; //同じくリンク先用の番号を取得（data-item-idの値）
          console.log("item_id: " + item_id);
          // infoWindow内の要素にクリックイベントを設置
          inner_dom.addEventListener("click", function () {
            my_this.go(item_id);
          });
        });
        // infoWindowをマーカーに紐付け
        marker.addListener("click", function () {
          currentWindow && currentWindow.close();
          infoWindow.open(this.map, marker);
          currentWindow = infoWindow;
        });
        // return marker;
      });
    },
    go(item_id) {
      console.log("item_id: " + item_id);
      this.$router.push({ name: "detail", params: { id: item_id } });
    },
  },
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 700px;
}

#OK_button {
  margin-left: 5px;
}

/* .gm-style .gm-style-iw-c {
  position: absolute;
  box-sizing: border-box;
  overflow: hidden;
  top: 0;
  left: 0;
  transform: translate(-50%, -100%);
  background-color: red;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 7px 1px rgba(0, 0, 0, 0.3);
} */
</style>
