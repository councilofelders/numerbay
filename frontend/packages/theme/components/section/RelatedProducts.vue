<template>
<section class="related-product-section section-space-b">
    <div class="container">
        <!-- section heading -->
        <SectionHeading classname="text-center" :text="title"></SectionHeading>
        <!-- product -->
        <swiper
            :slides-per-view="4"
            :breakpoints="{
              0: {
                  slidesPerView: 1
              },
              767: {
                  slidesPerView: 2
              },
              992: {
                  slidesPerView: 3
              },
              1200: {
                  slidesPerView: 4
              }
            }"
            :pagination="{ clickable: true }">
            <swiper-slide v-for="product in products" :key="product.id" >
                <ProductCardSmall :product="product"></ProductCardSmall>
<!--                <div class="card card-full">
                    <div class="card-image">
                        <img :src="productGetters.getCoverImage(product)" class="card-img-top" alt="art image">
                    </div>
                    <div class="card-body p-4">
                        <h5 class="card-title text-truncate mb-0">{{ productGetters.getName(product).toUpperCase() }}</h5>
                        <div class="card-author mb-1 d-flex align-items-center">
                            <span class="me-1 card-author-by">{{ productGetters.getCategory(product).slug }}</span>
                            <div class="custom-tooltip-wrap">
&lt;!&ndash;                                <router-link :to="product.authorLink" class="author-link">{{ product.author }}</router-link>&ndash;&gt;
                            </div>
                        </div>&lt;!&ndash; end card-author &ndash;&gt;
                        <div class="card-price-wrap d-flex align-items-center justify-content-between mb-3">
                          <div class="me-2">
                              <span class="card-price-title">Price</span>
                              <span class="card-price-number">{{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, product.optionIdx)) }}</span>
                          </div>
                          <div>
                              <a class="custom-tooltip author-link">Metrics...</a>
                              <div class="card-generic custom-tooltip-dropdown">abc</div>
                          </div>
                        </div>&lt;!&ndash; end card-price-wrap &ndash;&gt;
                       <span class="btn btn-sm" :class="productGetters.getIsActive(product)?'btn-dark':'btn-light disabled'">Buy</span>
                    </div>&lt;!&ndash; end card-body &ndash;&gt;
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
                            latestRepCorr: productGetters.getModelRep(product, 'corr'),
                            latestRepMmc: productGetters.getModelRep(product, 'mmc'),
                            latestRepFnc: productGetters.getModelRep(product, 'fnc'),
                            latestRepTc: productGetters.getModelRep(product, 'tc'),

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
                </div>&lt;!&ndash; end card &ndash;&gt;-->
            </swiper-slide>
        </swiper>
    </div><!-- .container -->
</section><!-- end related-product-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import {createPopper} from '@popperjs/core';
import ProductCardSmall from '@/components/section/ProductCardSmall';

// core version + navigation, pagination modules:
import { Pagination } from 'swiper';
import { SwiperCore } from 'swiper-vue2';

// configure Swiper to use modules
SwiperCore.use([Pagination]);

// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper-vue2';

// Composables
import { productGetters } from '@vue-storefront/numerbay';

export default {
  name: 'RelatedProducts',
  props: {
    title: {
      type: String,
      default: 'Related Products'
    },
    products: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  components: {
    Swiper,
    SwiperSlide,
    ProductCardSmall
  },
  data() {
    return {
      SectionData
    };
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
 .author-linkm,
 .card-price-wrap {
   z-index: 2;
   position: relative;
 }
 .swiper-container {
    overflow: visible;
  }
</style>
