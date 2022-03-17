<template>
<div class="page-wrap">
    <!-- login section -->
    <loginSectionTwo :authenticated="authenticated"></loginSectionTwo>
</div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
export default {
  name: 'Login',
  data () {
    return {
      SectionData
    };
  },
  props: {
    authenticated: {
      type: Boolean,
      default: false
    }
  }
};
</script>
