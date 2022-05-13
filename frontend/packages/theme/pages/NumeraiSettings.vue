<template>
  <div class="page-wrap">
    <!-- account section -->
    <section class="user-panel-section section-space">
      <div class="container">
        <div class="row">
          <!-- user sidebar -->
          <UserSidebar :lists="SectionData.accountSidebarData.navList" title="Numerai Settings"></UserSidebar>
          <NumeraiSettingSection></NumeraiSettingSection>
        </div><!-- end row -->
      </div><!-- end container -->
    </section><!-- end user-panel-section -->
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import NumeraiSettingSection from "@/components/section/NumeraiSettingSection";

export default {
  name: 'NumeraiSettings',
  layout: 'account',
  components: {
    NumeraiSettingSection
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
