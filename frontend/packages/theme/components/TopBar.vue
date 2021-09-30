<template>
  <SfTopBar class="topbar">
    <template #left>
      <p>NumerBay is in beta. Neither Numerai nor NumerBay is responsible for any loss.</p>
    </template>
    <!--<template #center>
    </template>-->
    <template #right>
      <p>This is NOT an official Numerai project. For support, please post in<SfButton class="topbar__button sf-button--text" link="https://community.numer.ai/channel/numerbay">#numerbay</SfButton></p>
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
