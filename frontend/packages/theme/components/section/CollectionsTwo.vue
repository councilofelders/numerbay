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
export default {
  name: 'CollectionsTwo',
  props: ['classname']
};
</script>
