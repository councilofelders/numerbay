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
import HeroFour from '@/components/section/HeroFour'
import VoteSection from "@/components/section/VoteSection";

export default {
  name: 'Vote',
  components: {
    HeroFour,
    VoteSection
  }
}
</script>
