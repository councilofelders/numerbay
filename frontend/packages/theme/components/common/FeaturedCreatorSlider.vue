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
      slidesPerView: 3
    }
  }"
    :modules="modules"
    :pagination="{ clickable: true }"
    :slides-per-view="3">
    <swiper-slide v-for="item in []" :key="item.id">
      <div class="card card-full card-creator">
        <router-link :to="item.btnLink" class="d-block">
          <img :src="item.img" alt="birds art image" class="card-img-top">
        </router-link>
        <div class="card-body card-body-s1">
          <router-link :to="item.btnLink" class="avatar avatar-1">
            <img :src="item.avatar" alt="avatar" class="rounded-circle">
          </router-link><!-- end avatar -->
          <h4 class="card-title mt-4 pt-2">
            <router-link :to="item.btnLink">{{ item.title }}</router-link>
          </h4>
          <p class="card-text mt-1 mb-3">{{ item.content }}</p>
          <p class="text-dark-gray">
            <span class="me-3 me-xl-4"><strong class="text-black">{{ item.followerNum }}</strong> {{
                item.followerText
              }}</span>
            <span><strong class="text-black">{{ item.followingNum }}</strong> {{ item.followingText }}</span>
          </p>
          <p class="mb-4 mt-1">{{ item.soldText }}</p>
          <ul class="btns-group">
            <li>
              <router-link :to="item.btnLink" class="btn bg-dark-dim">{{ item.followText }}</router-link>
            </li>
          </ul>
        </div><!-- end card-body -->
      </div><!-- end card -->
    </swiper-slide>
    <!-- pagination -->
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
