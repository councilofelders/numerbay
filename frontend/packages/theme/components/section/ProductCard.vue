<template>
    <div class="card card-full flex-sm-row product-s2">
        <div class="card-image">
            <img :src="productGetters.getCoverImage(product)" class="product-img" alt="avatar image">
        </div>
        <div class="card-body card-justified p-4">
            <h5 class="card-title text-truncate mb-0">{{ productGetters.getName(product).toUpperCase() }}</h5>
<!--            <div class="card-author mb-1 d-flex align-items-center">
                <span class="me-1 card-author-by">By</span>
                <div class="custom-tooltip-wrap">
                    <router-link to="item-details" class="custom-tooltip author-link">{{ productGetters.getOwner(product).toUpperCase() }}</router-link>
                    <div class="card-generic custom-tooltip-dropdown">
                        <div class="author-action d-flex flex-wrap align-items-center mb-3">
                            <div class="flex-shrink-0 avatar">
                                <img :src="product.avatar" alt="avatar">
                            </div>
                            <div class="ms-2">
                                <span class="author-username">{{ productGetters.getOwner(product).toUpperCase() }}</span>
                                <span class="author-follow-text">{{ product.followersText }}</span>
                            </div>
                        </div>
                        <h6 class="author-name mb-1">{{ productGetters.getOwner(product).toUpperCase() }}</h6>
                        <p class="author-desc smaller mb-3">{{ product.desc }}</p>
                        <div class="follow-wrap mb-3">
                            <h6 class="mb-1 smaller text-uppercase">Followed by</h6>
                            <div class="avatar-group">
                                <router-link :to="avatar.path" v-for="avatar in product.avatars" :key="avatar.id">
                                    <img :src="avatar.img" alt="avatar">
                                </router-link>
                            </div>
                        </div>&lt;!&ndash; end follow-wrap  &ndash;&gt;
                        <router-link to="item-details" class="btn btn-sm bg-dark-dim">Follow</router-link>
                    </div>&lt;!&ndash; end dropdown-menu &ndash;&gt;
                </div>&lt;!&ndash; end custom-tooltip-wrap &ndash;&gt;
            </div>&lt;!&ndash; end card-author &ndash;&gt;-->

            <div class="card-author d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center">
                    <div class="custom-tooltip-wrap">
                        <div class="card-author-by-2">
                          <span class="item-detail-text-meta">{{ productGetters.getCategory(product).slug }}</span>
                          <span class="badge fw-medium bg-success" v-if="product.is_ready" title="Artifact files are available for immediate download/submission">Instant</span>
                        </div>
<!--                        <span class="card-author-by card-author-by-2 fw-regular">Owned by</span>-->
                        <a href="javascript:void(0);" class="custom-tooltip author-link" v-show="!!productGetters.getCategory(product).tournament">Metrics...</a>
                        <div class="card-generic custom-tooltip-dropdown">
<!--                            <div class="author-action d-flex flex-wrap align-items-center mb-3">
                                <div class="flex-shrink-0 avatar">
                                    <img :src="product.avatar" alt="avatar">
                                </div>
                                <div class="ms-2">
                                    <span class="author-username">{{ product.userName }}</span>
                                    <span class="author-follow-text">{{ product.followersText }}</span>
                                </div>
                            </div>
                            <h6 class="author-name mb-1">{{ product.authorName }}</h6>
                            <p class="author-desc smaller mb-3">{{ product.desc }}</p>
                            <div class="follow-wrap mb-3">
                                <h6 class="mb-1 smaller text-uppercase">Followed by</h6>
                            </div>&lt;!&ndash; end follow-wrap  &ndash;&gt;
                            <router-link :to="product.authorLink" class="btn btn-sm bg-dark-dim">Follow</router-link>-->

                            <div class="metrics-wrap mb-3">
                                <h6 class="mb-1 smaller text-uppercase">Model Metrics</h6>
                            </div><!-- end metrics-wrap  -->
                            <ModelMetricsCard
                              :nmr-staked="nmrStaked"
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
                    <span class="card-price-number">{{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)) }}</span>
                </div>
                <span class="btn btn-sm" :class="productGetters.getIsActive(product)?'btn-dark':'btn-light disabled'">Buy</span>
            </div><!-- end card-price-wrap -->
            </div>

<!--            <div class="card-price-wrap d-flex align-items-center justify-content-sm-between mb-3">
                <div class="me-5 me-sm-2">
                    <span class="card-price-title">Price</span>
                    <span class="card-price-number">{{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)) }}</span>
                </div>
                <div class="text-sm-end">
                    <span class="card-price-title">Current bid</span>
                    <span class="card-price-number">NMR</span>
                </div>
            </div>&lt;!&ndash; end card-price-wrap &ndash;&gt;
            <router-link to="item-details" class="btn btn-sm btn-dark">Buy</router-link>-->
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
                metaText: product.metaText,
                price: productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)),
                priceTwo: productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)),
                imgLg: productGetters.getCoverImage(product),
                metaText: product.metaText,
                metaTextTwo: product.metaTextTwo,
                metaTextThree: product.metaTextThree,
                content: product.content,
                }
            }"
        >
        </router-link>
    </div><!-- end card -->
</template>
<script>
import { createPopper } from '@popperjs/core';

// Composables
import { productGetters } from '@vue-storefront/numerbay';

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      default: () =>{}
    }
  },
  computed: {
    nmrStaked() {
      return this.productGetters.getModelNmrStaked(this.product, 2);
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
  mounted () {

    /* ============= Custom Tooltips =============== */
    function customTooltip(selector, active) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          const parent = item.parentElement;
          const next = item.nextElementSibling;
          createPopper(item, next);
          parent.addEventListener('mouseenter', function() {
            parent.classList.add(active);
          });
          parent.addEventListener('mouseleave', function() {
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
