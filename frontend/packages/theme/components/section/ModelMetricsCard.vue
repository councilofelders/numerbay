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
                All Time Stake Return
              </td>
              <td :class="`stats text-${getMetricColor(latestReturns.allTime)}`">{{ latestReturns.allTime }}%</td>
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
      <div class="col-xl-12" v-if="tournament===8">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR20V2 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'canon_corr')  }}</td>
            </tr>
            <tr>
              <td>
                CORJ60 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'corj60') }}</td>
            </tr>
            <tr>
              <td>
                FNCV3 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'fnc_v3') }}</td>
            </tr>
            <tr>
              <td>
                MMC Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'canon_mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12" v-if="tournament===11">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                FNCV4 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'fnc_v4') }}</td>
            </tr>
            <tr>
              <td>
                CORRV4 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'corr_v4') }}</td>
            </tr>
            <tr>
              <td>
                ICV2 Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'ic_v2') }}</td>
            </tr>
            <tr>
              <td>
                RIC Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'ric') }}</td>
            </tr>
            <tr>
              <td>
                MMC Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12" v-if="tournament===12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'canon_corr')  }}</td>
            </tr>
            <tr>
              <td>
                MMC Reputation
              </td>
              <td class="stats">{{ formatReputation(latestReps, 'canon_mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12" v-if="tournament===8">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR20V2 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'canon_corr') }}</td>
            </tr>
            <tr>
              <td>
                CORJ60 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'corj60') }}</td>
            </tr>
            <tr>
              <td>
                FNCV3 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'fnc_v3') }}</td>
            </tr>
            <tr>
              <td>
                MMC Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'canon_mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12" v-if="tournament===11">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                FNCV4 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'fnc_v4') }}</td>
            </tr>
            <tr>
              <td>
                CORRV4 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'corr_v4') }}</td>
            </tr>
            <tr>
              <td>
                ICV2 Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'ic_v2') }}</td>
            </tr>
            <tr>
              <td>
                RIC Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'ric') }}</td>
            </tr>
            <tr>
              <td>
                MMC Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-xl-12" v-if="tournament===12">
        <div class="card-media card-media-s1">
          <table class="table mb-0 table-s1 item-detail-metrics-table">
            <tbody>
            <tr>
              <td>
                CORR Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'canon_corr') }}</td>
            </tr>
            <tr>
              <td>
                MMC Rank
              </td>
              <td class="stats">{{ formatRank(latestRanks, 'canon_mmc') }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
<!--      <div class="col-xl-12">
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
      </div>-->
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
    }
  },
  methods: {
    formatReputation(metrics, key) {
      if (!metrics || metrics.hasOwnProperty(key) === false) {
        return '-';
      }

      return metrics[key].toFixed(4);
    },
    formatRank(metrics, key) {
      if (!metrics || metrics.hasOwnProperty(key) === false) {
        return '-';
      }

      return metrics[key];
    },
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
