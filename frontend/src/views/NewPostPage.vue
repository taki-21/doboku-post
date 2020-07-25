<template>
  <div>
    <MyHeader />
    <!-- ヘッダー -->

    <div class="uk-width-1-1">
      <div class="uk-container">
        <div class="uk-grid-margin uk-grid-stack">
          <div class="uk-width-1-1@m">
            <div
              class="uk-margin uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large"
            >
              <h2 class="uk-card-title uk-text-center">新規投稿</h2>
              <form @submit.prevent="submitPost()">
                <div uk-grid>
                  <div class="uk-width-1-2">
                    <div uk-form-custom>
                      <div class="uk-placeholder uk-text-center">
                        <div class="preview">
                          <input type="file" @change="selectedFile">
                          <img id="image-preview" />
                        </div>
                        <div class="camera-choice">
                          <div class="camera-icon" uk-icon="icon: camera; ratio: 5"></div>
                          <p>画像を選択してください</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="uk-width-1-2">
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>カテゴリ</label>
                        {{category}}
                        <select
                          class="uk-select"
                          type="text"
                          v-model="category"
                          required
                        >
                          <option
                            v-for="(ctg,key) in categories"
                            :key="key"
                            v-bind:value="ctg.id"
                          >{{ctg.name}}</option>
                        </select>
                      </div>
                    </div>
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>タイトル</label>
                        {{title}}
                        <input
                          class="uk-input"
                          type="text"
                          v-model="title"
                          required
                        />
                      </div>
                    </div>
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>キャプション</label>
                        {{content}}
                        <textarea
                          class="uk-input"
                          type="textarea"
                          v-model="content"
                          required
                        ></textarea>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="uk-margin">
                  <button
                    class="uk-button uk-button-primary uk-button-large uk-width-1-1 post-button"
                    type="submit"
                  >投稿</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MyHeader from "@/components/MyHeader";
export default {
  components: {
    MyHeader
  },
  data() {
    return {
      categories: [],
      category: "",
      author_name: this.$store.getters["auth/id"],
      image: null,
      title: "",
      content: "",
      loading: false
    };
  },
  mounted() {
    this.axios
      .get("http://127.0.0.1:8000/api/v1/categories/")
      .then(response => {
        this.categories = response.data;
      });
  },
  methods: {
    selectedFile(event){
      event.preventDefault();
      this.image = event.target.files[0]

    },
    submitPost: function() {
      const formData = new FormData();
      formData.append("category", this.category);
      formData.append("author_name", this.author_name);
      formData.append("title", this.title);
      formData.append("content", this.content);
      formData.append("image", this.image);
      this.axios
        .post("http://127.0.0.1:8000/api/v1/posts/", formData)
        .then(response => {
          console.log("送信内容: " + response.data);
        })
        .catch(error => {
          console.log("response: ", error.response.data);
        });
    }
  }
};
</script>
