<template>
  <div class="page-wrap">
    <!-- login section -->
    <loginSectionTwo :authenticated="authenticated"></loginSectionTwo>
  </div><!-- end page-wrap -->
</template>

<script>
export default {
  name: 'Login',
  props: {
    authenticated: {
      type: Boolean,
      default: false
    }
  }
};
</script>
