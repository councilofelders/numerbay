<template>
  <div :class="isTransparent" class="header-main is-sticky">
    <div class="container">
      <div v-if="!isAuthenticated" class="header-wrap">
        <!-- logo -->
        <Logo></Logo>
        <!-- mobile action -->
        <MobileAction></MobileAction>
        <!-- heder search -->
        <HeaderSearch></HeaderSearch>
        <!-- Menu -->
        <Menu classname="btn-dark"></Menu>
        <div class="header-overlay"></div>
      </div><!-- .header-warp-->
      <div v-else class="header-wrap">
        <!-- logo -->
        <Logo></Logo>
        <!-- mobile action -->
        <MobileActionTwo></MobileActionTwo>
        <!-- heder search -->
        <HeaderSearch class="header-search-form-s2"></HeaderSearch>
        <!-- Menu -->
        <MenuTwo classname="btn-primary"></MenuTwo>
        <div class="header-overlay"></div>
      </div><!-- .header-warp-->
    </div><!-- .container-->
  </div><!-- .header-main-->
</template>
<script>
// @ is an alias to /src
import Logo from '@/components/common/Logo.vue';
import MobileAction from '@/components/common/MobileAction.vue';
import MobileActionTwo from '@/components/common/MobileActionTwo.vue';
import HeaderSearch from '@/components/common/HeaderSearch.vue';
import Menu from '@/components/common/Menu.vue';
import MenuTwo from '@/components/common/MenuTwo.vue';

// Composables
import {onSSR} from '@vue-storefront/core';
import {useUser, useGlobals} from '@vue-storefront/numerbay';

export default {
  name: 'HeaderMain',
  props: ['isTransparent'],
  components: {
    Logo,
    MobileAction,
    MobileActionTwo,
    HeaderSearch,
    Menu,
    MenuTwo
  },
  setup() {
    const {isAuthenticated, load: loadUser} = useUser();
    const {load: loadGlobals} = useGlobals();

    onSSR(async () => {
      await loadUser();
      await loadGlobals();
    });

    return {
      isAuthenticated
    };
  }
};
</script>
