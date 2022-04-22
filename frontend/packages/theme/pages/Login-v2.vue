<template>
  <div class="page-wrap">
    <!-- login section -->
    <loginSectionTwo :authenticated="authenticated"></loginSectionTwo>
  </div><!-- end page-wrap -->
</template>

<script>
import LoginSectionTwo from "../components/section/LoginSectionTwo";

export default {
  name: 'Login',
  components: {
    LoginSectionTwo
  },
  props: {
    authenticated: {
      type: Boolean,
      default: false
    }
  }
};
</script>
