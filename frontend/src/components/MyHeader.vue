<template>
  <header class="title-header" uk-sticky>
    <div id="header-text">
      <a href class="title">
        <img class="doboku_icon" src="../../../media/doboku.png" width="40" height="40" />DOBOKU_Post
      </a>
    </div>
    <nav>
      <HeaderSide />
    </nav>
  </header>
</template>

<style scoped>
.header {
  padding: 0px;
  /* position: fixed; */
  top: 0;
  width: 100%;
  display: flex;
  align-items: center;
}
.doboku_icon {
  position: relative;
  top: -5px;
  margin-right: 8px;
}
#header-text {
  margin: 0;
  padding: 0;
  font-size: 40px;
  font-family: "Economica";
}
#header-text a {
  text-decoration: none;
  color: black;
}

.title-header {
  padding: 10px 4% 10px;
  /* position: fixed; */
  top: 0;
  width: 100%;
  background-color: rgba(90, 84, 75, 0.85);
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}
nav {
    margin: 0 0 0 auto;
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
