/* eslint-disable no-undef */
<template>
  <swiper :modules="modules"
          :slides-per-view="2"
          :loop="true"
          :autoHeight="true"
          :pagination="{ clickable: true }"
          :breakpoints='{
        "320": {
          "slidesPerView": 1
        },
        "768": {
          "slidesPerView": 2,
        }
      }' class="swiper-button-s1">
    <swiper-slide v-for="item in SectionData.howItWorkData.howItWorkListFour" :key="item.id">
      <div class="card card-hiw card-hiw-s3">
        <div class="card-body">
          <h4 class="mb-3 card-title"><em
            class="ni ni-question icon icon-sm text-orange icon-circle icon-wbg shadow-sm me-2"></em> {{ item.title }}
          </h4>
          <p class="card-text">{{ item.content }}</p>
        </div><!-- end card-body -->
      </div><!-- end card -->
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
  name: 'HowItWorkSlider',
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
