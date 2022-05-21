<template>
  <div class="page-wrap">
    <!-- Sales Value Chart -->
    <section class="section-space">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Sales Value`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_value', 'Sales Value (NMR)', false)"
                    class="numerai-chart"></StatsChart>
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
    <!-- Sales Quantity Chart -->
    <section class="section-space bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading :content="`By tournament round`" :text="`Sales Quantity`"
                        classname="text-center" isMargin="mb-3"></SectionHeading>
        <StatsChart :chartdata="getStatsChartData(stats, 'sales_quantity', 'Sales Quantity', false)"
                    class="numerai-chart"></StatsChart>
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
  </div><!-- end page-wrap -->
</template>

<script>
import StatsChart from '@/components/section/StatsChart';

// Composables
import {onSSR} from '@vue-storefront/core';
import {
  useStats
} from '@vue-storefront/numerbay';

export default {
  name: 'Stats',
  components: {
    StatsChart
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
