<template>
  <section class="section-space-b featured-creator-section">
    <div class="container">
      <!-- section heading -->
      <SectionHeading :content="SectionData.featuredCreatorsData.content" :text="SectionData.featuredCreatorsData.title"
                      classname="text-center" isMargin="mb-3"></SectionHeading>
      <!-- swiper sldier -->
      <FeaturedCreatorSlider></FeaturedCreatorSlider>
      <div class="text-center mt-5">
        <ButtonLink :text="SectionData.featuredCreatorsData.btnText" classname="btn-link btn-link-s1"
                    link="/author"></ButtonLink>
      </div>
    </div><!-- .container -->
  </section><!-- end featured-creator-section -->
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

import FeaturedCreatorSlider from "../common/FeaturedCreatorSlider";

export default {
  name: 'FeaturedCreators',
  components: {
    FeaturedCreatorSlider
  },
  data() {
    return {
      SectionData
    }
  }
}
</script>
