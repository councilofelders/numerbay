<template>
  <div class="page-wrap">
    <!-- Hero -->
    <HeroFour :lists="SectionData.breadcrumbData.breadcrumbList.navList" :title="SectionData.breadcrumbData.breadcrumbList.title"
              classname="hero-title"></HeroFour>
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

import ExploreSection from "@/components/section/ExploreSection";
import HeroFour from '@/components/section/HeroFour.vue';

export default {
  name: 'Explore',
  components: {
    ExploreSection,
    HeroFour
  },
  data() {
    return {
      SectionData
    };
  }
};
</script>
