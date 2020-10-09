export const watchScrollPosition = {
  watch: {
    loading() {
      this.$nextTick(() => {
        var positionY = sessionStorage.getItem("positionY");
        console.log(positionY);
        scrollTo(0, positionY);
        setTimeout(function () {
          scrollTo(0, positionY);
        });
      });
    },
  }
};

export const clearSession = {
  methods: {
    clearSession() {
      sessionStorage.removeItem('infinitePage_latest')
      sessionStorage.removeItem('infinitePage_popular')
      sessionStorage.removeItem('infinitePage_category')
      sessionStorage.removeItem('infinitePage_search')
      sessionStorage.removeItem('infinitePage_previous')
      sessionStorage.removeItem('infinitePage_liked')
    }
  }
}
