import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/services/api'
import moment from "moment";

import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

// 認証情報
const authModule = {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state: {
    username: '',
    isLoggedIn: false,
    id: '',
  },
  getters: {
    username: state => state.username,
    isLoggedIn: state => state.isLoggedIn,
    id: state => state.id,

  },
  mutations: {
    set(state, payload) {
      state.username = payload.user.username
      state.isLoggedIn = true
      state.id = payload.user.id
    },
    clear(state) {
      state.username = ''
      state.isLoggedIn = false
      state.id = false
    }
  },
  actions: {
    /**
     * ログイン
     */
    login(context, payload) {
      return api.post('/auth/jwt/create/', {
          'username': payload.username,
          'password': payload.password
        })
        .then(response => {
          // 認証用トークンをlocalStorageに保存
          localStorage.setItem('access', response.data.access)
          // ユーザー情報を取得してstoreのユーザー情報を更新
          return context.dispatch('reload')
            .then(user => user)
        })
        .catch(error => {
          console.log('ログインえらー！！！！')
          console.log(error)
        })
    },
    /**
     * ログアウト
     */
    logout(context) {
      // 認証用トークンをlocalStorageから削除
      localStorage.removeItem('access')
      // storeのユーザー情報をクリア
      context.commit('clear')
    },
    /**
     * ユーザー情報更新
     */
    reload(context) {
      return api.get('/auth/users/me/')
        .then(response => {
          const user = response.data
          // storeのユーザー情報を更新
          context.commit('set', {
            user: user
          })
          console.log('user!!.password' + user.password)
          return user
        })
        .catch(error => {
          console.log('ユーザー情報更新えらー！！')
          console.log(error)
        })
    }
  }
}

// グローバルメッセージ
const messageModule = {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state: {
    error: '',
    warnings: [],
    info: ''
  },
  getters: {
    error: state => state.error,
    warnings: state => state.warnings,
    info: state => state.info
  },
  mutations: {
    set(state, payload) {
      if (payload.error) {
        state.error = payload.error
      }
      if (payload.warnings) {
        state.warnings = payload.warnings
      }
      if (payload.info) {
        state.info = payload.info
      }
    },
    clear(state) {
      state.error = ''
      state.warnings = []
      state.info = ''
    }
  },
  actions: {
    /**
     * エラーメッセージ表示
     */
    setErrorMessage(context, payload) {
      context.commit('clear')
      context.commit('set', {
        'error': payload.message
      })
    },
    /**
     * 警告メッセージ（複数）表示
     */
    setWarningMessages(context, payload) {
      context.commit('clear')
      context.commit('set', {
        'warnings': payload.messages
      })
    },
    /**
     * インフォメーションメッセージ表示
     */
    setInfoMessage(context, payload) {
      context.commit('clear')
      context.commit('set', {
        'info': payload.message
      })
    },
    /**
     * 全メッセージ削除
     */
    clearMessages(context) {
      context.commit('clear')
    }
  }
}

///////////////
//  投稿情報  //
//////////////
const postModule = {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state: {
    posts: [],
    // 検索パラメーター
    filterQuery: {}
  },
  getters: {
    latestPosts: function (state) {
      return state.posts
    },
    popularPosts: function (state) {
      return state.posts.slice().sort(function (a, b) {
        return a.like_count < b.like_count ?
          1 :
          a.like_count > b.like_count ?
          -1 :
          0;
      });
    },
    filteredPosts(state) {
      let data = state.posts;

      // タイトルの検索
      if (state.filterQuery.title !== "") {
        data = data.filter(function (row) {
          return row['title'].indexOf(state.filterQuery.title) !== -1;
        });
      }

      // カテゴリの検索
      if (state.filterQuery.category !== '') {
        data = data.filter(function (row) {
          return row['category'] === state.filterQuery.category
        })
      }

      // 期間の検索
      var now = moment()
      var designatedDate = moment(now).subtract(state.filterQuery.period, 'days').format()
      if (state.filterQuery.period !== '') {
        data = data.filter(function (row) {
          return row['published_at'] > designatedDate
        })
      }

      return data;
    }
  },
  mutations: {
    // 投稿を一括登録
    setPosts(state, posts) {
      state.posts = posts
    },
    // 引数を展開してステートに入れる
    setFilterQuery(state, filterQuery) {
      state.filterQuery = {
        ...filterQuery
      }
    }
  },
  actions: {
    getAllPosts(context) {
      api.get('http://127.0.0.1:8000/api/v1/posts/')
        .then(response => {
          context.commit('setPosts', response.data);
        })
        .catch(error => {
          console.log(error);
        });
    },
  }
}

//////////////////
//  ユーザー情報  //
/////////////////
const userModule = {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state: {
    id: '',
    username: '',
    email: '',
    introduction: '',
    icon_image: '',
    home_image: '',
  },
  getters: {
    id: state => state.id,
    username: state => state.username,
    email: state => state.email,
    introduction: state => state.introduction,
    icon_image: state => state.icon_image,
    home_image: state => state.home_image,
    getUser: state => {
      return {
        id: state.id,
        username: state.username,
        email: state.email,
        introduction: state.introduction,
        icon_image: state.icon_image,
        home_image: state.home_image,
      }
    }
  },
  mutations: {
    set(state, payload) {
      state.id = payload.user.id
      state.username = payload.user.username
      state.email = payload.user.email
      state.introduction = payload.user.introduction
      state.icon_image = payload.user.icon_image
      state.home_image = payload.user.home_image
    },
    clear(state) {
      state.id = ''
      state.username = ''
      state.email = ''
      state.introduction = ''
      state.icon_image = ''
      state.home_image = ''
    }
  },
  actions: {
    load(context, payload) {
      return api.get('/users/' + payload.id + '/')
        .catch(error => {
          console.log(error)
        })
        .then(response => {
          console.log('response.data: ' + response.data)
          const user = response.data
          // storeのユーザー情報を更新
          context.commit('set', {
            user: user
          })
          return user
        })
    },
    logout(context) {
      // storeのユーザー情報をクリア
      context.commit('clear')
    }
  }
}




const store = new Vuex.Store({
  modules: {
    auth: authModule,
    message: messageModule,
    user: userModule,
    post: postModule
  },
  plugins: [createPersistedState({
    key: 'example',
    storage: window.sessionStorage
  })]
})

export default store
