module.exports = {
  pages: {
    index: {
      entry: 'src/main.js', // 必須パラメータ
      title: 'ページタイトル',
    }
  },
  // publicPath: process.env.NODE_ENV === 'production'
  publicPath: '/dist',
  // productionSourceMap: false,

}
