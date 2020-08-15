<template>
  <div>
    <header class="title-header" uk-sticky>
      <router-link class='router-link' to="/">
        <div class="title">
          <img class="doboku_icon" src="../../../media/doboku.png" width="40" height="40" />
          <span>DOBOKU_Post</span>
        </div>
      </router-link>
      <nav>
        <HeaderSide />
      </nav>
    </header>
  </div>
</template>

<style scoped>
.router-link {
  text-decoration: none;
}
.title-header {
  padding: 5px 5%;
  /* position: fixed; */
  top: 0;
  width: 100%;
  background-color: rgba(139, 138, 135, 0.85);
  display: flex;
  align-items: center;
  height: 60px;
  /* position: fixed; */
}
.doboku_icon {
  position: relative;
  top: -10px;
  margin-right: 8px;
}

.title {
  text-decoration: none;
  color: black;
  margin: 0;
  padding: 0;
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

<script>
import HeaderSide from "../components/HeaderSide";
export default {
  components: {
    HeaderSide
  }
};
</script>
