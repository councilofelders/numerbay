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
<!--          <SfHeading
            :title="productGetters.getName(product)"
            :level="1"
            class="sf-heading&#45;&#45;no-underline sf-heading&#45;&#45;left"
          />-->
          <SfHeading
            :level="1"
            class="sf-heading--no-underline sf-heading--left"
          >
            <template #title><a :href="productGetters.getModelUrl(product)" class="sf-heading__title" target="_blank">{{ productGetters.getName(product) }}</a></template>
          </SfHeading>
          <SfIcon
            icon="drag"
            size="xxl"
            color="var(--c-text-disabled)"
            class="product__drag-icon smartphone-only"
          />
        </div>
        <div class="product__subheader">
          <div class="sf-heading__title h5 sf-heading--no-underline sf-heading--left">
            <div class="product__meta">
              <span class="product__meta__item"><span v-if="!!productGetters.getCategory(product).tournament">Round:&nbsp;</span><span class="product__subheader__highlight" v-if="!globalsLoading && !!productGetters.getCategory(product).tournament">{{ globals.selling_round }}</span></span>
              <span class='divider-pipe desktop-only' v-if="!!productGetters.getCategory(product).tournament">|</span>
              <span class="product__meta__item">Seller:&nbsp;<span class="product__subheader__highlight">{{ product.owner?product.owner.username.toUpperCase():'-' }}</span></span>
              <span class='divider-pipe desktop-only'>|</span>
              <span class="product__meta__item">Type:&nbsp;<span class="product__subheader__highlight">{{ productGetters.getCategory(product).slug.toUpperCase() }}</span></span>
              <span class='divider-pipe desktop-only'>|</span> <span class="product__meta__item">Platform:&nbsp;<SfBadge class="color-warning sf-badge third-party-badge" v-if="!productGetters.getOrderedOption(product, optionIdx).is_on_platform">3rd Party</SfBadge>
              <span class="product__subheader__highlight">{{ productGetters.getOptionPlatform(productGetters.getOrderedOption(product, optionIdx)) }}</span></span>
            </div>
            <div class="product__meta" v-if="productGetters.getMode(productGetters.getOrderedOption(product, optionIdx))">
              <span class="product__meta__item">Mode:&nbsp;<span class="product__subheader__highlight">{{ productGetters.getMode(productGetters.getOrderedOption(product, optionIdx)).toUpperCase() }}</span></span>
              <span class='divider-pipe desktop-only' v-if="productGetters.getMode(productGetters.getOrderedOption(product, optionIdx))==='stake_with_limit'">|</span>
              <span class="product__meta__item"><span v-if="productGetters.getMode(productGetters.getOrderedOption(product, optionIdx))==='stake_with_limit'">Stake Limit:&nbsp;</span><span class="product__subheader__highlight" v-if="productGetters.getMode(productGetters.getOrderedOption(product, optionIdx))==='stake_with_limit'">{{ productGetters.getStakeLimit(productGetters.getOrderedOption(product, optionIdx)) }}</span></span>
            </div>
          </div>
        </div>
        <div class="product__pricing">
          <div class="last-sale">
            <div>
              <div class="product__rating">
                <SfRating
                  :score="averageRating"
                  :max="5"
                />
                <a v-if="!!totalReviews" href="#" class="product__count">
                  ({{ totalReviews }})
                </a>
              </div>
            </div>
            <div class="last-sale" v-if="productGetters.getOrderedOption(product, optionIdx).is_on_platform">
              <span class='divider-pipe desktop-only'>|</span>
              <span class="product__meta__item">
                <h3>Total # Sales</h3>
                <div class="sale-value">{{ product.total_num_sales }}</div>
              </span>
              <!--todo show total sales value instead-->
              <!--<span class='divider-pipe'>|</span>
              <h3>Last Sale</h3>
              <div class="sale-value">{{ product.last_sale_price ? `${product.last_sale_price} ${productGetters.getOrderedOption(product, optionIdx).currency}` : '-' }}</div>
              <p :class="`last-sale-change delta-${Number(product.last_sale_price_delta)>0?'positive':'negative'}`">{{ product.last_sale_price_delta ? `${product.last_sale_price_delta} ${productGetters.getOrderedOption(product, optionIdx).currency} (${(Number(product.last_sale_price_delta)*100.0/(Number(product.last_sale_price)-Number(product.last_sale_price_delta))).toFixed(1)}%)` : '' }}</p>-->
            </div>
          </div>
          <div>
            <SfSelect
              v-e2e="'size-select'"
              :disabled="!(productGetters.getOptions(product).length > 1)"
              v-model="optionIdx"
              label="Option"
              class="sf-select--underlined product__select-size"
              required
            >
              <SfSelectOption v-for="(option, key) in productGetters.getOrderedOptions(product)" :key="key" :value="key">{{ productGetters.getFormattedOption(option) }}</SfSelectOption>
            </SfSelect>
            <SfAddToCart
              v-e2e="'product_add-to-cart'"
              v-model="qty"
              :disabled="productLoading || !productGetters.getIsActive(product) || !productGetters.getOrderedOption(product, optionIdx).is_on_platform || !productGetters.getCategory(product).is_per_round"
              class="product__add-to-cart"
            >
              <template #add-to-cart-btn>
                <SfButton
                  class="sf-add-to-cart__button"
                  :disabled="productLoading || !productGetters.getIsActive(product) || !productGetters.getOrderedOption(product, optionIdx).third_party_url && !productGetters.getOrderedOption(product, optionIdx).is_on_platform"
                  @click="handleBuyButtonClick(product, optionIdx, qty)"
                >
                  {{`${productGetters.getOptionIsOnPlatform(productGetters.getOrderedOption(product, optionIdx)) ? 'Buy for' : 'For Ref Price '} ${productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, optionIdx), true)}`}}
                </SfButton>
              </template>
            </SfAddToCart>
          </div>
          <!--<BuyButton
            :disabled="!productGetters.getIsActive(product) || !product.third_party_url && !product.is_on_platform"
            :price="productGetters.getFormattedPrice(product, withCurrency=!product.is_on_platform, decimals=product.is_on_platform?4:2)"
            :label="product.is_on_platform ? 'NMR' : 'Ref Price'"
            @click="handleBuyButtonClick(product)"
          />-->
        </div>
        <SfLoader :class="{ loader: numeraiLoading }" :loading="numeraiLoading">
          <NumeraiChart class="numerai-chart" v-if="!productLoading && !numeraiLoading && !!productGetters.getCategory(product).tournament" :chartdata="!numerai.modelInfo?{}:numeraiChartData"></NumeraiChart>
        </SfLoader>
        <SfLoader :class="{ loader: numeraiLoading }" :loading="numeraiLoading">
          <div>
            <div class="product__details desktop-only" v-if="!!numerai.modelInfo">
              <span><h4>RANK</h4><p>{{ numerai.modelInfo.modelPerformance.latestRanks.corr }}</p></span>
              <span><h4>REPUTATION</h4><p>{{ Number(numerai.modelInfo.modelPerformance.latestReps.corr).toFixed(4) }}</p></span>
              <span><h4>MMC</h4><p>{{ Number(numerai.modelInfo.modelPerformance.latestReps.mmc).toFixed(4) }}</p></span>
              <span v-if="productGetters.getCategory(product).tournament==8"><h4>FNC</h4><p>{{ Number(numerai.modelInfo.modelPerformance.latestReps.fnc).toFixed(4) }}</p></span>
              <span v-if="productGetters.getCategory(product).tournament==8"><h4>CORR W/ METAMODEL</h4><p>{{ Number(numerai.modelInfo.modelPerformance.roundModelPerformances[0].corrWMetamodel).toFixed(4) }}</p></span>
            </div>
            <div class="product__details desktop-only" v-if="!!numerai.modelInfo">
              <span><h4>OWNER STAKE</h4><p>{{ Number(numerai.modelInfo.nmrStaked).toFixed(2) }} NMR</p></span>
              <span><h4>1 DAY RETURN</h4><p :class="`delta-${Number(numerai.modelInfo.modelPerformance.latestReturns.oneDay)>0?'positive':'negative'}`">
                {{ numerai.modelInfo.modelPerformance.latestReturns.oneDay?Number(numerai.modelInfo.modelPerformance.latestReturns.oneDay).toFixed(2):'-' }}%</p></span>
              <span><h4>3 MTH. RETURN</h4><p :class="`delta-${Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths)>0?'positive':'negative'}`">
                {{ numerai.modelInfo.modelPerformance.latestReturns.threeMonths?Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths).toFixed(2):'-' }}%</p></span>
              <span><h4>1 YR. RETURN</h4><p :class="`delta-${Number(numerai.modelInfo.modelPerformance.latestReturns.oneYear)>0?'positive':'negative'}`">
                {{ numerai.modelInfo.modelPerformance.latestReturns.oneYear?Number(numerai.modelInfo.modelPerformance.latestReturns.oneYear).toFixed(2):'-' }}%</p></span>
              <span><h4>WOKE</h4><p>{{ numerai.modelInfo.startDate.split('T')[0] }}</p></span>
            </div>
            <div class="product__details__mobile smartphone-only" v-if="!!numerai.modelInfo">
              <SfProperty
                  name="Owner Stake"
                  :value="`${Number(numerai.modelInfo.nmrStaked).toFixed(2)} NMR`"
                  class="product__property"
              />
              <SfProperty
                  name="Rank"
                  :value="`${numerai.modelInfo.modelPerformance.latestRanks.corr}`"
                  class="product__property"
              />
              <SfProperty
                  name="Reputation"
                  :value="`${Number(numerai.modelInfo.modelPerformance.latestReps.corr).toFixed(4)}`"
                  class="product__property"
              />
              <SfProperty
                  name="3 Mth. Return"
                  class="product__property"
              >
                <template #value>
                  <span :class="`sf-property__value delta-${Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths)>0?'positive':'negative'}`">
                {{ numerai.modelInfo.modelPerformance.latestReturns.threeMonths?Number(numerai.modelInfo.modelPerformance.latestReturns.threeMonths).toFixed(2):'-' }}%
                  </span>
                </template>
              </SfProperty>
              <SfProperty
                  name="Woke"
                  :value="`${numerai.modelInfo.startDate.split('T')[0]}`"
                  class="product__property"
              />
            </div>
          </div>
        </SfLoader>
        <LazyHydrate when-idle>
          <SfTabs id="tabs" :open-tab="1" class="product__tabs">
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
            <SfTab title="Reviews">
              <SfLoader :class="{ loader: reviewsLoading }" :loading="reviewsLoading">
                <div>
                  <SfReview
                    v-for="review in reviews"
                    :key="reviewGetters.getReviewId(review)"
                    :author="reviewGetters.getReviewAuthor(review).toUpperCase()"
                    :date="reviewGetters.getReviewDate(review)"
                    :message="reviewGetters.getReviewMessage(review)"
                    :max-rating="5"
                    :rating="reviewGetters.getReviewRating(review)"
                    :char-limit="250"
                    read-more-text="Read more"
                    hide-full-text="Read less"
                    class="product__review"
                  >
                    <template #icon v-if="!Boolean(reviewGetters.getReviewIsVerifiedOrder(review))"><span></span></template>
                  </SfReview>
                  <div
                    id="addReview"
                    v-if="productGetters.getIsActive(product)"
                  >
                    <ProductAddReviewForm
                      @add-review="successAddReview"
                    />
                  </div>
                </div>
              </SfLoader>
            </SfTab>
          </SfTabs>
        </LazyHydrate>
      </div>
    </div>
    </SfLoader>
    <LazyHydrate v-if="!!relatedProducts && relatedProducts.length > 0" when-visible>
      <RelatedProducts
        :products="relatedProducts"
        :loading="relatedLoading"
        title="From the same seller"
      />
    </LazyHydrate>
  </div>
