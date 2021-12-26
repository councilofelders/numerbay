<template>
  <SfSection :title-heading="title" class="section">
    <SfLoader :class="{ loading }" :loading="loading">
      <SfCarousel
        :settings="{ peek: 16, breakpoints: { 1023: { peek: 0, perView: 2 } } }"
        class="carousel"
      >
        <SfCarouselItem class="carousel__item" v-for="(product, i) in products" :key="i">
          <!--<SfProductCard
            :title="productGetters.getName(product)"
            :image="productGetters.getCoverImage(product)"
            :regular-price="$n(productGetters.getPrice(product).regular, 'currency')"
            :special-price="productGetters.getPrice(product).special && $n(productGetters.getPrice(product).special, 'currency')"
            :link="localePath(`/p/${productGetters.getId(product)}/${productGetters.getSlug(product)}`)"
          />-->
          <SfProductCard
            class="related-card"
            :regular-price="productGetters.getFormattedPrice(product)"
            :max-rating="5"
            :score-rating="productGetters.getAverageRating(product)"
            :reviews-count="productGetters.getTotalReviews(product)"
            :image="productGetters.getCoverImage(product)"
            :alt="productGetters.getName(product)"
            :title="productGetters.getName(product)"
            :link="`/p/${productGetters.getId(product)}/${productGetters.getSlug(product)}`"
            :badgeLabel="`${productGetters.getCategory(product).slug.includes('-models') ? 'Model Files ':''}${productGetters.getCategory(product).slug.includes('-data') ? 'Data Files ':''}${product.is_ready ? 'Ready' : ''}`"
            :show-add-to-cart-button="false"
            :isOnWishlist="false"
            :wishlistIcon="false"
          />
        </SfCarouselItem>
      </SfCarousel>
    </SfLoader>
  </SfSection>
</template>

<script lang="ts">

import {
  SfCarousel,
  SfLoader,
  SfProductCard,
  SfSection
} from '@storefront-ui/vue';

import { productGetters } from '@vue-storefront/numerbay';

export default {
  name: 'RelatedProducts',
  setup() {
    return { productGetters };
  },
  components: {
    SfCarousel,
    SfProductCard,
    SfSection,
    SfLoader
  },
  props: {
    title: String,
    products: Array,
    loading: Boolean
  }
};
</script>

<style lang="scss" scoped>
.section {
  margin-top: var(--spacer-base);
}

.carousel {
    margin: 0 calc(var(--spacer-sm) * -1) 0 0;
  @include for-desktop {
    margin: 0;
  }
  &__item {
    margin: 1.9375rem 0 2.4375rem 0;
  }
}

.related-card {
  ::v-deep .sf-image {
    --image-width: 200px;
    --image-height: 200px;
  }
  @include for-mobile {
    ::v-deep .sf-image {
      --image-width: 100%;
      --image-height: 150px;
    }
  }
}
</style>
