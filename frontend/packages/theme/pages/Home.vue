<template>
  <div class="page-wrap">
    <!-- Hero  -->
    <HeroSeven></HeroSeven>
    <!-- Category  -->
    <Category classname="section-space bg-gray"></Category>
    <!-- product  -->
<!--        <section class="section-space trending-section bg-gray">
        <div class="container">
            &lt;!&ndash; section heading &ndash;&gt;
            <SectionHeading classname="text-center" :text="SectionData.productData.title" :content="SectionData.productData.content" isMargin="mb-3"></SectionHeading>
            &lt;!&ndash; product &ndash;&gt;
            <ProductsContainer></ProductsContainer>
            <div class="text-center mt-4 mt-md-5">
                <ButtonLink :text="SectionData.productData.btnText" :link="SectionData.productData.btnLink" classname="btn-link btn-link-s1"></ButtonLink>
            </div>
        </div>&lt;!&ndash; .container &ndash;&gt;
    </section>&lt;!&ndash; trending-section &ndash;&gt;-->
    <!-- HowItWork  -->
<!--        <HowItWork classname="col-lg-3" :title="SectionData.howItWorkData.title" :subtitle="SectionData.howItWorkData.content" gutterBottom="mb-3"></HowItWork>-->
    <!-- Newsletter  -->
    <Newsletter></Newsletter>
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import HeroSeven from '@/components/section/HeroSeven.vue';

export default {
  name: 'Home',
  components: {
    HeroSeven
  },
  data () {
    return {
      SectionData
    };
  }
};
</script>
