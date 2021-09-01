<template>
  <div id="product">
    <!--<SfBreadcrumbs
      class="breadcrumbs desktop-only"
      :breadcrumbs="breadcrumbs"
    />-->
    <SfLoader :class="{ productLoading }" :loading="productLoading">
    <div class="product" v-if="!productLoading">
      <div class="product__info_full">
        <div class="product__header">
          <SfHeading
            :title="productGetters.getName(product)"
            :level="1"
            class="sf-heading--no-underline sf-heading--left"
          />
          <SfIcon
            icon="drag"
            size="xxl"
            color="var(--c-text-disabled)"
            class="product__drag-icon smartphone-only"
          />
        </div>
        <div class="product__subheader">
          <div class="sf-heading__title h5 sf-heading--no-underline sf-heading--left">
            Round: <span class="product__subheader__highlight" v-if="!!numerai.modelInfo">{{ numerai.modelInfo.rounds[0].number }}</span>
            <span class='divider-pipe'>|</span>
            Seller: <span class="product__subheader__highlight">{{ product.owner.username.toUpperCase() }}</span>
            <span class='divider-pipe'>|</span>
            Type: <span class="product__subheader__highlight">{{ product.category.slug.toUpperCase() }}</span>
            <span class='divider-pipe'>|</span> Platform: <SfBadge class="color-warning sf-badge third-party-badge" v-if="!!product.third_party_url">3rd Party</SfBadge>
            <span class="product__subheader__highlight">{{ resolveProductPlatform(product) }}</span>
          </div>
        </div>
        <div class="product__pricing">
          <div class="last-sale">
            <h3>Last Sale</h3>
            <div class="sale-value">$-</div>
            <p class="last-sale-change" style="color: green;">$0 (0%)</p>
          </div>
          <BuyButton
            :disabled="!product.third_party_url && !product.is_on_platform"
            :price="productGetters.getFormattedPrice(product, withCurrency=false, decimals=product.is_on_platform?4:2)"
            :label="product.is_on_platform ? 'NMR' : 'Ref Price'"
            @click="handleBuyButtonClick(product)"
          />
        </div>
        <SfLoader :class="{ loader: !numerai.modelInfo }" :loading="!numerai.modelInfo">
          <NumeraiChart class="numerai-chart" v-if="!productLoading && !numeraiLoading" :chartdata="!numerai.modelInfo?{}:numeraiChartData"></NumeraiChart>
        </SfLoader>
        <SfLoader :class="{ loader: !numerai.modelInfo }" :loading="!numerai.modelInfo">
        <div class="product__details" v-if="!!numerai.modelInfo">
          <span><h4>OWNER STAKE</h4><p>{{ Number(numerai.modelInfo.nmrStaked).toFixed(2) }} NMR</p></span>
          <span><h4>RANK</h4><p>{{ numerai.modelInfo.modelPerformance.latestRanks.corr }}</p></span>
          <span><h4>REPUTATION</h4><p>{{ Number(numerai.modelInfo.modelPerformance.latestReps.corr).toFixed(4) }}</p></span>
          <span><h4>3 MTH. RETURN</h4><p :class="`delta-${Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths)>0?'positive':'negative'}`">
            {{ numerai.modelInfo.modelPerformance.latestReturns.threeMonths?Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths).toFixed(2):'-' }}%</p></span>
          <span><h4>WOKE</h4><p>{{ numerai.modelInfo.startDate.split('T')[0] }}</p></span>
        </div>
        </SfLoader>
        <LazyHydrate when-idle>
          <SfTabs :open-tab="1" class="product__tabs">
            <SfTab title="Description">
              <div class="product__description" v-html="productGetters.getDescription(product)">
              </div>
              <!--<SfProperty
                v-for="(property, i) in properties"
                :key="i"
                :name="property.name"
                :value="property.value"
                class="product__property"
              >
                <template v-if="property.name === 'Category'" #value>
                  <SfButton class="product__property__button sf-button&#45;&#45;text">
                    {{ property.value }}
                  </SfButton>
                </template>
              </SfProperty>-->
            </SfTab>
          </SfTabs>
        </LazyHydrate>
      </div>
    </div>
    </SfLoader>
  </div>
