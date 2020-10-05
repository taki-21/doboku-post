<template>
  <div uk-sticky>
    <header class="title-header">
      <router-link class="router-link" to="/">
        <div class="title">
          <img
            class="doboku_icon"
            src="../assets/doboku.png"
            width="40"
            height="40"
          />
          <span>DOBOKU_Post</span>
        </div>
      </router-link>
      <nav>
        <HeaderSide />
      </nav>
    </header>
  </div>
</template>

<script>
import HeaderSide from "../components/HeaderSide";
export default {
  components: {
    HeaderSide,
  },
};
</script>

<style scoped>
@import "../assets/common.css";

.title-header {
  padding: 5px 5%;
  background-color: rgba(139, 138, 135, 1);
  display: flex;
  align-items: center;
  height: 60px;
}
.doboku_icon {
  position: relative;
  top: -10px;
  margin-right: 8px;
}

.title {
  text-decoration: none;
  color: black;
}
.title span {
  font-size: 40px;
  font-family: "Economica";
  position: relative;
  top: 2px;
}

nav {
  margin: 0 0 0 auto;
  padding-top: 22px;
}
</style>
