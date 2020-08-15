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
  props: ["user_id"],
  data() {
    return {
      google: null,
      map: {},
      marker: [],
      geocoder: {},
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
    markerData: function () {
      return this.latestPosts.filter((x) => x.author.id == this.user_id);
    },
  },
  async mounted() {
    this.google = await GoogleMapsApiLoader({
      apiKey: "",
    });
    this.initializeMap();
  },
  methods: {
    // 地図の作成
    initializeMap() {
      this.map = new this.google.maps.Map(this.$refs.googleMap, this.mapConfig);
      this.geocoder = new this.google.maps.Geocoder();
      this.setMarkers();
    },
    // マーカーごとの処理
    setMarkers() {
      let currentWindow;
      this.markerData.map((data) => {
        const marker = new this.google.maps.Marker({
          position: {
            lat: Number(data.lat),
            lng: Number(data.lng),
          },
          map: this.map,
        });

        marker.addListener("click", () => {
          currentWindow && currentWindow.close();
          const infoWindow = new this.google.maps.InfoWindow({
            content: "<div>" + data.title + "</div>",
          });
          infoWindow.open(this.map, marker);
          currentWindow = infoWindow;
        });
      });
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
</style>
