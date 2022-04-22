<template>
  <div class="page-wrap">
    <!-- login section -->
    <loginSection></loginSection>
  </div><!-- end page-wrap -->
</template>

<script>
import LoginSection from "@/components/section/LoginSection";

export default {
  name: 'Login',
  components: {
    LoginSection
  }
};
</script>
