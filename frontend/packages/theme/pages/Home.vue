<template>
  <div id="home">
    <LazyHydrate when-idle>
      <SfHero class="hero">
        <SfHeroItem
          v-for="(hero, i) in heroes"
          :key="i"
          :title="hero.title"
          :subtitle="hero.subtitle"
          :button-text="hero.buttonText"
          :background="hero.background"
          :image="hero.image"
          :link="hero.link"
          :class="hero.className"
        />
      </SfHero>
    </LazyHydrate>

    <LazyHydrate when-idle>
      <div class="sales-stats">
        <SfCard
          image=""
          :title="`${globals.total_num_products}`"
          :titleLevel="3"
          description="Products Available"
          link=""
        >
          <template #action><span></span></template>
        </SfCard>
        <SfCard
          image=""
          :title="`${globals.total_num_sales}`"
          :titleLevel="3"
          description="Products Sold"
          link=""
        >
          <template #action><span></span></template>
        </SfCard>
        <SfCard
          image=""
          :title="`${globals.total_sales_nmr} NMR`"
          :titleLevel="3"
          description="Sales Value"
          link=""
        >
          <template #action><span></span></template>
        </SfCard>
      </div>
    </LazyHydrate>

    <!--<LazyHydrate when-visible>
      <SfBannerGrid :banner-grid="1" class="banner-grid">
        <template v-for="item in banners" v-slot:[item.slot]>
          <SfBanner
            :key="item.slot"
            :title="item.title"
            :subtitle="item.subtitle"
            :description="item.description"
            :button-text="item.buttonText"
            :image="item.image"
            :class="item.class"
          />
        </template>
      </SfBannerGrid>
    </LazyHydrate>

    <LazyHydrate when-visible>
        <SfCarousel class="carousel" :settings="{ peek: 16, breakpoints: { 1023: { peek: 0, perView: 2 } } }">
          <template #prev="{go}">
            <SfArrow
              aria-label="prev"
              class="sf-arrow&#45;&#45;left sf-arrow&#45;&#45;long"
              @click="go('prev')"
            />
          </template>
          <template #next="{go}">
            <SfArrow
              aria-label="next"
              class="sf-arrow&#45;&#45;right sf-arrow&#45;&#45;long"
              @click="go('next')"
            />
          </template>
          <SfCarouselItem class="carousel__item" v-for="(product, i) in products" :key="i">
            <SfProductCard
              :title="product.title"
              :image="product.image"
              :regular-price="product.price.regular"
              :max-rating="product.rating.max"
              :score-rating="product.rating.score"
              :show-add-to-cart-button="true"
              :is-on-wishlist="product.isInWishlist"
              link="/"
              class="carousel__item__product"
              @click:wishlist="toggleWishlist(i)"
            />
          </SfCarouselItem>
        </SfCarousel>
    </LazyHydrate>-->

    <LazyHydrate when-visible>
      <SfLoader :class="{ loading: !iframe.loaded }" :loading="!iframe.loaded"  class="desktop-only">
        <iframe width="100%" height="747" :src="iframe.src" frameborder="0" allowFullScreen="true" v-if="iframe.loaded" class="desktop-only"></iframe>
      </SfLoader>
    </LazyHydrate>

    <LazyHydrate when-visible>
      <SfCallToAction
        title="Subscribe to COE Numerai Newsletters"
        button-text="Subscribe"
        description="Be aware of all Numerai community happenings!"
        image="/homepage/newsletter.webp"
        class="call-to-action"
        link="https://coenumerainewsletter.substack.com/"
      />
    </LazyHydrate>
  </div>
</template>
<script>
import {
  SfHero,
  SfBanner,
  SfCallToAction,
  SfCard,
  SfSection,
  SfCarousel,
  SfProductCard,
  SfImage,
  SfBannerGrid,
  SfHeading,
  SfArrow,
  SfButton,
  SfLoader
} from '@storefront-ui/vue';
import InstagramFeed from '~/components/InstagramFeed.vue';
import MobileStoreBanner from '~/components/MobileStoreBanner.vue';
import { useGlobals } from '@vue-storefront/numerbay';
import LazyHydrate from 'vue-lazy-hydration';
import axios from 'axios';
import { onSSR } from '@vue-storefront/core';

