import moment from "moment";
export default {
  data() {
    return {
      periods: [{
          name: "3日前",
          date: moment().subtract(3, "days").format("YYYY-MM-DD"),
        },
        {
          name: "1週間前",
          date: moment().subtract(1, "weeks").format("YYYY-MM-DD"),
        },
        {
          name: "1ヶ月前",
          date: moment().subtract(1, "months").format("YYYY-MM-DD"),
        },
      ],
    }
  }
}