</template>
<script>
import {
  SfProperty,
  SfHeading,
  SfPrice,
  SfRating,
  SfSelect,
  SfAddToCart,
  SfTabs,
  SfGallery,
  SfIcon,
  SfImage,
  SfBanner,
  SfAlert,
  SfSticky,
  SfReview,
  SfBreadcrumbs,
  SfButton,
  SfColor,
  SfBadge,
  SfLoader
} from '@storefront-ui/vue';

import InstagramFeed from '~/components/InstagramFeed.vue';
import RelatedProducts from '~/components/RelatedProducts.vue';
import { ref, computed } from '@vue/composition-api';
import {useProduct, productGetters, reviewGetters, useNumerai, useUser} from '@vue-storefront/numerbay';
import { useUiState } from '~/composables';
import { onSSR } from '@vue-storefront/core';
import MobileStoreBanner from '~/components/MobileStoreBanner.vue';
import LazyHydrate from 'vue-lazy-hydration';
import NumeraiChart from '../components/Molecules/NumeraiChart';
import BuyButton from '../components/Molecules/BuyButton';
import Web3 from 'web3';

export default {
  name: 'Product',
  transition: 'fade',
  setup(props, context) {
    const qty = ref(1);
    const { id } = context.root.$route.params;
    const { products, search, loading: productLoading } = useProduct(String(id));
    // const { products: relatedProducts, search: searchRelatedProducts, loading: relatedLoading } = useProduct('relatedProducts');
    // const { addItem, loading } = useCart();
    // const { reviews: productReviews, search: searchReviews } = useReview('productReviews');
    const { numerai, getModelInfo, loading: numeraiLoading } = useNumerai(String(id));
    const { web3User, initWeb3Modal, ethereumListener, isAuthenticated } = useUser();
    const { toggleLoginModal } = useUiState();

    const product = computed(() => productGetters.getFiltered(products.value.data, { master: true, attributes: context.root.$route.query })[0]);
    const options = computed(() => productGetters.getAttributes(products.value.data, ['color', 'size']));
    const configuration = computed(() => productGetters.getAttributes(product.value, ['color', 'size']));
    // const categories = computed(() => productGetters.getCategoryIds(product.value));
    // const reviews = computed(() => reviewGetters.getItems(productReviews.value));

    // TODO: Breadcrumbs are temporary disabled because productGetters return undefined. We have a mocks in data
    // const breadcrumbs = computed(() => productGetters.getBreadcrumbs ? productGetters.getBreadcrumbs(product.value) : props.fallbackBreadcrumbs);
    const productGallery = computed(() => productGetters.getGallery(product.value).map(img => ({
      mobile: { url: img.small },
      desktop: { url: img.normal },
      big: { url: img.big },
      alt: product.value._name || product.value.name
    })));

    onSSR(async () => {
      await search({ id });
      // await searchRelatedProducts({ catId: [categories.value[0]], limit: 8 });
      // await searchReviews({ productId: id });
      await getModelInfo({tournament: product?.value?.category?.slug.startsWith('signals') ? 11 : 8, modelName: product.value.name});
    });

    const updateFilter = (filter) => {
      context.root.$router.push({
        path: context.root.$route.path,
        query: {
          ...configuration.value,
          ...filter
        }
      });
    };

    const getNumeraiChartData = (numeraiData) => {
      const transposed = Object.assign(...Object.keys(numeraiData.modelInfo.modelPerformance.roundModelPerformances[0]).map(key =>
        ({ [key]: numeraiData.modelInfo.modelPerformance.roundModelPerformances.slice(0, 20).map(o => o[key]).reverse() })
      ));

      return {
        labels: transposed.roundNumber,
        datasets: [
          {
            label: 'CORR',
            borderColor: '#666666',
            fill: false,
            lineTension: 0,
            data: transposed.corr
          },
          {
            label: 'MMC',
            borderColor: '#acacac',
            fill: false,
            lineTension: 0,
            data: transposed.mmc
          }
        ]
      };
    };

    const resolveProductPlatform = (product) => {
      if (typeof product?.is_on_platform === 'boolean' && product?.is_on_platform === false && product?.third_party_url) {
        const domain = (new URL(product?.third_party_url));
        const urlParts = domain.hostname.split('.').slice(0);
        const baseUrl = urlParts.slice(-(urlParts.length === 4 ? 3 : 2)).join('.');
        return baseUrl;
      }
      if (product?.is_on_platform) {
        return 'NumerBay';
      }
      return '-';
    };

    const handleBuyButtonClick = (product) => {
      if (!isAuthenticated.value) {
        toggleLoginModal();
        return;
      }
      if (!product?.is_on_platform && product?.third_party_url) { // if third party listing
        window.open(product?.third_party_url, '_blank');
      } else {
        context.root.$router.push(`/checkout/payment?product=${product.id}`);
      }
    };

    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    const handleCryptoBuyButtonClick = async (product) => {
      await initWeb3Modal();
      await ethereumListener();
      const sender = web3User.value.activeAccount;
      const receiver = web3User.value.activeAccount;
      const web3 = new Web3(web3User.value.providerEthers.provider);
      web3.eth.sendTransaction({
        from: sender,
        // gasPrice: '50',
        // gas: '50',
        to: receiver,
        value: '1000000000000000'
        // data: ''
      });
      // web3.sendTransaction({to: receiver, from: sender, value: web3.toWei("0.5", "ether")})
    };

    return {
      updateFilter,
      getModelInfo,
      getNumeraiChartData,
      resolveProductPlatform,
      handleBuyButtonClick,
      handleCryptoBuyButtonClick,
      configuration,
      product,
      // reviews,
      reviewGetters,
      averageRating: computed(() => productGetters.getAverageRating(product.value)),
      totalReviews: computed(() => productGetters.getTotalReviews(product.value)),
      // relatedProducts: computed(() => productGetters.getFiltered(relatedProducts.value, { master: true })),
      numerai: computed(() => numerai.value ? numerai.value : null),
      numeraiChartData: computed(() => numerai.value.modelInfo ? getNumeraiChartData(numerai.value) : {}),
      modelInfo: computed(() => numerai.value?.modelInfo ? numerai.value?.modelInfo : null),
      numeraiLoading,
      productLoading,
      // relatedLoading,
      options,
      qty,
      // addItem,
      // loading,
      productGetters,
      productGallery
    };
  },
  components: {
    SfBadge,
    SfAlert,
    SfColor,
    SfProperty,
    SfHeading,
    SfPrice,
    SfRating,
    SfSelect,
    SfAddToCart,
    SfTabs,
    SfGallery,
    SfIcon,
    SfImage,
    SfBanner,
    SfSticky,
    SfReview,
    SfBreadcrumbs,
    SfButton,
    SfLoader,
    InstagramFeed,
    RelatedProducts,
    MobileStoreBanner,
    LazyHydrate,
    NumeraiChart,
    BuyButton
  },
  // test
  data() {
    return {
      stock: 5,
      properties: [
        {
          name: 'Product Code',
          value: '578902-00'
        },
        {
          name: 'Category',
          value: 'Numerai'
        },
        {
          name: 'Material',
          value: 'Cotton'
        },
        {
          name: 'Country',
          value: 'Germany'
        }
      ],
      description: 'The official example model. Submits example predictions.',
      detailsIsActive: false,
      brand:
          'Brand name is the perfect pairing of quality and design. This label creates major everyday vibes with its collection of modern brooches, silver and gold jewellery, or clips it back with hair accessories in geo styles.',
      careInstructions: 'Do not wash!',
      breadcrumbs: [
        {
          text: 'Home',
          route: {
            link: '/'
          }
        },
        {
          text: 'Category',
          route: {
            link: '#'
          }
        },
        {
          text: 'Numerai',
          route: {
            link: '#'
          }
        }
      ]
    };
  }
};
</script>

