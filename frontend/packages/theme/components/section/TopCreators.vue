<template>
  <section class="top-creator-section" :class="classname">
    <div class="container">
      <div class="section-head-sm" :class="isCenter">
        <h2>Featured Creators</h2>
      </div>
      <!-- creators -->
      <Creators></Creators>
    </div><!-- .container -->
  </section><!-- end top-creator-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import Creators from "../common/Creators";

export default {
  name: 'TopCreators',
  components: {
    Creators
  },
  props: ['classname', 'isCenter'],
  data() {
    return {
      SectionData
    };
  }
};
</script>
