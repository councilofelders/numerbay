<template>
    <footer class="footer-section" :class="classname">
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
