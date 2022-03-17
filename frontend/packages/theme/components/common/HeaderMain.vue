<template>
    <div class="header-main is-sticky" :class="isTransparent">
        <div class="container">
            <div class="header-wrap" v-if="!isAuthenticated">
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
            <div class="header-wrap" v-else>
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
import { onSSR } from '@vue-storefront/core';
import { useUser } from '@vue-storefront/numerbay';

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
    const { isAuthenticated, load: loadUser } = useUser();

    onSSR(async () => {
      await loadUser();
    });

    return {
      isAuthenticated
    };
  }
};
</script>
