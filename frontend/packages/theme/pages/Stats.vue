<template>
  <div class="page-wrap">
    <!-- Total Sales Value Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Total Sales Value`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_value', 'Sales Value (NMR)', false)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
    <!-- Sales Value by Tournament Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Sales Value by Tournament`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsStackedChart :chartdata="getStatsStackedChartData(stats, ['sales_value_numerai', 'sales_value_signals'], ['Numerai (NMR)', 'Signals (NMR)'], false)"
                    class="numerai-chart"></StatsStackedChart>
      </div><!-- end container -->
    </section>
    <!-- Cumulative Sales Value Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Cumulative Sales Value`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_value', 'Cumulative Sales Value (NMR)', true)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
    <!-- Cumulative Sales Value by Tournament Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Cumulative Sales Value by Tournament`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsStackedChart :chartdata="getStatsStackedChartData(stats, ['sales_value_numerai', 'sales_value_signals'], ['Numerai (NMR)', 'Signals (NMR)'], true)"
                    class="numerai-chart"></StatsStackedChart>
      </div><!-- end container -->
    </section>
    <!-- Total Sales Quantity Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Total Sales Quantity`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_quantity', 'Sales Quantity', false)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
    <!-- Sales Quantity by Tournament Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Sales Quantity by Tournament`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsStackedChart :chartdata="getStatsStackedChartData(stats, ['sales_quantity_numerai', 'sales_quantity_signals'], ['Numerai (NMR)', 'Signals (NMR)'], false)"
                    class="numerai-chart"></StatsStackedChart>
      </div><!-- end container -->
    </section>
    <!-- Cumulative Sales Quantity Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Cumulative Sales Quantity`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_quantity', 'Cumulative Sales Quantity', true)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
    <!-- Cumulative Sales Quantity by Tournament Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Cumulative Sales Quantity by Tournament`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsStackedChart :chartdata="getStatsStackedChartData(stats, ['sales_quantity_numerai', 'sales_quantity_signals'], ['Numerai (NMR)', 'Signals (NMR)'], true)"
                    class="numerai-chart"></StatsStackedChart>
      </div><!-- end container -->
    </section>
    <!-- Total Unique Models Sold Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Total Unique Models Sold`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'unique_models_sold', 'Unique Models', false)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
    <!-- Unique Models Sold by Tournament Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Unique Models Sold by Tournament`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsStackedChart :chartdata="getStatsStackedChartData(stats, ['unique_models_sold_numerai', 'unique_models_sold_signals'], ['Numerai', 'Signals'], false)"
                    class="numerai-chart"></StatsStackedChart>
      </div><!-- end container -->
    </section>
    <!-- Unique Buyers Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Unique Buyers`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'unique_buyers', 'Unique Buyers', false)"
                    class="numerai-chart"></StatsChart>
      </div><!-- end container -->
    </section>
  </div><!-- end page-wrap -->
</template>

<script>
import StatsChart from '@/components/section/StatsChart';
import StatsStackedChart from '@/components/section/StatsStackedChart';

// Composables
import {onSSR} from '@vue-storefront/core';
import {
  useStats
} from '@vue-storefront/numerbay';

export default {
  name: 'Stats',
  components: {
    StatsChart,
    StatsStackedChart
  },
  methods: {
    getStatsChartData: (stats, metric, title, cumulative) => {
      if (!stats?.stats) {
        return {};
      }

      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      const transposed = Object.assign(...Object.keys(stats?.stats[metric][0]).map(
        key => ({[key]: stats?.stats[metric].map(o => o[key])})
      ));

      return {
        labels: transposed.round_tournament,
        datasets: [
          {
            label: title,
            borderColor: '#666666',
            fill: false,
            lineTension: 0,
            data: cumulative ? transposed.value.map((sum => value => sum += value)(0)) : transposed.value,
          },
        ]
      };
    },
    getStatsStackedChartData: (stats, metrics, titles, cumulative) => {
      if (!stats?.stats) {
        return {};
      }

      const colors = ['#46cc1d', '#e61dfa', '#c3a25e', '#fb772a'];
      let datasets = [];
      let round_tournament;

      for (var i in metrics) {
        const metric = metrics[i];
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        const transposed = Object.assign(...Object.keys(stats?.stats[metric][0]).map(
          key => ({[key]: stats?.stats[metric].map(o => o[key])})
        ));

        datasets.push({
          label: titles[i],
          backgroundColor: colors[i],
          fill: false,
          lineTension: 0,
          data: cumulative ? transposed.value.map((sum => value => sum += value)(0)) : transposed.value,
        });

        round_tournament = transposed.round_tournament;
      }

      return {
        labels: round_tournament,
        datasets: datasets
      };
    }
  },
  setup(props, context) {
    const {stats, getStats, loading: statsLoading} = useStats();

    onSSR(async () => {
      await getStats();
    });

    return {
      stats
    };
  }
};
</script>

<style lang="css" scoped>
</style>
