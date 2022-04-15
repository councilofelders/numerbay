<template>
  <div class="page-wrap">
    <!-- Hero -->
    <HeroFour classname="hero-title" :title="SectionData.breadcrumbData.breadcrumbList.title"
              :lists="SectionData.breadcrumbData.breadcrumbList.navList"></HeroFour>
    <!-- Explore section  -->
    <ExploreSection></ExploreSection>
    <!-- top creators -->
    <!--    <TopCreators classname="section-space-t"></TopCreators>-->
    <!-- Collections -->
    <!--    <Collections></Collections>-->
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import HeroFour from '@/components/section/HeroFour.vue';

export default {
  name: 'Explore',
  components: {
    HeroFour
  },
  data() {
    return {
      SectionData
    };
  }
};
</script>
