
<script>
import { Line } from 'vue-chartjs';

export default {
  name: 'NumeraiChart',
  extends: Line,
  props: {
    height: {
      type: Number,
      default: 300
    },
    chartdata: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: () => ({responsive: true, maintainAspectRatio: false})
    }
  },
  mounted () {
    this.renderChart(this.chartdata, this.options);
  }
};
</script>
<style lang="scss" scoped>
</style>
