<template>
  <div class="page-wrap">
    <!-- offer section -->
    <section class="user-panel-section section-space">
      <div class="container">
        <div class="row">
          <!-- user sidebar -->
          <UserSidebar :lists="SectionData.accountSidebarData.navList" :navs="SectionData.editProfileData.editProfileTabNavMobile"
                       title="My Listings"></UserSidebar>
          <!-- offer -->
          <ListingsSection></ListingsSection>
        </div><!-- end row -->
      </div><!-- end container -->
    </section><!-- end user-panel-section -->
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import ListingsSection from "../components/section/ListingsSection";

export default {
  name: 'Listings',
  layout: 'account',
  components: {
    ListingsSection
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
