<template>
  <div class="page-wrap">
    <!-- header  -->
    <header class="header-section has-header-main" :class="getHeaderClass()">
      <!-- Header main -->
      <HeaderMain :isTransparent="$route.fullPath === '/' ? 'is-transparent': ''"></HeaderMain>
    </header>
    <Nuxt :key="$route.fullPath"/>
    <Notification/>
    <!-- Footer  -->
    <Footer classname="bg-dark on-dark"></Footer>
  </div><!-- end page-wrap -->
</template>

<script>
export default {
  name: 'DefaultLayout',
  methods: {
    getHeaderClass() {
      if (this.$route.fullPath === '/') {
        return 'bg-gradient-2';
      }
      return '';
    }
  }
};
</script>

