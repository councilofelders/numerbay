<template>
  <div class="page-wrap">
    <!-- hero -->
    <HeroFour classname="hero-title" :title="'Vote'" :lists="[
      {
        title: 'Vote'
      }
    ]"></HeroFour>
    <VoteSection></VoteSection>
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'
import HeroFour from '@/components/section/HeroFour.vue'

export default {
  name: 'Vote',
  components: {
    HeroFour
  },
  data() {
    return {
      SectionData
    }
  }
}
</script>
