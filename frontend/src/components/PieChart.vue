<script>
import { Pie } from "vue-chartjs";
export default {
  name: "PieChart",
  extends: Pie,
  props: ["data", "options"],
  mounted: function () {
    this.renderChart(this.data, this.options);
  },
  watch: {
    data() {
      this.renderChart(this.data, this.options);
    },
    options() {
      this.renderChart(this.data, this.options);
    },
    $route() {
      this.renderChart(this.data, this.options);
    },
  },
};
</script>
