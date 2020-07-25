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
              <form @submit.prevent='submitPost'>
                <div uk-grid>
                  <div class="uk-width-1-2">
                    <div uk-form-custom>
                      <div class="uk-placeholder uk-text-center">
                        <div class="preview">
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
                        <input class="uk-input" type="text" v-model='category' required />
                      </div>
                    </div>
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>タイトル</label>
                        {{title}}
                        <input class="uk-input" type="text" v-model='title' required />
                      </div>
                    </div>
                    <div class="uk-margin">
                      <div class="uk-inline uk-width-1-1">
                        <label>キャプション</label>
                        <input class="uk-input" type="textarea" required />
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
import MyHeader from "@/components/MyHeader"
export default {
  components: {
    MyHeader
  },
  data(){
    return{
      author: "",
      form:{
        image: "",
        category: "",
        title: "",
        caption:"",
      },
      loading: false,
    }
  },
  methods: {
    submitPost:function(){
      this.loading = true;
      this.axios.post('http://127.0.0.1:8000/api/v1/posts/')

    }
  }
}
</script>