<style lang="scss" scoped>
#product {
  box-sizing: border-box;
  @include for-desktop {
    max-width: 1272px;
    margin: 0 auto;
  }
}
.divider-pipe {
  padding: var(
    --breadcrumbs-list-item-before-padding,
    0 var(--spacer-sm)
  );
  color: var(--breadcrumbs-list-item-before-color, var(--c-text-muted));
}
.product {
  @include for-desktop {
    display: block;
    width: 60rem;
    margin: var(--spacer-lg) auto;
  }
  &__info {
    margin: var(--spacer-sm) auto;
    @include for-desktop {
      max-width: 32.625rem;
      margin: 0 0 0 7.5rem;
    }
  }
  &__info_full {
    margin: var(--spacer-sm) auto;
  }
  &__header {
    --heading-title-color: var(--c-link);
    --heading-title-font-weight: var(--font-weight--bold);
    --heading-padding: 0;
    text-transform: uppercase;
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      --heading-title-font-weight: var(--font-weight--semibold);
      margin: 0 auto;
    }
  }
  &__subheader {
    --heading-title-color: var(--c-text-muted);
    --heading-title-font-weight: var(--font-weight--bold);
    --heading-padding: 0;
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      --heading-title-font-weight: var(--font-weight--semibold);
      margin: 0 auto;
    }
    &__highlight {
      color: var(--c-primary);
    }
  }
  &__pricing {
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      margin: var(--spacer-sm) 0 var(--spacer-lg) 0;
    }
  }
  &__details {
    margin: var(--spacer-sm) var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      margin: var(--spacer-lg) var(--spacer-2xl);
    }
  }
  &__drag-icon {
    animation: moveicon 1s ease-in-out infinite;
  }
  &__price-and-rating {
    margin: 0 var(--spacer-sm) var(--spacer-base);
    align-items: center;
    @include for-desktop {
      display: flex;
      justify-content: space-between;
      margin: var(--spacer-sm) 0 var(--spacer-lg) 0;
    }
  }
  &__rating {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin: var(--spacer-xs) 0 var(--spacer-xs);
  }
  &__count {
    @include font(
      --count-font,
      var(--font-weight--normal),
      var(--font-size--sm),
      1.4,
      var(--font-family--secondary)
    );
    color: var(--c-text);
    text-decoration: none;
    margin: 0 0 0 var(--spacer-xs);
  }
  &__description {
    @include font(
      --product-description-font,
      var(--font-weight--light),
      var(--font-size--base),
      1.6,
      var(--font-family--primary)
    );
  }
  &__select-size {
    margin: 0 var(--spacer-sm);
    @include for-desktop {
      margin: 0;
    }
  }
  &__colors {
    @include font(
      --product-color-font,
      var(--font-weight--normal),
      var(--font-size--lg),
      1.6,
      var(--font-family--secondary)
    );
    display: flex;
    align-items: center;
    margin-top: var(--spacer-xl);
  }
  &__color-label {
    margin: 0 var(--spacer-lg) 0 0;
  }
  &__color {
    margin: 0 var(--spacer-2xs);
  }
  &__add-to-cart {
    margin: var(--spacer-base) var(--spacer-sm) 0;
    @include for-desktop {
      margin-top: var(--spacer-2xl);
    }
  }
  &__guide,
  &__compare,
  &__save {
    display: block;
    margin: var(--spacer-xl) 0 var(--spacer-base) auto;
  }
  &__compare {
    margin-top: 0;
  }
  &__tabs {
    --tabs-title-z-index: 0;
    margin: var(--spacer-base) auto var(--spacer-2xl);
    --tabs-title-font-size: var(--font-size--lg);
    @include for-desktop {
      margin-top: var(--spacer-xl);
    }
  }
  &__property {
    margin: var(--spacer-base) 0;
    &__button {
      --button-font-size: var(--font-size--base);
    }
  }
  &__review {
    padding-bottom: 24px;
    border-bottom: var(--c-light) solid 1px;
    margin-bottom: var(--spacer-base);
  }
  &__additional-info {
    color: var(--c-link);
    @include font(
      --additional-info-font,
      var(--font-weight--light),
      var(--font-size--sm),
      1.6,
      var(--font-family--primary)
    );
    &__title {
      font-weight: var(--font-weight--normal);
      font-size: var(--font-size--base);
      margin: 0 0 var(--spacer-sm);
      &:not(:first-child) {
        margin-top: 3.5rem;
      }
    }
    &__paragraph {
      margin: 0;
    }
  }
  &__gallery {
    flex: 1;
  }
}
.breadcrumbs {
  margin: var(--spacer-base) auto var(--spacer-lg);
}
@keyframes moveicon {
  0% {
    transform: translate3d(0, 0, 0);
  }
  50% {
    transform: translate3d(0, 30%, 0);
  }
  100% {
    transform: translate3d(0, 0, 0);
  }
}
.last-sale {
  display: flex;
  align-items: center;
  justify-content: center;
}
.last-sale h3 {
  color: var(--c-text-muted);
  font-size: var(--font-size--sm);
}
.third-party-badge {
  padding: 0.4em;
}
.sale-value {
  margin: 0 var(--spacer-xs) 0 var(--spacer-xs);
  font-size: var(--h3-font-size);
}
.numerai-chart {
  margin-top: var(--spacer-xl);
}
.delta-positive {
  color: #00a800;
}
.delta-negative {
  color: #d24141;
}
</style>
