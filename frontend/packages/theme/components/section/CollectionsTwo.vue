<template>
<section class="collection-section section-space bg-primary-dark is-theme">
    <div class="container">
       <div class="section-head-sm" :class="classname">
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

export default {
  name: 'CollectionsTwo',
  props: ['classname'],
  data () {
    return {
      SectionData
    };
  }
};
</script>