</template>
<script>
import {
  SfProperty,
  SfHeading,
  SfRating,
  SfSelect,
  SfAddToCart,
  SfTabs,
  SfIcon,
  SfAlert,
  SfBreadcrumbs,
  SfButton,
  SfBadge,
  SfLoader
} from '@storefront-ui/vue';

import RelatedProducts from '~/components/Molecules/RelatedProducts.vue';
import { ref, computed } from '@vue/composition-api';
import { useProduct, productGetters, useReview, reviewGetters, useNumerai, useUser, useGlobals } from '@vue-storefront/numerbay';
import { useUiState, useUiNotification } from '~/composables';
import { onSSR } from '@vue-storefront/core';
import LazyHydrate from 'vue-lazy-hydration';
import NumeraiChart from '../components/Molecules/NumeraiChart';
import SfReview from '~/components/Molecules/SfReview';
import ProductAddReviewForm from '~/components/ProductAddReviewForm';

export default {
  name: 'Product',
  transition: 'fade',
  setup(props, context) {
    const qty = ref(1);
    const optionIdx = ref('0');
    const { id } = context.root.$route.params;
    const { products, search, loading: productLoading } = useProduct(String(id));
    const { products: relatedProducts, search: searchRelatedProducts, loading: relatedLoading } = useProduct(`relatedProducts-${id}`);
    // const { addItem, loading } = useCart();
    const { reviews: productReviews, search: searchReviews, loading: reviewsLoading, addReview, error: reviewError } = useReview(`productReviews-${id}`);
    const { numerai, getModelInfo, loading: numeraiLoading } = useNumerai(String(id));
    const { user, isAuthenticated } = useUser();
    const { globals, getGlobals, loading: globalsLoading } = useGlobals();
    const { toggleLoginModal } = useUiState();
    const { send } = useUiNotification();

    const product = computed(() => productGetters.getFiltered(products.value.data, { master: true, attributes: context.root.$route.query })[0]);
    // const categories = computed(() => productGetters.getCategoryIds(product.value));
    const reviews = computed(() => reviewGetters.getItems(productReviews.value));

    // TODO: Breadcrumbs are temporary disabled because productGetters return undefined. We have a mocks in data
    // const breadcrumbs = computed(() => productGetters.getBreadcrumbs ? productGetters.getBreadcrumbs(product.value) : props.fallbackBreadcrumbs);

    onSSR(async () => {
      await search({ id });
      await searchRelatedProducts({ filters: {user: {in: [product.value.owner.id]}}}); // catId: product.value.category.id,
      await searchReviews({ productId: id });
      if (product?.value?.category?.tournament) {
        await getModelInfo({tournament: product?.value?.category?.slug.startsWith('signals') ? 11 : 8, modelName: product.value.name});
      }
      await getGlobals();
    });

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

    const handleBuyButtonClick = (product, optionIdx, qty) => {
      const option = productGetters.getOrderedOption(product, optionIdx);
      if (option.is_on_platform && !isAuthenticated.value) {
        send({
          message: 'You need to log in to buy this product',
          type: 'info'
        });
        toggleLoginModal();
        return;
      }
      if (option.is_on_platform && option.currency === 'NMR' && !user.value.numerai_api_key_public_id) { // if not setup numerai api key and product is in NMR
        send({
          message: 'This product requires your Numerai wallet address',
          type: 'info',
          action: {text: 'Set Numerai API Key', onClick: ()=>context.root.$router.push('/my-account/numerai-api')},
          persist: true
        });
        return;
      }
      if (!option.is_on_platform && option.third_party_url) { // if third party listing
        window.open(option.third_party_url, '_blank');
      } else {
        context.root.$router.push(`/checkout/payment?product=${product.id}&option=${option.id}&qty=${qty}`);
      }
    };

    const successAddReview = async (reviewData) => {
      await addReview(reviewData).then(async ()=>{
        if (reviewError.value.addReview) {
          send({
            message: reviewError.value.addReview.message,
            type: 'danger'
          });
        } else {
          await searchReviews({ productId: id }).then(()=>{
            document
              .querySelector('#tabs')
              .scrollIntoView({ behavior: 'smooth', block: 'end' });
          });
          send({
            message: 'Your review was submitted!',
            type: 'success'
          });
        }
      });
    };

    return {
      getModelInfo,
      getNumeraiChartData,
      handleBuyButtonClick,
      product,
      reviews,
      reviewsLoading,
      successAddReview,
      reviewGetters,
      averageRating: computed(() => reviewGetters.getAverageRating(productReviews.value)),
      totalReviews: computed(() => reviewGetters.getTotalReviews(productReviews.value)),
      relatedProducts: computed(() => relatedProducts?.value?.data?.filter((p)=>parseInt(p.id) !== parseInt(id))),
      numerai: computed(() => numerai.value ? numerai.value : null),
      numeraiChartData: computed(() => numerai.value.modelInfo ? getNumeraiChartData(numerai.value) : {}),
      modelInfo: computed(() => numerai.value?.modelInfo ? numerai.value?.modelInfo : null),
      globals,
      globalsLoading,
      numeraiLoading,
      productLoading,
      relatedLoading,
      qty,
      optionIdx,
      // addItem,
      // loading,
      productGetters
    };
  },
  components: {
    SfBadge,
    SfAlert,
    SfProperty,
    SfHeading,
    SfRating,
    SfSelect,
    SfAddToCart,
    SfTabs,
    SfIcon,
    SfReview,
    SfBreadcrumbs,
    SfButton,
    SfLoader,
    RelatedProducts,
    LazyHydrate,
    NumeraiChart,
    ProductAddReviewForm
  },
  // test
  data() {
    return {
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
          text: 'Product',
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
    @include for-mobile {
      display: block;
    }
    &__highlight {
      color: var(--c-primary);
    }
  }
  &__meta {
    display: flex;
    @include for-mobile {
      flex-direction: column;
      //flow: block;
    }
  }
  &__meta__item {
    display: flex;
  }
  &__pricing {
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      margin: var(--spacer-sm) 0 var(--spacer-lg) 0;
    }
    @include for-mobile {
      align-items: flex-start;
      flex-direction: column;
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
  &__details__mobile {
    margin: var(--spacer-sm) var(--spacer-sm);
  }
  &__drag-icon {
    animation: moveicon 1s ease-in-out infinite;
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
  }
  &__add-to-cart {
    margin: 0 var(--spacer-sm) 0;
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
  //align-items: center;
  justify-content: center;
  @include for-mobile {
    align-items: flex-start;
    flex-direction: column;
  }
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
  font-size: var(--h4-font-size);
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
