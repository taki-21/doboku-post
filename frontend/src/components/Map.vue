<template>
  <div id="Map">
    <p>Google Map</p>
    <GmapMap
      :center="{lat:10, lng:10}"
      :zoom="7"
      :options="{streetViewControl: false}"
      map-type-id="terrain"
      style="width: 800px; height: 600px"
      @dragend="onDragEnd"
    >
      <GmapMarker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :clickable="true"
        :draggable="true"
        @click="center=m.position"
      />
    </GmapMap>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      markers: [{ position: { lat: 10, lng: 10 } }]
    };
  },
  methods: {
    onDragEnd() {
      console.log("hoge");
    }
  }
};
</script>
