<template>
  <div class="item-metrics">
    <div class="row g-2">
      <div class="col-xl-12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                1 Day Stake Return
              </td>
              <td :class="`stats text-${getMetricColor(latestReturns.oneDay)}`">{{ latestReturns.oneDay }}%</td>
            </tr>
            <tr>
              <td>
                3 Month Stake Return
              </td>
              <td :class="`stats text-${getMetricColor(latestReturns.threeMonths)}`">{{
                  latestReturns.threeMonths
                }}%
              </td>
            </tr>
            <tr>
              <td>
                1 Year Stake Return
              </td>
              <td :class="`stats text-${getMetricColor(latestReturns.oneYear)}`">{{ latestReturns.oneYear }}%</td>
            </tr>
            <tr>
              <td>
                NMR Stake
              </td>
              <td class="stats">{{ nmrStaked }} NMR</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR Reputation
              </td>
              <td class="stats">{{ latestReps.corr }}</td>
            </tr>
            <tr>
              <td>
                CORR60 Reputation
              </td>
              <td class="stats">{{ latestReps.corr60 }}</td>
            </tr>
            <tr v-if="show.fnc">
              <td>
                FNC Reputation
              </td>
              <td class="stats">{{ latestReps.fnc }}</td>
            </tr>
            <tr v-if="show.fnc">
              <td>
                FNCv3 Reputation
              </td>
              <td class="stats">{{ latestReps.fncV3 }}</td>
            </tr>
            <tr v-if="show.ic">
              <td>
                IC Reputation
              </td>
              <td class="stats">{{ latestReps.ic }}</td>
            </tr>
            <tr v-if="show.tc">
              <td>
                TC Reputation
              </td>
              <td class="stats">{{ latestReps.tc }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR Rank
              </td>
              <td class="stats">{{ latestRanks.corr }}</td>
            </tr>
            <tr>
              <td>
                CORR60 Rank
              </td>
              <td class="stats">{{ latestRanks.corr60 }}</td>
            </tr>
            <tr v-if="show.fnc">
              <td>
                FNC Rank
              </td>
              <td class="stats">{{ latestRanks.fnc }}</td>
            </tr>
            <tr v-if="show.fnc">
              <td>
                FNCv3 Rank
              </td>
              <td class="stats">{{ latestRanks.fncV3 }}</td>
            </tr>
            <tr v-if="show.ic">
              <td>
                IC Rank
              </td>
              <td class="stats">{{ latestRanks.ic }}</td>
            </tr>
            <tr v-if="show.tc">
              <td>
                TC Rank
              </td>
              <td class="stats">{{ latestRanks.tc }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                Payout Multipliers
              </td>
              <td :class="[stakeInfo.tcMultiplier ? 'colortc':'']" class="stats">
                <span v-if="stakeInfo.corrMultiplier"> {{ stakeInfo.corrMultiplier }}xCORR</span>
                <span v-if="stakeInfo.tcMultiplier"> {{ stakeInfo.tcMultiplier }}xTC</span>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div><!-- end row -->
</template>
<script>
export default {
  name: 'ModelMetricsCard',
  props: {
    tournament: {
      type: Number,
      default: 8
    },
    nmrStaked: {
      type: String,
      default: '0'
    },
    stakeInfo: {
      type: Object,
      default: () => {
      }
    },
    latestReturns: {
      type: Object,
      default: () => {
      }
    },
    latestReps: {
      type: Object,
      default: () => {
      }
    },
    latestRanks: {
      type: Object,
      default: () => {
      }
    },
    show: {
      type: Object,
      default: () => ({
        fnc: true,
        tc: true,
        ic: false
      })
    }
  },
  methods: {
    getMetricColor(value) {
      if (value > 0) {
        return 'success';
      } else if (value < 0) {
        return 'danger';
      } else {
        return 'secondary';
      }
    }
  }
};
</script>

<style lang="css" scoped>
.colortc {
  color: #a278dc;
}
</style>
