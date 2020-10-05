<template>
  <div uk-sticky>
    <header class="title-header">
      <router-link class="router-link" to="/">
        <div class="title_content">
          <img class="doboku_icon" src="../assets/doboku.png" />
          <span id="title">DOBOKU_Post</span>
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
  width: 40px;
  height: 40px;
  position: relative;
  top: -10px;
  margin-right: 8px;
}

.title_content {
  text-decoration: none;
  color: black;
  display: flex;
}
#title {
  font-size: 40px;
  font-family: "Economica";
  position: relative;
  top: 2px;
}

nav {
  margin: 0 0 0 auto;
  padding-top: 22px;
}

@media (max-width: 640px) {
  .title-header {
  padding: 5px 5%;
  background-color: rgba(139, 138, 135, 1);
  display: flex;
  align-items: center;
  height: 30px;
}

  #title {
    font-size: 20px;
    font-family: "Economica";
    position: relative;
    top: 2px;
  }
  .doboku_icon {
    width: 20px;
    height: 20px;
    position: relative;
    top: 7px;
    margin-right: 4px;
  }
}
</style>
