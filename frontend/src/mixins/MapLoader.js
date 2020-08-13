import GoogleMapsApiLoader from "google-maps-api-loader";
export default {
  data() {
    return {
      google: null,
      map: {},
      // marker: null,
      geocoder: {},
      // results: {},
      mapConfig: {
        center: {
          lat: 35.68944,
          lng: 139.69167,
        },
        zoom: 5,
        streetViewControl: false,
        mapTypeId: "roadmap",
        language: "ja",
      },
    };
  },
  async mounted() {
    this.google = await GoogleMapsApiLoader({
      apiKey: "AIzaSyBW7b_xx8jq8M0AKlHv00S-y1sJeZUh1FE",
    });
    this.initializeMap();
  },
  methods: {
    initializeMap() {
      this.map = new this.google.maps.Map(this.$refs.googleMap, this.mapConfig);
      this.geocoder = new this.google.maps.Geocoder();
    },
  },
};
