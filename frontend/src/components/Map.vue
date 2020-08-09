<template>
  <div>
    <input type="text" v-model="address" />
    <button type="button" @click="mapSearch">検索</button>
    <div id="map" ref="googleMap"></div>
  </div>
</template>

<script>
import GoogleMapsApiLoader from "google-maps-api-loader";

export default {
  name: "Map",
  data() {
    return {
      google: null,
      map: {},
      marker: null,
      geocoder: {},
      address: "",
      mapConfig: {
        center: {
          lat: 35.68944,
          lng: 139.69167
        },
        zoom: 5
      }
    };
  },
  async mounted() {
    this.google = await GoogleMapsApiLoader({
      apiKey: ""
    });
    this.initializeMap();
  },
  methods: {
    initializeMap() {
      this.map = new this.google.maps.Map(this.$refs.googleMap, this.mapConfig);
      // this.map = new this.google.maps.Map(document.getElementById("map"));
      this.geocoder = new this.google.maps.Geocoder();
    },
    mapSearch() {
      this.geocoder.geocode(
        {
          address: this.address
        },
        (results, status) => {
          if (status === this.google.maps.GeocoderStatus.OK) {
            this.map.setCenter(results[0].geometry.location);
            // 緯度経度の取得
            results[0].geometry.location.lat();
            results[0].geometry.location.lng();
            this.marker = new this.google.maps.Marker({
              map: this.map,
              position: results[0].geometry.location
            });
          }
        }
      );
      console.log(this.results)
    }
  }
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 800px;
}
</style>
