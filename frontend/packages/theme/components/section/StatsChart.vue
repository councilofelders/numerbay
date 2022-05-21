<script>
import {Line} from 'vue-chartjs';

export default {
  name: 'StatsChart',
  extends: Line,
  props: {
    height: {
      type: Number,
      default: 360
    },
    chartdata: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            ticks: {
              maxTicksLimit: 20
            }
          }],
          yAxes: [{
            ticks: {
              suggestedMin: 0
            }
          }]
        },
        tooltips: {
          callbacks: {
            title(tooltipItem, data) {
              return data.labels[tooltipItem[0].index];
            },
            label(tooltipItem, data) {
              let label = data.datasets[tooltipItem.datasetIndex].label || '';

              if (label) {
                label += ': ';
              }
              label += Math.round(tooltipItem.yLabel * 1000) / 1000;
              return label;
            },
          }
        }
      })
    }
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  }
};
</script>
<style lang="scss" scoped>
.dark-mode {
  canvas {
    filter: invert(1) brightness(150%) hue-rotate(180deg);
  }
}
</style>
