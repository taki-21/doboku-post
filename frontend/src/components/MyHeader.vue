<template>
    <div>
      <header class="title-header" uk-sticky>
        <div>
          <a class="title">
            <img class="doboku_icon" src="../../../media/doboku.png" width="40" height="40" /><span>DOBOKU_Post</span>
          </a>
        </div>
        <nav>
          <HeaderSide />
        </nav>
      </header>
    </div>
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

.title {
  text-decoration: none;
  color: black;
  margin: 0;
  padding: 0;
}
.title span{
  font-size: 40px;
  font-family: "Economica";

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
