<template>
    <section class="section-space-b featured-creator-section">
            <div class="container">
                <!-- section heading -->
                <SectionHeading classname="text-center" :text="SectionData.featuredCreatorsData.title" :content="SectionData.featuredCreatorsData.content" isMargin="mb-3"></SectionHeading>
                <!-- swiper sldier -->
                <FeaturedCreatorSlider></FeaturedCreatorSlider>
                <div class="text-center mt-5">
                    <ButtonLink :text="SectionData.featuredCreatorsData.btnText" link="/author" classname="btn-link btn-link-s1"></ButtonLink>
                </div>
            </div><!-- .container -->
        </section><!-- end featured-creator-section -->
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

export default {
  name: 'FeaturedCreators',
  data () {
    return {
      SectionData
    }
  }
}
</script>
