<template>
  <div>
    <!-- ヘッダー -->
    <MyHeader/>
    <!-- <GlobalMessage/> -->


    <!-- メインエリア -->
    <div class="content">
      <PostList/>
    </div>
  </div>
</template>

<script>
// import GlobalMessage from "@/components/GlobalMessage.vue";
import MyHeader from "@/components/MyHeader";
import PostList from "@/components/PostList";

export default {
  components: {
    // GlobalMessage,
    MyHeader,
    PostList
  },
};
</script>

<style scoped>

.content {
  margin: 10px 30px;
}

</style>