export default {
  name: 'Home',
  components: {
    InstagramFeed,
    SfHero,
    SfBanner,
    SfCallToAction,
    SfCard,
    SfSection,
    SfCarousel,
    SfProductCard,
    SfImage,
    SfBannerGrid,
    SfHeading,
    SfArrow,
    SfButton,
    SfLoader,
    MobileStoreBanner,
    LazyHydrate
  },
  data() {
    return {
      heroes: [
        {
          title: 'Buy Anything Numerai',
          subtitle: 'NumerBay - The Numerai Community Marketplace',
          buttonText: 'Browse',
          background: '#eceff1',
          image: '/homepage/bannerA.webp',
          link: '/c/numerai'
        }
        // {
        //   title: 'Want to Sell Your Numerai Models?',
        //   subtitle: 'Sign Up to Start Selling',
        //   buttonText: 'Browse',
        //   background: '#eceff1',
        //   image: '/homepage/bannerB.webp',
        //   link: '/c/numerai'
        // }
      ],
      banners: [
      ],
      products: [
      ],
      iframe: {
        src: '',
        loaded: false
      }
    };
  },
  methods: {
    toggleWishlist(index) {
      this.products[index].isInWishlist = !this.products[index].isInWishlist;
    }
  },
  mounted() { // dynamic iframe
    axios.get('https://raw.githubusercontent.com/jos1977/numerai_statistics/main/ClassicDashboardLink.txt').then((response) => {
      this.iframe.src = response.data;
      this.iframe.loaded = true;
    });
  },
  setup() {
    const { globals, getGlobals, loading: globalsLoading } = useGlobals();

    onSSR(async () => {
      await getGlobals();
    });

    return {
      globals,
      globalsLoading
    };
  }
};
</script>

<style lang="scss" scoped>
#home {
  box-sizing: border-box;
  padding: 0 var(--spacer-sm);
  @include for-desktop {
    max-width: 1240px;
    padding: 0;
    margin: 0 auto;
  }
}

.hero {
  margin: var(--spacer-xl) auto var(--spacer-lg);
  --hero-item-background-position: center;
  ::v-deep .sf-link:hover {
    color: var(--c-white);
  }
  @include for-desktop {
    margin: var(--spacer-xl) auto var(--spacer-xl);
  }
  .sf-hero-item {
    &:nth-child(even) {
      --hero-item-background-position: left;
      @include for-mobile {
        --hero-item-background-position: 30%;
       ::v-deep .sf-hero-item__wrapper {
         &.sf-button {
            align-items: flex-end;
            text-align: right;
            padding: var(--spacer-sm) var(--spacer-sm) var(--spacer-sm) var(--spacer-2xl);
         }
        }
        ::v-deep .sf-hero-item__subtitle,
        ::v-deep .sf-hero-item__title {
          width: 100%;
        }
      }
    }
  }
  ::v-deep .sf-hero__control {
    &--right, &--left {
      display: none;
    }
  }
}

.banner-grid {
  --banner-container-width: 50%;
  margin: var(--spacer-xl) 0;
  ::v-deep .sf-link:hover {
    color: var(--c-white);
  }
  @include for-desktop {
    margin: var(--spacer-2xl) 0;
    ::v-deep .sf-link {
      --button-width: auto;
    }
  }
}

.banner {
  &__tshirt {
    background-position: left;
  }
  &-central {
    @include for-desktop {
      --banner-container-flex: 0 0 70%;
    }
  }
}

.similar-products {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacer-2xs);
  --heading-padding: 0;
  border-bottom: 1px var(--c-light) solid;
  @include for-desktop {
    border-bottom: 0;
    justify-content: center;
    padding-bottom: 0;
  }
}

.call-to-action {
  background-position: right;
  margin: var(--spacer-xs) 0;
  @include for-desktop {
    margin: var(--spacer-xl) 0 var(--spacer-2xl) 0;
  }
}

.carousel {
    margin: 0 calc(var(--spacer-sm) * -1) 0 0;
  @include for-desktop {
    margin: 0;
  }
  &__item {
    margin: 1.375rem 0 2.5rem 0;
    @include for-desktop {
      margin: var(--spacer-xl) 0 var(--spacer-xl) 0;
    }
    &__product {
      --product-card-add-button-transform: translate3d(0, 30%, 0);
    }
  }
  ::v-deep .sf-arrow--long .sf-arrow--right {
    --arrow-icon-transform: rotate(180deg);
     -webkit-transform-origin: center;
     transform-origin: center;
  }
}

.sales-stats {
  margin: var(--spacer-xl) auto var(--spacer-lg);
  display: flex;
  justify-content: space-between;
}
</style>
