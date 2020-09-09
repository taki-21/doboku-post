module.exports = {
  pages: {
    index: {
      entry: 'src/main.js', // 必須パラメータ
      title: 'ページタイトル',
    }
  },
  // outputDir: '../static',
  // indexPath: '../templates/index.html',
  // publicPath: process.env.NODE_ENV === 'production'
  publicPath: '/',
  productionSourceMap: false,

  //   ? '/static/'
  //   : '/'
}
