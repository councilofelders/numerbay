<template>
  <div class="page-wrap">
    <!-- offer section -->
    <section class="user-panel-section section-space">
      <div class="container">
        <div class="row">
          <!-- user sidebar -->
          <UserSidebar title="Purchases" :lists="SectionData.accountSidebarData.navList"
                       :navs="SectionData.editProfileData.editProfileTabNavMobile"></UserSidebar>
          <!-- purchases -->
          <PurchasesSection></PurchasesSection>
        </div><!-- end row -->
      </div><!-- end container -->
    </section><!-- end user-panel-section -->
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import PurchasesSection from "@/components/section/PurchasesSection";

export default {
  name: 'Purchases',
  layout: 'account',
  components: {
    PurchasesSection
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
