/* eslint-disable no-undef */
<template>
  <swiper
    :breakpoints="{
        0: {
          slidesPerView: 1
        },
        767: {
          slidesPerView: 2
        },
        992: {
          slidesPerView: 4
        }
     }"
    :loop="true"
    :modules="modules"
    :pagination="{ clickable: true }"
    :slides-per-view="4" class="swiper-container-space">
    <swiper-slide v-for="item in []" :key="item.id" class="h-auto">
      <router-link :to="item.path" class="card card-full card-collection">
        <img :src="item.img" alt="birds art image" class="card-img-top">
        <div class="card-body card-body-s1">
          <div class="avatar avatar-1">
            <img :src="item.avatar" alt="avatar" class="rounded-circle">
          </div><!-- end avatar -->
          <h4 class="card-title mt-4 mb-2 pt-1">{{ item.title }}</h4>
          <p class="fw-semibold">{{ item.price }}</p>
        </div><!-- end card-body -->
      </router-link><!-- end card -->
    </swiper-slide>
  </swiper>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// core version + navigation, pagination modules:
import {Pagination} from 'swiper';
import {SwiperCore} from 'swiper-vue2';

// configure Swiper to use modules
SwiperCore.use([Pagination]);

// Import Swiper Vue.js components
import {Swiper, SwiperSlide} from 'swiper-vue2';

export default {
  name: 'CollectionSlider',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      SectionData
    };
  },
  setup() {
    return {
      modules: [Pagination]
    };
  }
};
</script>
