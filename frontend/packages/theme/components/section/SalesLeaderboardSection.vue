<template>
  <section class="ranking-section section-space-b">
    <div class="container">
      <ul class="nav nav-tabs nav-tabs-s3 mb-2" id="myTab" role="tablist">
        <li class="nav-item" role="presentation" v-for="list in leaderboardTabs" :key="list.id">
          <button class="nav-link" :class="list.isActive" :id="list.slug" data-bs-toggle="tab"
                  :data-bs-target="list.bsTarget" type="button">{{ list.title }}
          </button>
        </li>
      </ul>
      <div id="leaderboardTabContent" class="tab-content mt-4">
        <div id="numerai-predictions" aria-labelledby="numerai-predictions-tab" class="tab-pane fade show active"
             role="tabpanel">
          <div class="table-responsive">
            <table class="table mb-0 table-s1">
              <thead>
              <tr>
                <th scope="col" v-for="item in leaderboardHeaders" :key="item.id">{{ item }}</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(product, i) of numeraiPredictionsLeaderboard" :key="productGetters.getId(product)">
                <th scope="row">
                  <router-link :to="`/product/numerai-predictions/${productGetters.getName(product)}`"
                               class="d-flex align-items-center text-black">
                    <span class="me-2 fs-13">{{ i + 1 }}</span>
                    <div class="avatar me-2">
                      <img :src="product.avatar" alt="">
                    </div>
                    <span>{{ product.name }}</span>
                  </router-link>
                </th>
                <td>{{ productGetters.getQtySales(product) }}</td>
                <td>{{ productGetters.getLastPrice(product) }}</td>
                <td>{{ productGetters.getLastPriceDelta(product) }}</td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'oneDay'))}`">
                  {{ productGetters.getModelReturn(product, 'oneDay') }}%
                </td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'threeMonths'))}`">
                  {{ productGetters.getModelReturn(product, 'threeMonths') }}%
                </td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'oneYear'))}`">
                  {{ productGetters.getModelReturn(product, 'oneYear') }}%
                </td>
              </tr>

              </tbody>
            </table>
          </div><!-- end table-responsive -->
          <button :disabled="numeraiPredictionsLeaderboardLoading || signalsPredictionsLeaderboardLoading"
                  class="btn btn-dark d-flex justify-content-center mx-auto mt-4" type="button"
                  v-if="!showAll" @click="handleLoadAll"
          >
            Load All
          </button>
        </div>
        <div id="signals-predictions" aria-labelledby="signals-predictions-tab" class="tab-pane fade" role="tabpanel">
          <div class="table-responsive">
            <table class="table mb-0 table-s1">
              <thead>
              <tr>
                <th scope="col" v-for="item in leaderboardHeaders" :key="item.id">{{ item }}</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(product, i) of signalsPredictionsLeaderboard" :key="productGetters.getId(product)">
                <th scope="row">
                  <router-link :to="`/product/signals-predictions/${productGetters.getName(product)}`"
                               class="d-flex align-items-center text-black">
                    <span class="me-2 fs-13">{{ i + 1 }}</span>
                    <div class="avatar me-2">
                      <img :src="product.avatar" alt="">
                    </div>
                    <span>{{ product.name }}</span>
                  </router-link>
                </th>
                <td>{{ productGetters.getQtySales(product) }}</td>
                <td>{{ productGetters.getLastPrice(product) }}</td>
                <td>{{ productGetters.getLastPriceDelta(product) }}</td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'oneDay'))}`">
                  {{ productGetters.getModelReturn(product, 'oneDay') }}%
                </td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'threeMonths'))}`">
                  {{ productGetters.getModelReturn(product, 'threeMonths') }}%
                </td>
                <td :class="`text-${getMetricColor(productGetters.getModelReturn(product, 'oneYear'))}`">
                  {{ productGetters.getModelReturn(product, 'oneYear') }}%
                </td>
              </tr>

              </tbody>
            </table>
          </div><!-- end table-responsive -->
          <button :disabled="numeraiPredictionsLeaderboardLoading || signalsPredictionsLeaderboardLoading"
                  class="btn btn-dark d-flex justify-content-center mx-auto mt-4" type="button"
                  v-if="!showAll" @click="handleLoadAll"
          >
            Load All
          </button>
        </div>
      </div>
    </div><!-- .container -->
  </section><!-- end ranking-section -->
</template>

<script>
// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {
  productGetters,
  useProduct
} from '@vue-storefront/numerbay';

export default {
  name: 'SalesLeaderboardSection',
  data() {
    return {
      showAll: false,
      leaderboardTabs: [
        {
          id: 1,
          isActive: 'active',
          title: 'Numerai Predictions',
          slug: 'numerai-predictions-tab',
          bsTarget: '#numerai-predictions'
        },
        {
          id: 2,
          title: 'Signals Predictions',
          slug: 'signals-predictions-tab',
          bsTarget: '#signals-predictions'
        }
      ],
      leaderboardHeaders: [
        'Product',
        'Sales Quantity',
        'Last Price (NMR)',
        'Price Delta (NMR)',
        '1D %',
        '3M %',
        '1Y %',
      ]
    }
  },
  methods: {
    getMetricColor(value) {
      if (value > 0) {
        return 'success';
      } else if (value < 0) {
        return 'danger';
      } else {
        return '';
      }
    },
    async handleLoadAll() {
      await this.getNumeraiPredictionsSalesLeaderboard({categorySlug: 'numerai-predictions'});
      await this.getSignalsPredictionsSalesLeaderboard({categorySlug: 'signals-predictions'});
      this.showAll = true;
    }
  },
  setup(props, context) {
    const {
      products: numeraiPredictionsLeaderboard,
      getSalesLeaderboard: getNumeraiPredictionsSalesLeaderboard,
      loading: numeraiPredictionsLeaderboardLoading
    } = useProduct('sales-leaderboard-numerai-predictions');
    const {
      products: signalsPredictionsLeaderboard,
      getSalesLeaderboard: getSignalsPredictionsSalesLeaderboard,
      loading: signalsPredictionsLeaderboardLoading
    } = useProduct('sales-leaderboard-signals-predictions');

    const limit = 50;
    onSSR(async () => {
      await getNumeraiPredictionsSalesLeaderboard({categorySlug: 'numerai-predictions', limit: limit});
      await getSignalsPredictionsSalesLeaderboard({categorySlug: 'signals-predictions', limit: limit});
    });

    return {
      numeraiPredictionsLeaderboard: computed(() => numeraiPredictionsLeaderboard?.value?.data ? numeraiPredictionsLeaderboard.value?.data : []),
      signalsPredictionsLeaderboard: computed(() => signalsPredictionsLeaderboard?.value?.data ? signalsPredictionsLeaderboard.value?.data : []),
      numeraiPredictionsLeaderboardLoading,
      signalsPredictionsLeaderboardLoading,
      getNumeraiPredictionsSalesLeaderboard,
      getSignalsPredictionsSalesLeaderboard,
      productGetters
    }
  }
}
</script>
