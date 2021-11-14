<template>
  <div id="product">
    <!--<SfBreadcrumbs
      class="breadcrumbs desktop-only"
      :breadcrumbs="breadcrumbs"
    />-->
    <SfLoader :class="{ pollLoading }" :loading="pollLoading">
    <div class="product" v-if="!pollLoading">
      <div class="product__info_full">
        <div class="product__header">
          <SfHeading
            :title="poll.topic"
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
            <div class="product__meta">
              <span class="product__meta__item">Owner:&nbsp;<span class="product__subheader__highlight">{{ pollGetters.getOwner(poll).toUpperCase() }}</span></span>
              <span class='divider-pipe desktop-only'>|</span>
              <span class="product__meta__item">Weight Mode:&nbsp;<span class="product__subheader__highlight">{{ poll.weight_mode.toUpperCase() }}</span></span>
              <span class='divider-pipe desktop-only'>|</span>
              <span class="product__meta__item">End Date:&nbsp;<span class="product__subheader__highlight">{{ pollGetters.getEndDate(poll) }}</span></span>
            </div>
          </div>
        </div>
        <LazyHydrate when-idle>
          <SfTabs id="tabs" :open-tab="1" class="product__tabs">
            <SfTab title="Poll">
<!--              {{poll}}-->
              {{ poll.description }}
              <vue-poll :can-show-results="!poll.is_blind" :multiple="poll.is_multiple" :maxOptions="poll.max_options" :answers="poll.options" @addvote="addVote"/>
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
  SfBreadcrumbs,
  SfButton,
  SfColor,
  SfBadge,
  SfLoader
} from '@storefront-ui/vue';

import InstagramFeed from '~/components/InstagramFeed.vue';
import RelatedProducts from '~/components/Molecules/RelatedProducts.vue';
import { computed } from '@vue/composition-api';
import {pollGetters, usePoll, useUser, useGlobals} from '@vue-storefront/numerbay';
import { useUiState, useUiNotification } from '~/composables';
import { onSSR } from '@vue-storefront/core';
import MobileStoreBanner from '~/components/MobileStoreBanner.vue';
import LazyHydrate from 'vue-lazy-hydration';
import NumeraiChart from '../components/Molecules/NumeraiChart';
import BuyButton from '../components/Molecules/BuyButton';
import SfReview from '~/components/Molecules/SfReview';
import ProductAddReviewForm from '~/components/ProductAddReviewForm';

export default {
  name: 'Voting',
  transition: 'fade',
  setup(props, context) {
    const { id } = context.root.$route.params;
    const { polls, search, loading: pollLoading } = usePoll(String(id));
    const { user, isAuthenticated } = useUser();
    const { globals, getGlobals, loading: globalsLoading } = useGlobals();
    const { toggleLoginModal } = useUiState();
    const { send } = useUiNotification();

    const poll = computed(() => polls?.value?.data[0]);

    onSSR(async () => {
      await search({ id });
      await getGlobals();
    });

    return {
      pollGetters,
      poll,
      globals,
      globalsLoading,
      pollLoading
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
    BuyButton,
    ProductAddReviewForm,
  },
  // test
  methods: {
      addVote(obj){
          console.log('You voted ' + JSON.stringify(obj) + '!');
      }
  },
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
    margin: 0 var(--spacer-sm) 0;
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
