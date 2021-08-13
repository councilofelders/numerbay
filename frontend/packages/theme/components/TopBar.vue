<template>
  <SfTopBar class="topbar">
    <template #left>
      <p>NumerBay is under active development, features will change without prior notice.</p>
    </template>
    <!--<template #center>
    </template>-->
    <template #right>
      <p>This is NOT an<SfButton class="topbar__button sf-button--text" link="https://numer.ai/">Official Website of Numerai</SfButton>.</p>
<!--      <LocaleSelector />-->
    </template>
  </SfTopBar>
</template>

<script>
import { SfButton, SfTopBar } from '@storefront-ui/vue';
import LocaleSelector from './LocaleSelector';

export default {
  components: {
    SfTopBar,
    SfButton,
    LocaleSelector
  }
};

</script>
<style lang="scss" scoped>
.topbar {
  position: relative;
  z-index: 2;
  &__button {
    margin: 0 0 0 var(--spacer-xs);
  }
}
</style>
