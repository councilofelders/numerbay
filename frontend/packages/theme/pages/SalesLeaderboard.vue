<template>
<div class="page-wrap">
    <!-- hero -->
    <HeroFour classname="hero-title" title="Sales Leaderboard" :lists="[{title: 'Sales Leaderboard'}]"></HeroFour>
    <!-- sales leaderboard section -->
    <SalesLeaderboardSection></SalesLeaderboardSection>
</div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'
import HeroFour from '@/components/section/HeroFour.vue'
import SalesLeaderboardSection from '@/components/section/SalesLeaderboardSection.vue'

export default {
  name: 'SalesLeaderboard',
  components: {
    HeroFour,
    SalesLeaderboardSection
  },
  data () {
    return {
      SectionData
    }
  }
}
</script>
