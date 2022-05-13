<template>
  <section class="collection-section section-space">
    <div class="container">
      <div :class="classname" class="section-head-sm">
        <h2>Collections</h2>
      </div>
      <!-- collection slider -->
      <CollectionSlider></CollectionSlider>
    </div><!-- .container -->
  </section><!-- end collection-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import CollectionSlider from "../common/CollectionSlider";

export default {
  name: 'Collections',
  components: {
    CollectionSlider
  },
  props: ['classname'],
  data() {
    return {
      SectionData
    };
  }
};
</script>
