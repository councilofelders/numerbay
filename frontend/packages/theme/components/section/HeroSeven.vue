<template>
  <div class="hero-wrap hero-wrap-5">
    <div class="container">
      <div class="row">
        <div class="col-md-9 mx-auto">
          <div class="hero-content py-0 text-center">
            <h1 class="hero-title hero-title-lg mb-4">{{ SectionData.heroDataSix.title }}</h1>
            <p class="hero-text hero-text-s2 px-lg-5">{{ SectionData.heroDataSix.content }}</p>
            <ButtonGroup :btns="SectionData.btnDataThree" classname="hero-btns"></ButtonGroup>
            <div class="row g-gs justify-content-center counter-wrap">
              <div v-for="item in countItemData" :key="item.id" :class="item.className" class="col-sm-4">
                <div class="count-item">
                  <h3 class="count-title">{{ item.title }}</h3>
                  <span class="count-text small">{{ item.text }}</span>
                </div>
              </div>
            </div>
          </div><!-- hero-content -->
        </div><!-- col -->
      </div>
    </div><!-- .container-->
  </div><!-- end hero-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {computed} from '@vue/composition-api';
import {useGlobals} from '@vue-storefront/numerbay';

export default {
  name: 'HeroSeven',
  data() {
    return {
      SectionData
    };
  },
  setup() {
    const {globals} = useGlobals();

    return {
      globals,
      countItemData: computed(() => globals ? [
        {
          id: 1,
          title: `${globals.value.total_num_products || 0}`,
          text: 'Products Available',
          className: 'col-6'
        },
        {
          id: 2,
          title: `${globals.value.total_qty_sales || 0}`,
          text: 'Quantity Sold',
          className: 'col-6'
        },
        {
          id: 3,
          title: `${globals.value.total_sales_nmr || 0} NMR`,
          text: 'Sales Value'
        }
      ] : [])
    };
  }
};
</script>
