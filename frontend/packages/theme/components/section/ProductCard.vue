<template>
  <div class="card card-full flex-sm-row product-s2">
    <div class="card-image">
      <img :src="productGetters.getCoverImage(product)" class="product-img" alt="avatar image">
    </div>
    <div class="card-body card-justified p-4">
      <h5 class="card-title text-truncate mb-0">{{ productGetters.getName(product).toUpperCase() }}</h5>
      <div class="card-author d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center">
          <div class="custom-tooltip-wrap">
            <div class="card-author-by-2">
              <span class="item-detail-text-meta">{{ productGetters.getCategory(product).slug }}</span>
              <span class="badge fw-medium bg-success" v-if="product.is_ready"
                    title="Artifact files are available for immediate download/submission">Instant</span>
            </div>
            <a href="javascript:void(0);" class="custom-tooltip author-link"
               v-show="!!productGetters.getCategory(product).is_per_model">Metrics...</a>
            <div class="card-generic custom-tooltip-dropdown">
              <div class="metrics-wrap mb-3">
                <h6 class="mb-1 smaller text-uppercase">Model Metrics</h6>
              </div><!-- end metrics-wrap  -->
              <ModelMetricsCard
                :tournament="productGetters.getCategory(product).tournament"
                :nmr-staked="nmrStaked"
                :stake-info="stakeInfo"
                :latest-returns="latestReturns"
                :latest-reps="latestReps"
                :latest-ranks="latestRanks"
                :show="{fnc: productGetters.getCategory(product).tournament==8, tc: productGetters.getCategory(product).tournament==8, ic: productGetters.getCategory(product).tournament==11}"
              ></ModelMetricsCard>
            </div><!-- end dropdown-menu -->
          </div><!-- end custom-tooltip-wrap -->
        </div>
      </div><!-- end card-author -->
      <div style="vertical-align: bottom">
        <hr>
        <div class="card-price-wrap d-flex align-items-center justify-content-between">
          <div class="me-5 me-sm-2">
            <span class="card-price-title">Price</span>
            <span class="card-price-number">{{
                productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx))
              }}</span>
          </div>
          <span class="btn btn-sm"
                :class="productGetters.getIsActive(product)?'btn-dark':'btn-light disabled'">Buy</span>
        </div><!-- end card-price-wrap -->
      </div>
    </div><!-- end card-body -->
    <router-link
      class="details"
      :to="{
                name: 'ProductDetailsByFullName',
                params: {
                id: product.id,
                category: productGetters.getCategory(product).slug,
                name: productGetters.getName(product),
                slug: productGetters.getSlug(product),
                owner: productGetters.getOwner(product),
                description: productGetters.getDescription(product),
                modelUrl: productGetters.getModelUrl(product),
                nmrStaked: productGetters.getModelNmrStaked(product, 2),
                stakeInfoCorrMultiplier: productGetters.getModelStakeInfo(product, 'corrMultiplier'),
                stakeInfoMmcMultiplier: productGetters.getModelStakeInfo(product, 'mmcMultiplier'),
                stakeInfoTcMultiplier: productGetters.getModelStakeInfo(product, 'tcMultiplier'),
                latestRankCorr: productGetters.getModelRank(product, 'corr'),
                latestRankMmc: productGetters.getModelRank(product, 'mmc'),
                latestRankFnc: productGetters.getModelRank(product, 'fnc'),
                latestRankTc: productGetters.getModelRank(product, 'tc'),
                latestRankIc: productGetters.getModelRank(product, 'ic'),
                latestRepCorr: productGetters.getModelRep(product, 'corr'),
                latestRepMmc: productGetters.getModelRep(product, 'mmc'),
                latestRepFnc: productGetters.getModelRep(product, 'fnc'),
                latestRepFncV3: productGetters.getModelRep(product, 'fncV3'),
                latestRepTc: productGetters.getModelRep(product, 'tc'),
                latestRepIc: productGetters.getModelRep(product, 'ic'),

                title: productGetters.getName(product).toUpperCase(),
                price: productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)),
                priceTwo: productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)),
                imgLg: productGetters.getCoverImage(product),
                }
            }"
    >
    </router-link>
  </div><!-- end card -->
</template>
<script>
import {createPopper} from '@popperjs/core';

// Composables
import {productGetters} from '@vue-storefront/numerbay';

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      default: () => {
      }
    }
  },
  computed: {
    nmrStaked() {
      return this.productGetters.getModelNmrStaked(this.product, 2);
    },
    stakeInfo() {
      return {
        corrMultiplier: this.productGetters.getModelStakeInfo(this.product, 'corrMultiplier') || (this.productGetters.getCategory(this.product).tournament === 8 ? 0 : 2),
        mmcMultiplier: this.productGetters.getModelStakeInfo(this.product, 'mmcMultiplier') || 0,
        tcMultiplier: this.productGetters.getModelStakeInfo(this.product, 'tcMultiplier') || 0
      };
    },
    latestRanks() {
      return {
        corr: this.productGetters.getModelRank(this.product, 'corr'),
        mmc: this.productGetters.getModelRank(this.product, 'mmc'),
        fnc: this.productGetters.getModelRank(this.product, 'fnc'),
        fncV3: this.productGetters.getModelRank(this.product, 'fncV3'),
        tc: this.productGetters.getModelRank(this.product, 'tc'),
        ic: this.productGetters.getModelRank(this.product, 'ic')
      };
    },
    latestReps() {
      return {
        corr: this.productGetters.getModelRep(this.product, 'corr'),
        mmc: this.productGetters.getModelRep(this.product, 'mmc'),
        fnc: this.productGetters.getModelRep(this.product, 'fnc'),
        fncV3: this.productGetters.getModelRep(this.product, 'fncV3'),
        tc: this.productGetters.getModelRep(this.product, 'tc'),
        ic: this.productGetters.getModelRep(this.product, 'ic')
      };
    },
    latestReturns() {
      return {
        oneDay: this.productGetters.getModelReturn(this.product, 'oneDay'),
        threeMonths: this.productGetters.getModelReturn(this.product, 'threeMonths'),
        oneYear: this.productGetters.getModelReturn(this.product, 'oneYear')
      };
    }
  },
  methods: {
    isModelFileProduct(product) {
      return Boolean(productGetters.getCategory(product)) && productGetters.getCategory(product).slug.includes('-models');
    },
    isDataFileProduct(product) {
      return Boolean(productGetters.getCategory(product)) && productGetters.getCategory(product).slug.includes('-data');
    }
  },
  mounted() {

    /* ============= Custom Tooltips =============== */
    function customTooltip(selector, active) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          const parent = item.parentElement;
          const next = item.nextElementSibling;
          createPopper(item, next);
          parent.addEventListener('mouseenter', function () {
            parent.classList.add(active);
          });
          parent.addEventListener('mouseleave', function () {
            parent.classList.remove(active);
          });
        });
      }
    }

    customTooltip('.custom-tooltip', 'active');

  },
  setup() {
    return {
      productGetters
    };
  }
};
</script>

<style lang="css" scoped>
.details {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.author-link {
  z-index: 2;
  position: relative;
}
</style>
