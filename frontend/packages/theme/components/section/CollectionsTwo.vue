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
import CollectionSlider from "../common/CollectionSlider";

export default {
  name: 'CollectionsTwo',
  components: {
    CollectionSlider
  },
  props: ['classname']
};
</script>
