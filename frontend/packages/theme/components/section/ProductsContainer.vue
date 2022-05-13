<template>
  <div class="row g-gs">
    <div v-for="product in []" :key="product.id" class="col-xl-3 col-lg-4 col-sm-6">
      <Products :product="product"></Products>
    </div>
  </div>
</template>

<script>
import SectionData from '@/store/store.js';
import Products from '@/components/section/Products';

export default {
  name: 'ProductsContainer',
  components: {
    Products
  },
  data() {
    return {
      SectionData
    };
  }

};
</script>
