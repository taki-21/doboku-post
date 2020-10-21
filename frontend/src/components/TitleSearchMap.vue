<template>
  <div>
    <div v-if="title">
    <div v-show="isLoading" class="loader">
      <span uk-spinner></span>
    </div>
      <div v-show="!isLoading">
        <input
          class="uk-input uk-form-width-medium"
          type="text"
          v-model="title"
          @change="mapSearch"
        />
        <div class="uk-margin" uk-margin>
          <div v-if="results[0]">
            <input
              class="uk-input uk-form-width-large"
              type="text"
              v-model="results[0].formatted_address"
            />
            <button
              id="ok_button"
              class="uk-button uk-button-default uk-modal-close"
              @click="call_parent"
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <span id="error_message">タイトルを入力してください</span>
    </div>
    <div v-show="title && !isLoading" id="map" ref="googleMap"></div>
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
      marker: null,
      results: {},
      isLoading: true,
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
      return this.results[0].geometry.viewport.Ya.i;
    },
    lng: function () {
      return this.results[0].geometry.viewport.Sa.i;
    },
  },
  methods: {
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
            this.marker = new this.google.maps.Marker({
              map: this.map,
              position: results[0].geometry.location,
            });
            this.isLoading = false;
          }
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
@import "../assets/common.css";

#map {
  width: 100%;
  height: 600px;
}
.loader {
    text-align: center;
    position: relative;
    top: 0px;
}
</style>
