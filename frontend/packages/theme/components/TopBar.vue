<template>
  <SfTopBar class="topbar">
    <template #left>
      <p><SfLink class="topbar__button sf-button--text" href="https://docs.numerbay.ai/" target="_blank">Docs & Tutorials</SfLink></p>
    </template>
    <!--<template #center>
    </template>-->
    <template #right>
      <p>This is NOT an official Numerai project. Neither Numerai nor NumerBay is responsible for any loss. For support, please post in<SfLink class="topbar__button sf-button--text" href="https://community.numer.ai/channel/numerbay" target="_blank">#numerbay</SfLink></p>
<!--      <LocaleSelector />-->
    </template>
  </SfTopBar>
</template>

<script>
import { SfLink, SfTopBar } from '@storefront-ui/vue';
import LocaleSelector from './LocaleSelector';

export default {
  components: {
    SfTopBar,
    SfLink,
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
