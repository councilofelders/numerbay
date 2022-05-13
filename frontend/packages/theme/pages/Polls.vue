<template>
  <div class="page-wrap">
    <!-- offer section -->
    <section class="user-panel-section section-space">
      <div class="container">
        <div class="row">
          <!-- user sidebar -->
          <UserSidebar :lists="SectionData.accountSidebarData.navList" :navs="SectionData.editProfileData.editProfileTabNavMobile"
                       title="My Polls"></UserSidebar>
          <!-- offer -->
          <PollsSection></PollsSection>
        </div><!-- end row -->
      </div><!-- end container -->
    </section><!-- end user-panel-section -->
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import PollsSection from "@/components/section/PollsSection";

export default {
  name: 'Polls',
  layout: 'account',
  components: {
    PollsSection
  },
  middleware: [
    'is-authenticated'
  ],
  data() {
    return {
      SectionData
    };
  }
};
</script>
