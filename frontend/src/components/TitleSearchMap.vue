<template>
  <div>
    <input class="uk-input uk-form-width-medium" type="text" v-model="title" @change="mapSearch" />
    <button type="button" @click="mapSearch">検索</button>
    <div class="uk-margin" uk-margin>
      <div v-if="results[0]">
        <input
          class="uk-input uk-form-width-large"
          type="text"
          v-model="results[0].formatted_address"
        />
        <button
          id="OK_button"
          class="uk-button uk-button-default uk-modal-close"
          @click="call_parent"
        >OK</button>
      </div>
    </div>
    <div id="map" ref="googleMap"></div>
  </div>
</template>

<script>
// import GoogleMapsApiLoader from "google-maps-api-loader";
import google from "../mixins/MapLoader";
import map from "../mixins/MapLoader";
import geocoder from "../mixins/MapLoader";

export default {
  name: "Map",
  props: ["title"],
  mixins: [google, map, geocoder],

  data() {
    return {
      // google: null,
      // map: {},
      marker: null,
      // geocoder: {},
      results: {},
      // mapConfig: {
      //   center: {
      //     lat: 35.68944,
      //     lng: 139.69167,
      //   },
      //   zoom: 5,
      //   streetViewControl: false,
      //   mapTypeId: "roadmap",
      //   language: "ja",
      // },
    };
  },
  computed: {
    prefecture: function () {
      return this.results[0].address_components.filter(function (component) {
        return component.types.indexOf("administrative_area_level_1") > -1;
      });
    },
    address: function () {
      return this.results[0].formatted_address;
    },
    lat: function () {
      return this.results[0].geometry.viewport.ab.i;
    },
    lng: function () {
      return this.results[0].geometry.viewport.Va.i;
    },
  },
  // async created() {
  //   this.google = await GoogleMapsApiLoader({
  //     apiKey: "",
  //   });
  //   this.initializeMap();
  // },
  methods: {
    // initializeMap() {
    //   this.map = new this.google.maps.Map(this.$refs.googleMap, this.mapConfig);
    //   this.geocoder = new this.google.maps.Geocoder();
    // },
    mapSearch() {
      if (this.marker) {
        this.marker.setMap(null);
      }
      this.geocoder.geocode(
        {
          address: this.title,
          // 検索時英語で表記されるのを防ぐためregionの設定を行う
          region: "jp",
        },
        (results, status) => {
          if (status === this.google.maps.GeocoderStatus.OK) {
            this.results = results;

            this.map.setCenter(results[0].geometry.location);
            // 緯度経度の取得
            // results[0].geometry.location.lat();
            // results[0].geometry.location.lng();
            this.marker = new this.google.maps.Marker({
              map: this.map,
              position: results[0].geometry.location,
            });
          }
          console.log(results[0]);
        }
      );
    },
    call_parent() {
      this.$emit(
        "callParent",
        this.address,
        this.prefecture,
        this.lat,
        this.lng
      );
    },
  },
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 600px;
}

#OK_button {
  margin-left: 5px;
}
</style>
