<template>
  <footer :class="classname" class="footer-section">
    <!-- footer section -->
    <FooterSection></FooterSection>
  </footer><!-- end footer-section -->
</template>

<script>
export default {
  name: 'Footer',
  props: ['classname']
}
</script>
