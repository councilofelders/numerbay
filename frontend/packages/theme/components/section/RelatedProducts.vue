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
        <swiper-slide v-for="product in products" :key="product.id">
          <ProductCardSmall :product="product"></ProductCardSmall>
        </swiper-slide>
      </swiper>
    </div><!-- .container -->
  </section><!-- end related-product-section -->
</template>

<script>
import ProductCardSmall from '@/components/section/ProductCardSmall';

// core version + navigation, pagination modules:
import {Pagination} from 'swiper';
import {SwiperCore} from 'swiper-vue2';

// configure Swiper to use modules
SwiperCore.use([Pagination]);

// Import Swiper Vue.js components
import {Swiper, SwiperSlide} from 'swiper-vue2';

// Composables
import {productGetters} from '@vue-storefront/numerbay';

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
  setup() {
    return {
      productGetters
    };
  }
};
</script>

<style lang="css" scoped>
</style>
